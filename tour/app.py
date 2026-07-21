import streamlit as st
import requests
import pandas as pd
import random
import datetime
import folium
from streamlit_folium import st_folium

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="🎉 전국 축제 탐험대",
    page_icon="🎈",
    layout="wide"
)

# --- API 키 로드 ---
try:
    API_KEY = st.secrets["TOUR_API_KEY"]
except KeyError:
    st.error("⚠️ API 키가 설정되지 않았습니다. .streamlit/secrets.toml 또는 Streamlit Cloud Secrets에 TOUR_API_KEY를 설정해주세요.")
    st.stop()

# API 기본 URL (TourAPI 4.0 국문관광정보서비스)
BASE_URL = "http://apis.data.go.kr/B551011/KorService1/searchFestival1"

# --- API 데이터 가져오기 함수 (캐싱 적용) ---
@st.cache_data(ttl=3600)  # 1시간 동안 결과 캐싱
def fetch_festivals(event_start_date):
    params = {
        'serviceKey': API_KEY,
        'numOfRows': '100',
        'pageNo': '1',
        'MobileOS': 'ETC',
        'MobileApp': 'FestivalApp',
        '_type': 'json',
        'listYN': 'Y',
        'arrange': 'A',  # 제목순
        'eventStartDate': event_start_date
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
        if isinstance(items, dict):  # 아이템이 1개일 경우 Dict로 올 수 있음
            items = [items]
        return items
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return []

# --- UI 레이아웃 ---
st.title("🎈 전국 방방곡곡 축제 탐험대")
st.caption("한국관광공사 Open API 데이터를 기반으로 전국의 신나는 축제 정보를 알려드립니다.")

# Sidebar - 검색 옵션
st.sidebar.header("🔍 축제 검색 옵션")
today_str = datetime.datetime.now().strftime("%Y%m%d")
selected_date = st.sidebar.date_input("축제 시작일 기준", datetime.datetime.now())
search_date_str = selected_date.strftime("%Y%m%d")

# 데이터 로드
with st.spinner("축제 데이터를 불러오는 중..."):
    festivals = fetch_festivals(search_date_str)

if not festivals:
    st.warning("이용 가능한 축제 정보가 없거나 API 호출에 실패했습니다.")
    st.stop()

# 데이터프레임 변환
df = pd.DataFrame(festivals)

# --- Tab 구성 ---
tab1, tab2, tab3 = st.tabs(["🎪 축제 목록 보기", "🎲 오늘 어디 갈까? (룰렛)", "🗺️ 축제 지도"])

# ----------------------------------------------------
# TAB 1: 축제 목록 보기
# ----------------------------------------------------
with tab1:
    st.subheader(f"📅 {selected_date.strftime('%Y년 %m월 %d일')} 이후 개막하는 축제 목록 (총 {len(df)}개)")
    
    # 키워드 검색 필터
    search_term = st.text_input("축제 이름으로 검색해보세요!", "")
    
    filtered_df = df
    if search_term:
        filtered_df = df[df['title'].str.contains(search_term, case=False, na=False)]

    # Grid 형태로 포토카드 배치
    cols = st.columns(3)
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            with st.container(border=True):
                # 이미지 표시
                img_url = row.get('firstimage') or "https://via.placeholder.com/300x200?text=No+Image"
                st.image(img_url, use_column_width=True)
                
                st.markdown(f"### {row.get('title', '제목 없음')}")
                st.write(f"📅 **기간**: {row.get('eventstartdate', '')} ~ {row.get('eventenddate', '')}")
                st.write(f"📍 **위치**: {row.get('addr1', '주소 정보 없음')}")
                
                # 상세 보기 토글
                with st.expander("더보기"):
                    st.write(f"📞 **문의/전화**: {row.get('tel', '정보 없음')}")

# ----------------------------------------------------
# TAB 2: 재미있는 랜덤 룰렛 기능
# ----------------------------------------------------
with tab2:
    st.subheader("🎲 주말에 뭐 하지? 랜덤 축제 추천!")
    st.write("버튼을 누르면 전국 축제 중 하나를 무작위로 뽑아드립니다!")

    if st.button("🎉 축제 뽑기!", type="primary"):
        random_festival = random.choice(festivals)
        
        st.balloons()  # 축하 효과!
        
        st.markdown("### 🎯 당첨된 축제는?!")
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            rand_img = random_festival.get('firstimage') or "https://via.placeholder.com/300x200?text=No+Image"
            st.image(rand_img, use_column_width=True)
            
        with res_col2:
            st.title(f"✨ {random_festival.get('title')}")
            st.markdown(f"- **행사 기간**: {random_festival.get('eventstartdate')} ~ {random_festival.get('eventenddate')}")
            st.markdown(f"- **장소**: {random_festival.get('addr1', '정보 없음')}")
            st.markdown(f"- **연락처**: {random_festival.get('tel', '정보 없음')}")

# ----------------------------------------------------
# TAB 3: 축제 지도 시각화
# ----------------------------------------------------
with tab3:
    st.subheader("🗺️ 한눈에 보는 전국 축제 지도")
    
    # 좌표 정보가 유효한 데이터만 필터링
    map_data = df.dropna(subset=['mapx', 'mapy'])
    
    if not map_data.empty:
        # 지도 시작 위치 (첫 번째 축제 위치 또는 한국 중심)
        start_lat = float(map_data.iloc[0]['mapy'])
        start_lon = float(map_data.iloc[0]['mapx'])
        
        m = folium.Map(location=[start_lat, start_lon], zoom_start=7)
        
        for _, row in map_data.iterrows():
            try:
                lat = float(row['mapy'])
                lon = float(row['mapx'])
                title = row['title']
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(f"<b>{title}</b><br>{row.get('addr1', '')}", max_width=200),
                    tooltip=title,
                    icon=folium.Icon(color='red', icon='star')
                ).add_to(m)
            except ValueError:
                continue
                
        st_folium(m, width=1000, height=500)
    else:
        st.info("지도에 표시할 좌표 정보가 없습니다.")
