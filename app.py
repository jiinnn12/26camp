import streamlit as st
import pandas as pd
import scipy.stats as stats

st.set_page_config(page_title="5등급 ➔ 9등급 성적 환산기", layout="centered")

st.title("📊 내신 5등급제 ➔ 9등급제 환산 시뮬레이터")
st.caption("2022 개정 교육과정 5등급제 성적을 기존 9등급제 기준으로 추정·환산합니다.")

# 1. 환산 방식 선택
mode = st.radio("환산 방식을 선택하세요:", ["단순 등급 매핑 (추정)", "Z-점수 기반 정밀 계산 (원점수/평균 필요)"])

# 9등급제 누적 비율 기준 (상한선)
scale_9 = [
    (0.04, 1),
    (0.11, 2),
    (0.23, 3),
    (0.40, 4),
    (0.60, 5),
    (0.77, 6),
    (0.89, 7),
    (0.96, 8),
    (1.00, 9)
]

def pct_to_9grade(pct):
    """백분율(0.0~1.0)을 9등급으로 변환"""
    for limit, grade in scale_9:
        if pct <= limit:
            return grade
    return 9

if mode == "단순 등급 매핑 (추정)":
    st.subheader("과목별 5등급제 성적 입력")
    
    # 5등급제 중간 백분율값 매핑
    grade5_mid_pct = {
        1: 0.05,  # 상위 0~10% (중간 5%)
        2: 0.22,  # 상위 10~34% (중간 22%)
        3: 0.50,  # 상위 34~66% (중간 50%)
        4: 0.78,  # 상위 66~90% (중간 78%)
        5: 0.95   # 상위 90~100% (중간 95%)
    }

    grade5_input = st.selectbox("5등급제 등급 선택", [1, 2, 3, 4, 5])
    
    if st.button("환산하기"):
        estimated_pct = grade5_mid_pct[grade5_input]
        grade9_result = pct_to_9grade(estimated_pct)
        
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric("입력한 5등급제 성적", f"{grade5_input} 등급")
        col2.metric("추정 9등급제 성적", f"{grade9_result} 등급")
        
        st.info(f"💡 5등급제 {grade5_input}등급의 추정 상위 백분율 약 {int(estimated_pct*100)}%를 기준으로 산출되었습니다.")

else:
    st.subheader("상세 성적 입력 (정규분포 Z-점수 활용)")
    
    col1, col2 = st.columns(2)
    with col1:
        raw_score = st.number_input("내 원점수", min_value=0.0, max_value=100.0, value=85.0)
        mean_score = st.number_input("과목 평균", min_value=0.0, max_value=100.0, value=70.0)
    with col2:
        std_dev = st.number_input("표준편차", min_value=0.1, max_value=50.0, value=15.0)
        
    if st.button("정밀 환산하기"):
        # Z-점수 계산 (X - mu) / sigma
        z_score = (raw_score - mean_score) / std_dev
        # 상위 백분율 (1 - 누적분포함수)
        top_pct = 1 - stats.norm.cdf(z_score)
        
        grade9_result = pct_to_9grade(top_pct)
        
        st.divider()
        st.metric("Z-점수 기반 추정 9등급", f"{grade9_result} 등급")
        st.write(f"- 계산된 Z-Score: **{z_score:.2f}**")
        st.write(f"- 추정 상위 백분율: **상위 {top_pct*100:.1f}%**")
