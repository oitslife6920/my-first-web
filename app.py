import streamlit as st
import pandas as pd
import numpy as np

# 1. 홈페이지의 브라우저 탭 제목 설정
st.set_page_config(page_title="대표님의 첫 홈페이지", page_icon="✨")

# 2. 화면에 보여줄 내용 적기
st.title("🚀 나의 첫 파이썬 홈페이지")
st.subheader("아무것도 모르는 상태에서 시작해 서버 구동까지 성공!")

st.markdown("""
---
### 🛠️ 앞으로 업데이트할 기능들
1. 실시간 데이터 분석 그래프 넣기
2. 클로드(Claude) AI 챗봇 연동하기
3. 나만의 디지털 지식 저장소 구축하기
""")

# 3. 유저의 입력을 받는 인터랙티브 상자
name = st.text_input("방문하신 분의 이름을 알려주세요:")
if name:
    st.success(f"안녕하세요, {name} 대표님! 홈페이지가 완벽하게 작동 중입니다.")


st.markdown("---")
st.subheader("📊 나의 월별 목표 달성률 추이")

# 테스트용 가상 데이터 생성 (최근 5달 동안의 데이터)
chart_data = pd.DataFrame(
    {
        "목표량": [80, 85, 90, 95, 100],
        "실제달성량": [75, 88, 89, 94, 102]
    },
    index=["1월", "2월", "3월", "4월", "5월"]
)

# 화면에 멋진 선 그래프 그리기
st.line_chart(chart_data)

