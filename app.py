import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="수면 시간 기록기", layout="centered")

st.title("🌙 수면 시간 기록 앱")

# 세션 상태 초기화
if "sleep_records" not in st.session_state:
    st.session_state["sleep_records"] = []

# 입력 폼
with st.form("sleep_form"):
    date = st.date_input("날짜", datetime.now())
    sleep_time = st.time_input("취침 시간")
    wake_time = st.time_input("기상 시간")
    quality = st.selectbox("수면의 질", ["매우 좋음", "좋음", "보통", "나쁨", "매우 나쁨"])
    memo = st.text_area("메모 및 특이사항")

    submitted = st.form_submit_button("기록 저장")

    if submitted:
        new_record = {
            "날짜": str(date),
            "취침 시간": str(sleep_time),
            "기상 시간": str(wake_time),
            "수면의 질": quality,
            "메모": memo
        }
        st.session_state["sleep_records"].append(new_record)
        st.success("수면 기록이 저장되었습니다!")

# 사이드바 데이터 관리 (엑셀 내보내기 기능 탑재)
with st.sidebar:
    st.subheader("⚙️ 설정 및 데이터 관리")
    
    if st.button("모든 데이터 초기화", type="secondary"):
        st.session_state["sleep_records"] = []
        st.success("초기화되었습니다.")
        st.rerun()
        
    st.divider()
    
    if st.session_state["sleep_records"]:
        df = pd.DataFrame(st.session_state["sleep_records"])
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        
        st.download_button(
            label="📊 엑셀로 내보내기",
            data=csv_data,
            file_name="수면기록_전체.csv",
            mime="text/csv",
            help="수면 데이터를 CSV 파일로 다운로드합니다."
        )
    else:
        st.info("다운로드할 데이터가 없습니다.")
