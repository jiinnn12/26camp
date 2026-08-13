import streamlit as st
import numpy as np
from openai import OpenAI

st.set_page_config(page_title="Upstage AI 기반 대입 진학 시뮬레이터", layout="centered")

st.title("🎯 Upstage AI 성적 환산 & 대입 진학 컨설턴트")
st.caption("5등급제 내신 성적을 정밀 환산하고, Upstage Solar AI가 목표 대학 진학 전략을 분석해 드립니다.")

# 1. Upstage API 클라이언트 세팅
api_key = st.secrets.get("UPSTAGE_API_KEY", "")

# 2. 사용자 입력 폼
st.subheader("📝 내 성적 및 목표 대학 입력")

# 신분 선택 기능 추가 (재학생 vs 자퇴생)
student_type = st.radio(
    "현재 학생 신분을 선택하세요:",
    ["고등학교 재학생", "자퇴생 / 검정고시 준비생"],
    horizontal=True
)

col1, col2 = st.columns(2)

with col1:
    current_grade = st.number_input(
        "현재 5등급제 평균 등급 (소수점 입력)",
        min_value=1.0,
        max_value=5.0,
        value=2.2,
        step=0.1,
        format="%.1f"
    )

with col2:
    target_univ = st.text_input(
        "목표 대학 및 학과",
        value="고려대학교 컴퓨터공학과"
    )

user_context = st.text_area(
    "추가 상황 (선택 사항)",
    placeholder="예: 일반고 재학 중이고 정시보다 수시 학종 위주로 고민 중입니다. 또는 주요 취약 과목 등에 대해 적어주세요.",
    height=80
)

# 3. 파이썬 기반 수학적 정밀 환산 계산 (선형 보간법)
x_5scale = [1.0, 1.5, 2.5, 3.5, 4.5, 5.0]
y_9scale = [1.0, 1.9, 3.7, 5.3, 7.5, 9.0]
pct_scale = [0.0, 10.0, 34.0, 66.0, 90.0, 100.0]

estimated_9grade = float(np.interp(current_grade, x_5scale, y_9scale))
estimated_pct = float(np.interp(current_grade, x_5scale, pct_scale))

st.divider()

# 4. 환산 결과 기본 표시
st.subheader("📊 성적 환산 결과")
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="입력한 5등급제 성적", value=f"{current_grade:.1f} 등급")

with res_col2:
    st.metric(label="추정 9등급제 성적", value=f"{estimated_9grade:.1f} 등급")

st.info(f"💡 상위 약 **{estimated_pct:.1f}%** 수준이며, 기존 9등급제 기준 **{estimated_9grade:.1f}등급**으로 추산됩니다.")

st.divider()

# 5. Upstage Solar AI 리포트 생성 버튼
if st.button("🤖 Upstage AI 진학 컨설팅 리포트 생성"):
    if not api_key:
        st.error("⚠️ Streamlit Secrets에 `UPSTAGE_API_KEY`가 설정되지 않았습니다. Settings -> Secrets를 확인해 주세요.")
    else:
        with st.spinner("Solar AI가 2022 개정 교육과정 및 입시 데이터를 분석 중입니다..."):
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.upstage.ai/v1/solar"
                )
                
                # 학생 신분에 따른 가이드라인 분기 처리
                if student_type == "고등학교 재학생":
                    type_guideline = """
                    - 학생은 현재 고등학교에 재학 중인 일반 학생입니다. 절대 자퇴생으로 가정하지 마세요.
                    - 학교 내신 등급 유지 및 향상 전략, 학교 생활기록부(세특, 창의적 체험활동 등) 관리 팁, 수시(교과/학종) 및 정시 준비 방향성을 제시해 주세요.
                    """
                else:
                    type_guideline = """
                    - 학생은 자퇴생 또는 검정고시를 준비 중인 학교 밖 청소년입니다.
                    - 검정고시 고득점 전략, 청소년 생활기록부 대체서식 작성법, 수능 최저학력기준 대비 및 정시 전략을 위주로 제시해 주세요.
                    """

                prompt = f"""
                너는 2022 개정 교육과정 및 대한민국 대입 제도에 정통한 전문적이고 따뜻한 대입 입시 컨설턴트야.

                [학생 데이터]
                - 학생 신분: {student_type}
                - 현재 5등급제 성적: {current_grade:.1f}등급
                - 기존 9등급제 추정 성적: {estimated_9grade:.1f}등급 (상위 {estimated_pct:.1f}%)
                - 목표 대학 및 학과: {target_univ}
                - 학생 추가 설명: {user_context if user_context else '특별한 추가 설명 없음'}

                [신분별 맞춤 가이드라인]
                {type_guideline}

                [요청 사항]
                1. **성적 위치 분석**: 현재 환산 성적({current_grade:.1f}등급 / 9등급 기준 {estimated_9grade:.1f}등급)이 {target_univ} 진학 관점에서 가지는 위치와 입시적 의미를 설명해 줘.
                2. **목표 등급 가이드**: {target_univ} 합격 안정권에 들기 위해 5등급제/9등급제 기준으로 대략 어느 정도의 등급대가 필요한지 짚어주고, 현재 성적과의 격차를 설명해 줘.
                3. **맞춤형 실행 전략 (2가지)**: 학생의 신분({student_type})과 2022 개정 교육과정 특성을 고려하여 성적 격차를 극복하고 입시에서 유리해질 수 있는 실질적인 전략 2가지를 제시해 줘.
                4. **응원 메시지**: 따뜻하고 격려하는 한마디로 마무리해 줘.

                [작성 톤앤매너]
                - 마크다운(Markdown) 형식을 활용해 보기 쉽게 작성할 것.
                - 친절하고 전문적인 어조를 유지할 것.
                """

                response = client.chat.completions.create(
                    model="solar-pro",
                    messages=[
                        {"role": "system", "content": "너는 대한민국 최상위 대입 입시 컨설턴트 솔라(Solar)야."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                result_text = response.choices[0].message.content

                st.subheader("✨ Solar AI 맞춤형 진학 리포트")
                st.markdown(result_text)

            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")
