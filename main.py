import math
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="다기능 계산기", page_icon="🧮")

st.title("🧮 다기능 계산기 웹앱")
st.write(
    "깃허브 & 스트림릿으로 만든 간단한 계산기입니다.\n"
    "아래에서 원하는 연산을 선택하고 값을 입력해 보세요."
)

# 연산 선택
operation = st.radio(
    "원하는 연산을 선택하세요:",
    (
        "사칙연산 (+, -, ×, ÷)",
        "모듈러 연산 (a % b)",
        "지수 연산 (a^b)",
        "로그 연산 (log₍base₎(value))",
        "다항함수 그래프",
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
    # log는 0보다 커야 해서 아주 작은 양수부터 입력 가능하게 설정
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
                # log_base(value) = ln(value) / ln(base)
                result = math.log(value) / math.log(base)
                st.success(f"결과: log₍{base}₎({value}) = {result}")
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")

# 다항함수 그래프
elif operation == "다항함수 그래프":
    st.subheader("다항함수 그래프 그리기")

    st.markdown(
        """
        - 계수는 **최고차항부터** 차례대로 입력하세요.  
        - 예: `1, -3, 2` → \( f(x) = 1x^2 - 3x + 2 \)
        """
    )

    coeff_text = st.text_input(
        "계수 목록 (쉼표로 구분해서 입력)",
        value="1, -3, 2",
    )

    x_min = st.number_input("x 최소값", value=-10.0)
    x_max = st.number_input("x 최대값", value=10.0)
    num_points = st.slider("그래프를 위한 x 샘플 개수", 50, 1000, 400, 50)

    if st.button("그래프 그리기"):
        # x 범위 체크
        if x_min >= x_max:
            st.error("x 최소값은 최대값보다 작아야 합니다.")
        else:
            try:
                # 계수 파싱
                coeffs = [
                    float(c.strip())
                    for c in coeff_text.split(",")
                    if c.strip() != ""
                ]
                if not coeffs:
                    st.error("최소 하나 이상의 계수를 입력해야 합니다.")
                else:
                    # 다항식 객체 생성
                    p = np.poly1d(coeffs)

                    # x, y 값 계산
                    xs = np.linspace(x_min, x_max, num_points)
                    ys = p(xs)

                    # 다항식 식 보여주기
                    degree = len(coeffs) - 1
                    terms = []
                    for i, c in enumerate(coeffs):
                        power = degree - i
                        if abs(c) < 1e-12:
                            continue
                        if power == 0:
                            term = f"{c}"
                        elif power == 1:
                            term = f"{c}x"
                        else:
                            term = f"{c}x^{power}"
                        terms.append(term)
                    poly_str = " + ".join(terms).replace("+ -", "- ")

                    st.write(f"**f(x) = {poly_str}**")

                    # 그래프 그리기
                    df = pd.DataFrame({"x": xs, "f(x)": ys})
                    st.line_chart(df, x="x", y="f(x)")
            except ValueError:
                st.error("계수는 숫자로만 입력해야 합니다. (예: 1, -3, 2)")
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
