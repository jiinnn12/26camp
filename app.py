import streamlit as st
import numpy as np

st.set_page_config(page_title="소수점 정밀 내신 환산기", layout="centered")

st.title("📊 소수점 단위 5등급제 ➔ 9등급제 정밀 환산기")
st.caption("5등급제 내신 평균 등급을 소수점 첫째 자리까지 입력하면 9등급제로 정밀 추정합니다.")

# 1. 5등급제 등급 입력 (소수점 첫째자리 슬라이더 및 숫자인풋)
col1, col2 = st.columns([2, 1])

with col1:
    grade5_val = st.slider(
        "5등급제 평균 등급을 선택하세요:",
        min_value=1.0,
        max_value=5.0,
        value=1.4,
        step=0.1,
        format="%.1f"
    )

with col2:
    # 수치 직접 입력도 가능
    grade5_input = st.number_input(
        "직접 입력 (1.0 ~ 5.0)",
        min_value=1.0,
        max_value=5.0,
        value=float(grade5_val),
        step=0.1,
        format="%.1f"
    )

# 두 입력값 동기화
target_grade = grade5_input

# 2. 선형 보간 알고리즘 (5등급제 기준점 ➔ 9등급제 대치점)
# 5등급제 경계점 (1.0, 1.5, 2.5, 3.5, 4.5, 5.0)
x_5scale = [1.0, 1.5, 2.5, 3.5, 4.5, 5.0]

# 해당 백분율 위치에 대응하는 9등급제 연속 등급 값
y_9scale = [1.0, 1.9, 3.7, 5.3, 7.5, 9.0]

# numpy interp 함수로 소수점 연속 계산
estimated_9grade = np.interp(target_grade, x_5scale, y_9scale)

# 입력 등급에 따른 대략적인 상위 백분율 추정
pct_x = [1.0, 1.5, 2.5, 3.5, 4.5, 5.0]
pct_y = [0.0, 10.0, 34.0, 66.0, 90.0, 100.0]
estimated_pct = np.interp(target_grade, pct_x, pct_y)

st.divider()

# 3. 결과 출력
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="입력한 5등급제 성적", value=f"{target_grade:.1f} 등급")

with res_col2:
    st.metric(label="추정 9등급제 성적", value=f"{estimated_9grade:.1f} 등급")

st.success(f"💡 **5등급제 {target_grade:.1f}등급**은 상위 약 **{estimated_pct:.1f}%** 수준에 해당하며, 기존 9등급제 기준 **{estimated_9grade:.1f}등급**으로 추산됩니다.")

# 추가 가이드 박스
with st.expander("📌 환산 구간 가이드 기준 보기"):
    st.write("""
    - **1.0 ~ 1.5 미만**: 9등급제 **1.0 ~ 1.9 등급** 수준 (최상위권)
    - **1.5 ~ 2.5 미만**: 9등급제 **1.9 ~ 3.7 등급** 수준 (상위권)
    - **2.5 ~ 3.5 미만**: 9등급제 **3.7 ~ 5.3 등급** 수준 (중위권)
    - **3.5 ~ 4.5 미만**: 9등급제 **5.3 ~ 7.5 등급** 수준
    - **4.5 ~ 5.0 이하**: 9등급제 **7.5 ~ 9.0 등급** 수준
    """)
