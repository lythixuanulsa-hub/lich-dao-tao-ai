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

# Sidebar Navigation
st.sidebar.title("🛠 Quản lý Đào tạo")
menu = st.sidebar.radio(
    "Chọn chức năng:",
    ["🏠 Trang chủ & Lịch", "📝 Đăng ký Đào tạo", "🔐 Quản trị viên"]
)

# List of sessions
SESSIONS = ["Buổi 1: Lý thuyết", "Buổi 2: Thực hành cơ bản", "Buổi 3: Thực hành nâng cao", "Buổi 4: Chia sẻ bài tập"]

# --- HOME PAGE ---
if menu == "🏠 Trang chủ & Lịch":
    st.markdown('<div class="main-header"><h1>Lịch đăng ký đào tạo AI năm 2026</h1><p>Hệ thống hiển thị lịch trực quan cho các bộ phận</p></div>', unsafe_allow_html=True)
    
    registrations = db.get_registrations()
    
    # Month Selection
    current_month = st.radio("Chọn tháng xem lịch:", [5, 6], horizontal=True, format_func=lambda x: f"Tháng {x}")
    year = 2026
    
    st.markdown(f"### 🗓 Lịch trình Tháng {current_month} / {year}")
    
    # CALENDAR RENDER LOGIC
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, current_month)
    
    weekdays = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
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
                            is_morning = "Sáng" in row['TimeSlot']
                            marker_class = "event-morning" if is_morning else "event-afternoon"
                            day_html += f'<div class="event-marker {marker_class}"><b>{row["Department"]}</b><br/>⏱ {row["TimeSlot"]}<br/>👥 {row["Attendees"]} người</div>'
                    
                    day_html += '</div>'
                    st.markdown(day_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('🔵 **Xanh**: Ca Sáng | 🟠 **Cam**: Ca Chiều | ⬛ **Xám**: Ngày nghỉ (Chủ Nhật)')

# --- REGISTRATION PAGE ---
elif menu == "📝 Đăng ký Đào tạo":
    st.markdown("## 📝 Biểu mẫu Đăng ký Đào tạo")
    st.warning("⚠️ **Lưu ý:** Các bộ phận hãy đăng ký theo một khung giờ và thứ cố định hàng tuần.")
    
    min_date = date(2026, 5, 1)
    max_date = date(2026, 6, 30)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("registration_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                dept_options = ["Kỹ thuật", "Sản xuất", "QC", "RD", "Kinh doanh", "Kế toán", "Kho", "Khác (tự nhập)"]
                dept_selection = st.selectbox("Bộ phận:", dept_options)
                
                final_dept = dept_selection
                if dept_selection == "Khác (tự nhập)":
                    final_dept = st.text_input("Nhập tên bộ phận khác:", placeholder="Ví dụ: Bảo vệ, Tạp vụ...")
                
                team_name = st.text_input("Team (tự điền):", placeholder="Ví dụ: Kỹ thuật sản phẩm...")
                session_type = st.selectbox("3. Buổi đào tạo:", SESSIONS)
                attendees = st.number_input("6. Số lượng người nhận đào tạo (dự kiến):", min_value=1, max_value=200, value=5)
            with col2:
                training_date = st.date_input("4. Ngày đào tạo (Tháng 5 & 6):", value=min_date, min_value=min_date, max_value=max_date)
                st.write("5. Khung giờ:")
                c1, c2 = st.columns([1, 2])
                with c1:
                    period = st.radio("Buổi:", ["Sáng", "Chiều"], horizontal=True)
                with c2:
                    exact_time = st.text_input("Giờ cụ thể:", placeholder="Ví dụ: 09:00...")
                final_timeslot = f"{period} {exact_time}"
                
            submitted = st.form_submit_button("Xác nhận Đăng ký")
            if submitted:
                if team_name and exact_time and final_dept:
                    db.save_registration(final_dept, team_name, session_type, "", training_date, final_timeslot, attendees)
                    st.success(f"✅ Đã lưu đăng ký cho {final_dept} thành công!")
                else:
                    st.error("⚠️ Vui lòng điền đủ thông tin.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- ADMIN PAGE ---
elif menu == "🔐 Quản trị viên":
    st.markdown("## 🔐 Khu vực Quản trị viên")
    
    password = st.text_input("Nhập mật khẩu để truy cập:", type="password")
    
    if password == "admin123":
        st.success("Xác thực thành công!")
        
        tab_list, tab_manage = st.tabs(["📊 Danh sách Tổng hợp", "🗑️ Quản lý & Xóa"])
        
        registrations = db.get_registrations()
        
        with tab_list:
            st.markdown("### 📊 Toàn bộ danh sách đăng ký")
            if not registrations.empty:
                display_df = registrations[['Date', 'TimeSlot', 'Department', 'Team', 'Session', 'Attendees']].copy()
                display_df.columns = ['Ngày', 'Giờ', 'Bộ phận', 'Team', 'Nội dung', 'Số người']
                st.dataframe(display_df.sort_values(by=['Ngày', 'Giờ']), use_container_width=True, hide_index=True)
                
                csv = registrations.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 Tải xuống toàn bộ (CSV)", csv, "lich_dao_tao_tong_hop.csv", "text/csv")
            else:
                st.info("Chưa có dữ liệu.")
                
        with tab_manage:
            st.markdown("### 🗑️ Xóa bản đăng ký")
            if not registrations.empty:
                for index, row in registrations.iterrows():
                    with st.expander(f"📌 {row['Date']} - {row['Department']} ({row['Team']})"):
                        st.write(f"**Giờ:** {row['TimeSlot']} | **Số người:** {row['Attendees']}")
                        st.write(f"**Nội dung:** {row['Session']}")
                        if st.button(f"Xóa đăng ký này", key=f"del_{index}"):
                            if db.delete_registration(index):
                                st.rerun()
            else:
                st.info("Không có dữ liệu để quản lý.")
    elif password:
        st.error("Mật khẩu không chính xác.")
    else:
        st.info("Vui lòng nhập mật khẩu quản trị để xem danh sách tổng hợp và thực hiện xóa.")
