import pandas as pd
from pytrends.request import TrendReq
import streamlit as st

# =====================================================================
# 1. 데이터 수집 함수 (반드시 호출부보다 위에 위치해야 합니다)
# =====================================================================
@st.cache_data(ttl=3600)  # 1시간 동안 캐싱하여 구글 IP 차단 방지
def get_trends_dataframe(keywords, timeframe="today 3-m"):
    try:
        pytrends = TrendReq(hl="ko-KR", tz=540)
        pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo="KR")
        df = pytrends.interest_over_time()

        if not df.empty and "isPartial" in df.columns:
            df = df.drop(columns=["isPartial"])
        return df
    except Exception as e:
        st.error(f"구글 트렌드 데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return None

# =====================================================================
# 2. Streamlit 웹 UI 구성 및 호출 함수
# =====================================================================
def main():
    st.title("📊 실시간 구글 트렌드 분석 대시보드")
    st.subheader("대표님을 위한 마케팅 키워드 모니터링 자동화 시스템")

    # 사이드바 설정
    st.sidebar.header("🔍 검색 조건 설정")
    kw_input = st.sidebar.text_input(
        "분석할 키워드 (쉼표로 구분, 최대 5개)", "파이썬, 챗GPT"
    )
    keywords = [kw.strip() for kw in kw_input.split(",") if kw.strip()]

    timeframe_options = {
        "최근 1달": "today 1-m",
        "최근 3달": "today 3-m",
        "최근 1년": "today 12-m",
    }
    selected_period = st.sidebar.selectbox(
        "조회 기간 선택", list(timeframe_options.keys())
    )
    timeframe = timeframe_options[selected_period]

    # 실행 버튼 클릭 시
    if st.sidebar.button("트렌드 데이터 조회하기"):
        if not keywords:
            st.warning("최소 하나 이상의 키워드를 입력해 주세요.")
            return

        if len(keywords) > 5:
            st.error("구글 트렌드 API 제한으로 키워드는 최대 5개까지만 가능합니다.")
            return

        with st.spinner("구글 트렌드에서 데이터를 분석 중입니다..."):
            # 위에서 정의한 함수를 여기서 호출합니다.
            df = get_trends_dataframe(keywords, timeframe)

        if df is not None and not df.empty:
            st.markdown("### 📈 시간 경과에 따른 관심도 추이")
            st.line_chart(df)

            st.markdown("### 📋 상세 데이터 테이블")
            st.dataframe(df.sort_index(ascending=False), use_container_width=True)

            csv = df.to_csv(encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 분석 데이터 CSV 다운로드",
                data=csv,
                file_name=f"google_trends_{timeframe}.csv",
                mime="text/csv",
            )
        else:
            st.info("조회된 데이터가 없습니다. 키워드를 확인해 주세요.")

# =====================================================================
# 3. 프로그램 시작점
# =====================================================================
if __name__ == "__main__":
    main()