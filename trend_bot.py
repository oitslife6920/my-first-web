import os
from pytrends.request import TrendReq


def run_trend_automation():
    print("구글 트렌드 데이터 수집을 시작합니다...")

    # 1. 구글 트렌드 연결 설정 (한국어, 한국 시간대)
    pytrends = TrendReq(hl="ko-KR", tz=540)

    # 2. 분석할 키워드 및 조건 설정 (최대 5개)
    keywords = ["파이썬", "챗GPT"]
    # timeframe 변경 가능 예: 'today 1-m'(최근 1달), 'today 3-m'(최근 3달)
    pytrends.build_payload(kw_list=keywords, timeframe="today 3-m", geo="KR")

    # 3. 데이터 가져오기 (Pandas 데이터프레임 반환)
    df = pytrends.interest_over_time()

    if df.empty:
        print("수집된 데이터가 없습니다.")
        return

    # 4. [Pandas 활용 1] 불필요한 'isPartial' 컬럼 제거
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    # 5. [Pandas 활용 2] 데이터 확인하기
    print("\n--- 최근 5일 데이터 확인 ---")
    print(df.tail())  # 가장 최근 5행 출력

    print("\n--- 요약 통계량 (평균 검색량 등) ---")
    print(df.mean())  # 각 키워드의 평균 관심도 출력

    # 6. [Pandas 활용 3] 엑셀 및 CSV 파일로 자동 저장 (자동화의 핵심)
    # 한글 깨짐 방지를 위해 인코딩 설정 추가
    csv_filename = "google_trends_report.csv"
    df.to_csv(csv_filename, encoding="utf-8-sig")

    print(
        f"\n[성공] 데이터가 '{csv_filename}' 파일로 자동 저장되었습니다."
    )
    print(f"파일 저장 위치: {os.getcwd()}")


if __name__ == "__main__":
    run_trend_automation()