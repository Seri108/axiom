import math
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
    b = st.number_input("지_

