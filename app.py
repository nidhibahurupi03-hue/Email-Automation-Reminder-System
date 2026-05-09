import streamlit as st
import pandas as pd
import plotly.express as px

from src.loader import DataLoader
from src.analytics import build_summary
from src.scheduler import save_schedule
from src.mailer import run_dry

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Luxury Email Automation",
    page_icon="📧",
    layout="wide"
)

# ---------------- LUXURY THEME ----------------
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#050505,#111111);
    color:white;
}
.card{
    background: rgba(255,215,0,0.08);
    padding:20px;
    border-radius:18px;
    border:1px solid rgba(255,215,0,0.35);
    box-shadow:0 0 25px rgba(255,215,0,0.08);
}
.big{
    font-size:26px;
    font-weight:700;
    color:gold;
}
.small{
    font-size:14px;
    color:#ddd;
}
.title{
    font-size:40px;
    font-weight:800;
    color:gold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
loader = DataLoader()
df = loader.merge_sources()
summary = build_summary(df)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>Smart Email Automation Enterprise</div>", unsafe_allow_html=True)
st.write("")

# ---------------- KPI CARDS ----------------
c1, c2, c3, c4 = st.columns(4)

cards = [
    (len(df), "Total Contacts"),
    (24, "Scheduled"),
    (18, "Sent"),
    (2, "Failed")
]

for col, (val, label) in zip([c1,c2,c3,c4], cards):
    with col:
        st.markdown(f"""
        <div class='card'>
            <div class='big'>{val}</div>
            <div class='small'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2,1])

# CONTACT TABLE
with left:
    st.subheader("Contact Database")
    st.dataframe(df, use_container_width=True)

# SCHEDULER PANEL
with right:
    st.subheader("Reminder Scheduler")

    reminder_type = st.selectbox(
        "Reminder Type",
        ["Meeting", "Payment", "Follow-up", "Webinar"]
    )

    reminder_date = st.date_input("Schedule Date")

    message = st.text_area(
        "Message",
        value="Hello Team,\nThis is your reminder notification.",
        key="msg_box"
    )

    if st.button("Schedule Reminder"):
        save_schedule(reminder_type, reminder_date, message)
        st.success("Reminder scheduled successfully 🚀")

st.write("")

# ---------------- ANALYTICS ----------------
a, b = st.columns(2)

with a:
    st.subheader("Department Analytics")

    if not summary.empty:
        fig = px.pie(
            summary,
            names="Department",
            values="Count",
            hole=0.5
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for analytics")

with b:
    st.subheader("Email Preview")

    st.markdown(f"""
    <div style='background:white;color:black;padding:20px;border-radius:15px'>
        <h3>Reminder Email</h3>
        <p>{message}</p>
        <br>
        <b>Regards,<br>Automation System</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Control Panel")

mode = st.sidebar.radio(
    "Mode",
    ["Dry Run", "Live Send (Mock)"]
)

source = st.sidebar.selectbox(
    "Data Source",
    ["API", "CSV", "Google Sheets"]
)

if st.sidebar.button("Run Automation"):
    report = run_dry(df)
    st.success(f"{len(report)} emails processed successfully 🚀")
    st.dataframe(report, use_container_width=True)

if st.sidebar.button("Generate Report"):
    st.info("Report will be saved in outputs folder")

if st.sidebar.button("View Logs"):
    st.info("Check logs/automation.log file")