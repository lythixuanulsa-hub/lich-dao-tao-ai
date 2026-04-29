import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import database as db
import os
import calendar

# Page configuration
st.set_page_config(
    page_title="Lịch đăng ký đào tạo AI năm 2026",
    page_icon="📅",
    layout="wide"
)

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# Initialize database
db.init_db()

# Language Dictionary
LANG_DICT = {
    "Tiếng Việt": {
        "sidebar_title": "🛠 Quản lý Đào tạo / 교육 관리",
        "lang_select": "🌐 Ngôn ngữ / 언어 선택:",
        "menu_label": "Chức năng / 메뉴 chọn:",
        "menu_home": "🏠 Trang chủ & Lịch / 홈 및 일정",
        "menu_reg": "📝 Đăng ký Đào tạo / 교육 신청",
        "menu_admin": "🔐 Quản trị viên / 관리자",
        "home_title": "Lịch đăng ký đào tạo AI năm 2026",
        "home_subtitle": "2026년 AI 교육 신청 일정",
        "select_month": "Chọn tháng xem lịch / 일정 조회 월 선택:",
        "month_label": "Tháng / 월",
        "calendar_title": "🗓 Lịch trình Tháng / 일정표 -",
        "weekdays": ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
        "legend": "🔵 **Xanh**: Ca Sáng | 🟠 **Cam**: Ca Chiều | ⬛ **Xám**: Ngày nghỉ (Chủ Nhật)",
        "reg_title": "📝 Biểu mẫu Đăng ký Đào tạo / 교육 신청서",
        "reg_note": "⚠️ **Lưu ý:** Các bộ phận hãy đăng ký theo một khung giờ và thứ cố định hàng tuần. / 매주 고정된 요일과 시간대를 선택하여 신청해 주세요.",
        "dept": "Bộ phận / 부서:",
        "team": "Team (tự điền) / 팀명:",
        "session": "3. Buổi đào tạo / 교육 회차:",
        "attendees": "6. Số lượng người nhận đào tạo / 교육 인원:",
        "date": "4. Ngày đào tạo (Tháng 5, 6, 7) / 교육 날짜:",
        "timeslot": "5. Khung giờ / 시간대:",
        "period": "Buổi / 구분:",
        "morning": "Sáng / 오전",
        "afternoon": "Chiều / 오후",
        "time_exact": "Giờ cụ thể / 상세 시간:",
        "submit": "Xác nhận Đăng ký / 신청 확인",
        "success": "✅ Đã lưu đăng ký thành công! / 신청이 성공적으로 저장되었습니다!",
        "error": "⚠️ Vui lòng điền đủ thông tin. / 모든 정보를 입력해 주세요.",
        "admin_title": "🔐 Khu vực Quản trị viên / 관리자 전용",
        "password": "Nhập mật khẩu / 비밀번호를 입력하세요:",
        "auth_success": "Xác thực thành công! / 인증 성공!",
        "tab_list": "📊 Danh sách Tổng hợp / 전체 목록",
        "tab_manage": "🗑️ Quản lý & Xóa / 관리 및 삭제",
        "list_title": "📊 Toàn bộ danh sách đăng ký / 전체 신청 목록",
        "download": "📥 Tải xuống (CSV) / 다운로드",
        "no_data": "Chưa có dữ liệu. / 데이터가 없습니다.",
        "delete_title": "🗑️ Xóa bản đăng ký / 신청 삭제",
        "delete_btn": "Xóa / 삭제",
        "placeholder_team": "Ví dụ: Kỹ thuật... / 예: 기술팀...",
        "placeholder_time": "Ví dụ: 09:00...",
        "placeholder_dept": "Ví dụ: Bảo vệ... / 예: 보안...",
        "people": "người / 명",
        "sessions": ["Buổi 1: Lý thuyết / 1회차: 이론", "Buổi 2: Thực hành cơ bản / 2회차: 기본 실습", "Buổi 3: Thực hành nâng cao / 3회차: 심화 실습", "Buổi 4: Chia sẻ bài tập / 4회차: 과제 공유"]
    },
    "한국어": {
        "sidebar_title": "🛠 Quản lý Đào tạo / 교육 관리",
        "lang_select": "🌐 Ngôn ngữ / 언어 선택:",
        "menu_label": "Chức năng / 메뉴 chọn:",
        "menu_home": "🏠 Trang chủ & Lịch / 홈 및 일정",
        "menu_reg": "📝 Đăng ký Đào tạo / 교육 신청",
        "menu_admin": "🔐 Quản trị viên / 관리자",
        "home_title": "2026년 AI 교육 신청 일정",
        "home_subtitle": "Lịch đăng ký đào tạo AI năm 2026",
        "select_month": "Chọn tháng xem lịch / 일정 조회 월 선택:",
        "month_label": "Tháng / 월",
        "calendar_title": "🗓 Lịch trình Tháng / 일정표 -",
        "weekdays": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        "legend": "🔵 **파란색**: 오전 | 🟠 **주황색**: 오후 | ⬛ **회색**: 휴일 (일요일)",
        "reg_title": "📝 교육 신청서 / Biểu mẫu Đăng ký",
        "reg_note": "⚠️ **참고:** 매주 고정된 요일과 시간대를 선택하여 신청해 주세요. / Lưu ý: Đăng ký theo khung giờ cố định.",
        "dept": "부서 / Bộ phận:",
        "team": "팀명 / Team (tự điền):",
        "session": "3. 교육 회차 / Buổi đào tạo:",
        "attendees": "6. 교육 인원 / Số lượng người:",
        "date": "4. 교육 날짜 (5, 6, 7월) / Ngày đào tạo:",
        "timeslot": "5. 시간대 / Khung giờ:",
        "period": "구분 / Buổi:",
        "morning": "오전 / Sáng",
        "afternoon": "오후 / Chiều",
        "time_exact": "상세 시간 / Giờ cụ thể:",
        "submit": "신청 확인 / Xác nhận",
        "success": "✅ 신청이 성공적으로 저장되었습니다! / Lưu thành công!",
        "error": "⚠️ 모든 정보를 입력해 주세요. / Vui lòng điền đủ thông tin.",
        "admin_title": "🔐 관리자 전용 / Quản trị viên",
        "password": "비밀번호를 입력하세요 / Nhập mật khẩu:",
        "auth_success": "인증 성공! / Xác thực thành công!",
        "tab_list": "📊 전체 목록 / Danh sách",
        "tab_manage": "🗑️ 관리 및 삭제 / Quản lý",
        "list_title": "📊 전체 신청 목록 / Toàn bộ danh sách",
        "download": "📥 전체 다운로드 (CSV) / Tải xuống",
        "no_data": "데이터가 없습니다. / Chưa có dữ liệu.",
        "delete_title": "🗑️ 신청 삭제 / Xóa bản đăng ký",
        "delete_btn": "삭제 / Xóa",
        "placeholder_team": "예: 기술팀... / Ví dụ: Kỹ thuật...",
        "placeholder_time": "예: 09:00...",
        "placeholder_dept": "예: 보안... / Ví dụ: Bảo vệ...",
        "people": "명 / người",
        "sessions": ["1회차: 이론 / Buổi 1: Lý thuyết", "2회차: 기본 실습 / Buổi 2: Thực hành cơ bản", "3회차: 심화 실습 / Buổi 3: Thực hành nâng cao", "4회차: 과제 공유 / Buổi 4: Chia sẻ bài tập"]
    }
}

# Initial language check
if "lang" not in st.session_state:
    st.session_state.lang = "Tiếng Việt"

# 1. Language Selection in Sidebar
lang_choice = st.sidebar.radio(
    "🌐 Ngôn ngữ / 언어 chọn:",
    ["Tiếng Việt", "한국어"],
    index=0 if st.session_state.lang == "Tiếng Việt" else 1,
    key="lang_radio"
)

# Update session state and rerun if language changed
if lang_choice != st.session_state.lang:
    st.session_state.lang = lang_choice
    st.rerun()

lang = st.session_state.lang
T = LANG_DICT[lang]

# Sidebar Navigation
st.sidebar.title(T["sidebar_title"])
menu = st.sidebar.radio(
    T["menu_label"],
    [T["menu_home"], T["menu_reg"], T["menu_admin"]],
    key="menu_radio"
)

# --- HOME PAGE ---
if menu == T["menu_home"]:
    st.markdown(f'<div class="main-header"><h1>{T["home_title"]}</h1><p>{T["home_subtitle"]}</p></div>', unsafe_allow_html=True)
    
    registrations = db.get_registrations()
    
    # Month Selection
    current_month = st.radio(T["select_month"], [5, 6, 7], horizontal=True, format_func=lambda x: f"{T['month_label']} {x}")
    year = 2026
    
    st.markdown(f"### {T['calendar_title']} {current_month} / {year}")
    
    # CALENDAR RENDER LOGIC
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, current_month)
    
    weekdays = T["weekdays"]
    header_cols = st.columns(7)
    for i, day in enumerate(weekdays):
        header_cols[i].markdown(f'<div style="background:#4b6cb7; color:white; text-align:center; padding:10px; border-radius:5px; font-weight:bold;">{day}</div>', unsafe_allow_html=True)
    
    if not registrations.empty:
        registrations['Date'] = pd.to_datetime(registrations['Date'])
    
    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                is_sunday = (i == 6)
                day_class = "calendar-day sunday-day" if is_sunday else "calendar-day"
                
                if day == 0:
                    st.markdown(f'<div class="{day_class} other-month"></div>', unsafe_allow_html=True)
                else:
                    target_date = date(year, current_month, day)
                    day_html = f'<div class="{day_class}"><span class="day-number">{day}</span>'
                    
                    if not registrations.empty:
                        day_regs = registrations[registrations['Date'].dt.date == target_date]
                        for _, row in day_regs.iterrows():
                            # Handle session translations if stored in Vietnamese but viewing in Korean
                            display_dept = row['Department']
                            display_timeslot = row['TimeSlot']
                            # Map morning/afternoon in display
                            display_timeslot = display_timeslot.replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"])
                            
                            is_morning = "Sáng" in row['TimeSlot']
                            marker_class = "event-morning" if is_morning else "event-afternoon"
                            day_html += f'<div class="event-marker {marker_class}"><b>{display_dept}</b><br/>⏱ {display_timeslot}<br/>👥 {row["Attendees"]} {T["people"]}</div>'
                    
                    day_html += '</div>'
                    st.markdown(day_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(T["legend"])

# --- REGISTRATION PAGE ---
elif menu == T["menu_reg"]:
    st.markdown(f"## {T['reg_title']}")
    st.warning(T["reg_note"])
    
    min_date = date(2026, 5, 1)
    max_date = date(2026, 7, 31)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("registration_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                # Keep fixed dept options but translate if needed? 
                # Let's keep them as is or translate the common ones
                dept_options = ["Kỹ thuật", "Sản xuất", "QC", "RD", "Kinh doanh", "Kế toán", "Kho", "Khác (tự nhập)"]
                if lang == "한국어":
                    dept_options_kr = ["기술", "생산", "QC", "RD", "영업", "회계", "창고", "기타 (직접 입력)"]
                    dept_selection = st.selectbox(T["dept"], dept_options_kr)
                    # Map back to VN for DB or keep KR? User might want consistent DB.
                    # For now, let's keep the DB consistent in Vietnamese or use what's selected.
                    # Usually better to store raw input.
                else:
                    dept_selection = st.selectbox(T["dept"], dept_options)
                
                final_dept = dept_selection
                if "Khác" in dept_selection or "기타" in dept_selection:
                    final_dept = st.text_input(T["placeholder_dept"], placeholder=T["placeholder_dept"])
                
                team_name = st.text_input(T["team"], placeholder=T["placeholder_team"])
                session_type = st.selectbox(T["session"], T["sessions"])
                attendees = st.number_input(T["attendees"], min_value=1, max_value=200, value=5)
            with col2:
                training_date = st.date_input(T["date"], value=min_date, min_value=min_date, max_value=max_date)
                st.write(T["timeslot"])
                c1, c2 = st.columns([1, 2])
                with c1:
                    period = st.radio(T["period"], [T["morning"], T["afternoon"]], horizontal=True)
                with c2:
                    exact_time = st.text_input(T["time_exact"], placeholder=T["placeholder_time"])
                
                # Standardize storage to Vietnamese for morning/afternoon to maintain DB consistency
                storage_period = "Sáng" if period == T["morning"] else "Chiều"
                final_timeslot = f"{storage_period} {exact_time}"
                
            submitted = st.form_submit_button(T["submit"])
            if submitted:
                if team_name and exact_time and final_dept:
                    # We store the session name as selected (might be KR or VN)
                    db.save_registration(final_dept, team_name, session_type, "", training_date, final_timeslot, attendees)
                    st.success(T["success"])
                else:
                    st.error(T["error"])
        st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN PAGE ---
elif menu == T["menu_admin"]:
    st.markdown(f"## {T['admin_title']}")
    
    password = st.text_input(T["password"], type="password")
    
    if password == "admin123":
        st.success(T["auth_success"])
        
        tab_list, tab_manage = st.tabs([T["tab_list"], T["tab_manage"]])
        
        registrations = db.get_registrations()
        
        with tab_list:
            st.markdown(f"### {T['list_title']}")
            if not registrations.empty:
                display_df = registrations[['Date', 'TimeSlot', 'Department', 'Team', 'Session', 'Attendees']].copy()
                # Localize timeslot in display
                display_df['TimeSlot'] = display_df['TimeSlot'].apply(lambda x: x.replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"]))
                
                display_df.columns = [
                    'Ngày' if lang == "Tiếng Việt" else '날짜', 
                    'Giờ' if lang == "Tiếng Việt" else '시간', 
                    'Bộ phận' if lang == "Tiếng Việt" else '부서', 
                    'Team', 
                    'Nội dung' if lang == "Tiếng Việt" else '교육 내용', 
                    'Số người' if lang == "Tiếng Việt" else '인원'
                ]
                st.dataframe(display_df.sort_values(by=display_df.columns[0]), use_container_width=True, hide_index=True)
                
                csv = registrations.to_csv(index=False).encode('utf-8-sig')
                st.download_button(T["download"], csv, "lich_dao_tao_tong_hop.csv", "text/csv")
            else:
                st.info(T["no_data"])
                
        with tab_manage:
            st.markdown(f"### {T['delete_title']}")
            if not registrations.empty:
                for index, row in registrations.iterrows():
                    display_time = row['TimeSlot'].replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"])
                    with st.expander(f"📌 {row['Date']} - {row['Department']} ({row['Team']})"):
                        st.write(f"**{T['timeslot']}** {display_time} | **{T['attendees']}** {row['Attendees']} {T['people']}")
                        st.write(f"**{T['session']}** {row['Session']}")
                        if st.button(T["delete_btn"], key=f"del_{index}"):
                            if db.delete_registration(index):
                                st.rerun()
            else:
                st.info(T["no_data"])
    elif password:
        st.error("Mật khẩu không chính xác." if lang == "Tiếng Việt" else "비밀번호가 틀렸습니다.")
    else:
        st.info(T["password"] if lang == "Tiếng Việt" else "관리자 메뉴를 이용하려면 비밀번호를 입력하세요.")
