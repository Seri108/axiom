# main.py
import math
import random

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="통합 웹앱", page_icon="🧮")


# ------------------------------
# 1. 다기능 계산기 앱 (기존 코드 유지)
# ------------------------------
def calculator_app():
    st.title("🧮 다기능 계산기 웹앱")
    st.write(
        "깃허브 & 스트림릿으로 만든 간단한 계산기입니다.\n"
        "아래에서 원하는 연산을 선택하고 값을 입력해 보세요."
    )

    operation = st.radio(
        "원하는 연산을 선택하세요:",
        (
            "사칙연산 (+, -, ×, ÷)",
            "모듈러 연산 (a % b)",
            "지수 연산 (a^b)",
            "로그 연산 (log₍base₎(value))",
        ),
    )

    st.divider()

    # 사칙연산
    if operation == "사칙연산 (+, -, ×, ÷)":
        st.subheader("사칙연산")
        a = st.number_input("첫 번째 수 (a)", value=0.0)
        b = st.number_input("두 번째 수 (b)", value=0.0)

        op = st.selectbox("연산자를 선택하세요:", ["+", "-", "×", "÷"])

        if st.button("계산하기"):
            try:
                if op == "+":
                    result = a + b
                elif op == "-":
                    result = a - b
                elif op == "×":
                    result = a * b
                elif op == "÷":
                    if b == 0:
                        st.error("0으로 나눌 수 없습니다.")
                        st.stop()
                    result = a / b
                st.success(f"결과: {result}")
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

    # 모듈러 연산
    elif operation == "모듈러 연산 (a % b)":
        st.subheader("모듈러 연산 (a % b)")
        a = st.number_input("a 값 (정수 권장)", value=0.0)
        b = st.number_input("b 값 (0이 아닌 수)", value=1.0)

        if st.button("계산하기"):
            if b == 0:
                st.error("b 는 0이 될 수 없습니다.")
            else:
                try:
                    result = a % b
                    st.success(f"결과: {result}")
                except Exception as e:
                    st.error(f"에러가 발생했습니다: {e}")

    # 지수 연산
    elif operation == "지수 연산 (a^b)":
        st.subheader("지수 연산 (a^b)")
        a = st.number_input("밑 a", value=2.0)
        b = st.number_input("지수 b", value=2.0)

        if st.button("계산하기"):
            try:
                result = a ** b
                st.success(f"결과: {result}")
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

    # 로그 연산
    elif operation == "로그 연산 (log₍base₎(value))":
        st.subheader("로그 연산")
        value = st.number_input(
            "로그를 취할 값 (value, 0보다 커야 함)",
            value=1.0,
            min_value=1e-9,
            format="%.6f",
        )
        base = st.number_input(
            "밑 (base, 0보다 크고 1이 아니어야 함)",
            value=10.0,
            min_value=1e-9,
            format="%.6f",
        )

        if st.button("계산하기"):
            if base == 1:
                st.error("base 는 1이 될 수 없습니다.")
            else:
                try:
                    result = math.log(value) / math.log(base)
                    st.success(f"결과: log₍{base}₎({value}) = {result}")
                except Exception as e:
                    st.error(f"에러가 발생했습니다: {e}")


# ------------------------------
# 2. 확률 시뮬레이터 (예시 구현)
#    이미 만든 코드가 있다면 이 함수 안을
#    네 코드로 바꿔도 됨.
# ------------------------------
def probability_simulator_app():
    st.title("🎲 확률 시뮬레이터")

    st.write("어떤 사건이 일어날 확률 p와 시행 횟수를 정해서 모의 실험을 해봅니다.")

    p = st.slider("사건이 일어날 확률 p", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    n = st.number_input("시행 횟수 n (양의 정수)", min_value=1, value=1000, step=1)

    if st.button("시뮬레이션 시작"):
        successes = 0
        for _ in range(int(n)):
            if random.random() < p:
                successes += 1

        freq = successes / n

        st.write(f"성공한 횟수: {successes} / {int(n)}")
        st.write(f"실험에서 관측된 성공 비율: {freq:.4f}")
        st.write(f"이론적인 확률 p: {p:.4f}")

        st.bar_chart(
            pd.DataFrame(
                {
                    "비율": [p, freq],
                },
                index=["이론값 p", "실험값"],
            )
        )


# ------------------------------
# 3. 연도별 세계인구 분석 앱
#    - 첨부된 CSV를 업로드해서 분석
#    - 1970,1980,1990,2000,2010,2015,2020,2022 선택
#    - 인구수 구간에 따라 색을 다르게 보여줌
#    - 세계 인구 대비 비율(%)도 색으로 표현
# ------------------------------
def world_population_app():
    st.title("🌍 연도별 세계인구 분석")

    st.write(
        "- CSV 파일을 업로드하면 세계 지도가 그려집니다.\n"
        "- 필요한 주요 컬럼 예시: `country`, `iso_code`, `year`, `population`"
    )

    uploaded = st.file_uploader("세계 인구 데이터 파일 업로드 (CSV)", type=["csv"])

    target_years = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

    if uploaded is None:
        st.info("먼저 CSV 파일을 업로드해 주세요.")
        return

    # 데이터 읽기
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        return

    # 컬럼 이름 유연하게 처리
    col_map = {}

    def find_col(candidates):
        for c in df.columns:
            if c.lower() in [name.lower() for name in candidates]:
                return c
        return None

    col_map["country"] = find_col(["country", "국가명", "Country"])
    col_map["iso_code"] = find_col(["iso_code", "ISO3", "iso3", "code"])
    col_map["year"] = find_col(["year", "Year", "연도"])
    col_map["population"] = find_col(["population", "Population", "인구", "pop"])

    if None in col_map.values():
        st.error(
            "필요한 컬럼을 찾지 못했습니다. 최소한 다음 컬럼이 필요합니다:\n"
            "- country / iso_code / year / population"
        )
        st.write("현재 CSV 컬럼:", list(df.columns))
        return

    # 연도 선택 드롭다운
    year = st.selectbox("연도를 선택하세요", target_years)

    # 선택한 연도만 필터링
    year_df = df[df[col_map["year"]] == year].copy()
    if year_df.empty:
        st.warning(f"{year}년에 해당하는 데이터가 없습니다.")
        return

    # 인구수 기준 구간 나누기 (절대값 기준)
    # 구간은 데이터 분포를 보며 적당히 조정 가능
    pop_col = col_map["population"]
    bins = [0, 1_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, float("inf")]
    labels = [
        "1M 미만",
        "1M ~ 10M",
        "10M ~ 50M",
        "50M ~ 100M",
        "100M ~ 500M",
        "500M 이상",
    ]
    year_df["population_bin"] = pd.cut(year_df[pop_col], bins=bins, labels=labels)

    # 세계 총인구와 비율 계산
    world_total = year_df[pop_col].sum()
    year_df["world_share"] = year_df[pop_col] / world_total * 100

    st.subheader(f"1) {year}년 국가별 인구수 구간 지도로 보기")

    fig_abs = px.choropleth(
        year_df,
        locations=col_map["iso_code"],
        color="population_bin",
        hover_name=col_map["country"],
        category_orders={"population_bin": labels},
        title=f"{year}년 국가별 인구수 구간",
    )
    st.plotly_chart(fig_abs, use_container_width=True)

    st.subheader(f"2) {year}년 세계 인구 대비 비율(%)로 보기")

    # 비율 구간도 구간화
    share_bins = [0, 0.1, 0.5, 1, 2, 5, 10, 20, float("inf")]
    share_labels = [
        "<0.1%",
        "0.1%~0.5%",
        "0.5%~1%",
        "1%~2%",
        "2%~5%",
        "5%~10%",
        "10%~20%",
        "20% 이상",
    ]
    year_df["share_bin"] = pd.cut(year_df["world_share"], bins=share_bins, labels=share_labels)

    fig_share = px.choropleth(
        year_df,
        locations=col_map["iso_code"],
        color="share_bin",
        hover_name=col_map["country"],
        hover_data={"world_share": ":.2f"},
        category_orders={"share_bin": share_labels},
        title=f"{year}년 세계 인구에서 각 국가가 차지하는 비율(%)",
    )
    st.plotly_chart(fig_share, use_container_width=True)

    st.caption("※ CSV 형식과 컬럼 이름에 따라 그래프가 다르게 보일 수 있습니다.")


# ------------------------------
# 사이드바에서 앱 선택
# ------------------------------
st.sidebar.title("활동 선택")

app_choice = st.sidebar.selectbox(
    "앱을 선택하세요",
    ("다기능 계산기", "확률 시뮬레이터", "연도별 세계인구 분석"),
)

if app_choice == "다기능 계산기":
    calculator_app()
elif app_choice == "확률 시뮬레이터":
    probability_simulator_app()
else:
    world_population_app()
