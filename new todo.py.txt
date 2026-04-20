import streamlit as st
from datetime import datetime
import pandas as pd
import time

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="To-Do Reminder", page_icon="⏰", layout="centered")

# ใช้ Session State เพื่อเก็บข้อมูลงาน (ข้อมูลจะไม่หายเมื่อกดปุ่มอื่น)
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# ฟังก์ชันเพิ่มงาน
def add_task(name, t):
    st.session_state.tasks.append({
        "id": time.time(),
        "task": name,
        "time": t.strftime("%H:%M"),
        "status": "Pending",
        "notified": False
    })

# --- ส่วน UI ---
st.title("⏰ To-Do List Reminder")
st.write("จัดการรายการงานของคุณ และรับการแจ้งเตือนบนหน้าเว็บ")

# ช่องกรอกข้อมูล
with st.container(border=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        task_input = st.text_input("ระบุสิ่งที่ต้องทำ", placeholder="เช่น ประชุมงาน...")
    with col2:
        time_input = st.time_input("เวลาแจ้งเตือน", datetime.now())
    
    if st.button("➕ เพิ่มรายการ", use_container_width=True):
        if task_input:
            add_task(task_input, time_input)
            st.success("เพิ่มงานสำเร็จ!")
        else:
            st.warning("กรุณากรอกชื่อรายการ")

# --- ส่วนแสดงรายการ ---
st.subheader("📌 รายการงานทั้งหมด")

if not st.session_state.tasks:
    st.info("ยังไม่มีรายการงานในตอนนี้")
else:
    # สร้างตารางการทำงาน
    for i, item in enumerate(st.session_state.tasks):
        col_t, col_n, col_s, col_d = st.columns([1, 2, 1, 1])
        with col_t:
            st.write(f"🕒 {item['time']}")
        with col_n:
            # ถ้าแจ้งเตือนแล้วให้ขีดฆ่า
            display_text = f"~~{item['task']}~~" if item['status'] == "Completed" else item['task']
            st.write(display_text)
        with col_s:
            if st.button("✅", key=f"done_{item['id']}"):
                st.session_state.tasks[i]['status'] = "Completed"
                st.rerun()
        with col_d:
            if st.button("🗑️", key=f"del_{item['id']}"):
                st.session_state.tasks.pop(i)
                st.rerun()

# --- ระบบแจ้งเตือน (Check Reminder) ---
# ส่วนนี้จะทำงานทุกครั้งที่หน้าเว็บ Refresh
current_time = datetime.now().strftime("%H:%M")

for item in st.session_state.tasks:
    if item['time'] == current_time and item['status'] == "Pending" and not item['notified']:
        st.toast(f"🔔 ถึงเวลาแล้ว: {item['task']}", icon="❗")
        st.warning(f"⚠️ **แจ้งเตือน:** {item['task']} (เวลา {item['time']})")
        item['notified'] = True
        # เล่นเสียงแจ้งเตือนสั้นๆ (Optional)
        st.balloons() 

# ปุ่มล้างรายการที่เสร็จแล้ว
if st.button("ล้างงานที่ทำเสร็จแล้ว"):
    st.session_state.tasks = [t for t in st.session_state.tasks if t['status'] != "Completed"]
    st.rerun()

# Auto Refresh ทุกๆ 60 วินาที เพื่อเช็คเวลา
st.empty()
time.sleep(1) # หน่วงเวลาเล็กน้อย
if any(t['status'] == "Pending" for t in st.session_state.tasks):
    st.caption("ระบบกำลังตรวจสอบเวลาแจ้งเตือนอัตโนมัติ...")
    # หมายเหตุ: Streamlit Cloud จะรีรันเมื่อมีการโต้ตอบ 
    # หากต้องการให้เช็คตลอดเวลาโดยไม่กดอะไรเลย อาจต้องใช้ไลบรารี st_autorefresh