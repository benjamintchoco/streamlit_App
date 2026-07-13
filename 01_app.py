
import streamlit as st
from datetime import date
import random

st.set_page_config(page_title="Star Football Match",page_icon="⭐",layout="centered")

CSS=open("style.css",encoding="utf-8").read()
st.markdown(f"<style>{CSS}</style>",unsafe_allow_html=True)

PLAYERS={
"양자리":[{"name":"Kylian Mbappé","club":"Real Madrid","country":"France","img":"https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=600","desc":"폭발적인 스피드와 결정력이 뛰어난 공격수."},
{"name":"Vinicius Jr.","club":"Real Madrid","country":"Brazil","img":"https://images.unsplash.com/photo-1547347298-4074fc3086f0?w=600","desc":"화려한 드리블과 돌파가 장점."}],
"황소자리":[{"name":"Declan Rice","club":"Arsenal","country":"England","img":"https://images.unsplash.com/photo-1518091043644-c1d4457512c6?w=600","desc":"안정적인 수비형 미드필더."}],
"쌍둥이자리":[{"name":"Lamine Yamal","club":"Barcelona","country":"Spain","img":"https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?w=600","desc":"창의적인 윙어."}],
"게자리":[{"name":"Son Heung-min","club":"Tottenham","country":"Korea","img":"https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600","desc":"양발 능력이 뛰어난 공격수."}],
"사자자리":[{"name":"Jude Bellingham","club":"Real Madrid","country":"England","img":"https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=600","desc":"리더십이 뛰어난 미드필더."}],
"처녀자리":[{"name":"Pedri","club":"Barcelona","country":"Spain","img":"https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600","desc":"경기 조율 능력이 뛰어남."}],
"천칭자리":[{"name":"Paulo Dybala","club":"Roma","country":"Argentina","img":"https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a?w=600","desc":"기술적인 플레이."}],
"전갈자리":[{"name":"Virgil van Dijk","club":"Liverpool","country":"Netherlands","img":"https://images.unsplash.com/photo-1547347298-4074fc3086f0?w=600","desc":"세계적인 수비수."}],
"사수자리":[{"name":"Jack Grealish","club":"Manchester City","country":"England","img":"https://images.unsplash.com/photo-1518091043644-c1d4457512c6?w=600","desc":"드리블이 뛰어난 윙어."}],
"염소자리":[{"name":"Harry Kane","club":"Bayern","country":"England","img":"https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600","desc":"최고 수준의 스트라이커."}],
"물병자리":[{"name":"Kevin De Bruyne","club":"Napoli","country":"Belgium","img":"https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600","desc":"최고의 플레이메이커."}],
"물고기자리":[{"name":"Neymar","club":"Santos","country":"Brazil","img":"https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=600","desc":"개인기와 창의성이 뛰어남."}],
}
def z(d):
 m,day=d.month,d.day
 return "양자리" if (m==3 and day>=21)or(m==4 and day<=19) else "황소자리" if (m==4 and day>=20)or(m==5 and day<=20) else "쌍둥이자리" if (m==5 and day>=21)or(m==6 and day<=21) else "게자리" if (m==6 and day>=22)or(m==7 and day<=22) else "사자자리" if (m==7 and day>=23)or(m==8 and day<=22) else "처녀자리" if (m==8 and day>=23)or(m==9 and day<=22) else "천칭자리" if (m==9 and day>=23)or(m==10 and day<=22) else "전갈자리" if (m==10 and day>=23)or(m==11 and day<=22) else "사수자리" if (m==11 and day>=23)or(m==12 and day<=21) else "염소자리" if (m==12 and day>=22)or(m==1 and day<=19) else "물병자리" if (m==1 and day>=20)or(m==2 and day<=18) else "물고기자리"
st.title("⭐ Star Football Match")
b=st.date_input("생년월일",date(2006,1,1))
if st.button("추천받기"):
 s=z(b);p=random.choice(PLAYERS[s]);st.subheader(f"별자리 : {s}")
 st.image(p["img"],use_container_width=True)
 st.markdown(f"### ⚽ {p['name']}\n🌍 {p['country']}  \n🏟 {p['club']}\n\n{p['desc']}")
 st.info("※ 재미를 위한 추천입니다.")

pip install -r requirements.txt
streamlit run app.py
streamlit

body{background:#08111f}.stApp{background:linear-gradient(#08111f,#111c35)}
