
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Student Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F5F7FB;
}
h1 {
    color: #243B64;
    font-size: 36px;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}
</style>
""", unsafe_allow_html=True)

data = {
    "Name": ["Alex", "Bella", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah"],
    "Class": ["7A", "7A", "7B", "7B", "7A", "7C", "7C", "7B"],
    "Math": [85, 90, 70, 95, 80, 75, 88, 92],
    "Science": [80, 85, 75, 90, 78, 82, 85, 95],
    "English": [90, 88, 72, 96, 85, 80, 90, 93]
}

df = pd.DataFrame(data)
subjects = ["Math", "Science", "English"]
df["Average"] = df[subjects].mean(axis=1).round(1)

st.sidebar.title("🎓 Student Portal")
menu = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Student Records", "Performance"]
)

selected_class = st.sidebar.selectbox(
    "Select Class",
    ["All Classes"] + sorted(df["Class"].unique().tolist())
)

filtered_df = df if selected_class == "All Classes" else df[df["Class"] == selected_class]

st.title("🎓 Student Performance Dashboard")
st.write("Welcome to the Student Academic Dashboard.")
st.divider()

if menu == "Overview":
    st.subheader("Academic Overview")

    total_students = len(filtered_df)
    average_score = filtered_df["Average"].mean() if total_students > 0 else 0
    passed_students = len(filtered_df[filtered_df["Average"] >= 75])
    pass_rate = passed_students / total_students * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Average Score", f"{average_score:.1f}")
    col3.metric("Pass Rate", f"{pass_rate:.1f}%")

    st.subheader("Student Performance")

    if total_students > 0:
        fig = px.bar(
            filtered_df,
            x="Name",
            y="Average",
            color="Class",
            title="Average Score by Student",
            range_y=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Student Records":
    st.subheader("Student Records")
    search = st.text_input("Search Student Name")

    result = filtered_df[
        filtered_df["Name"].str.contains(search, case=False, na=False)
    ]

    st.dataframe(result, use_container_width=True)

elif menu == "Performance":
    st.subheader("Subject Performance")

    if len(filtered_df) > 0:
        subject_average = filtered_df[subjects].mean().reset_index()
        subject_average.columns = ["Subject", "Average Score"]

        fig = px.bar(
            subject_average,
            x="Subject",
            y="Average Score",
            color="Subject",
            title="Average Score by Subject",
            range_y=[0, 100]
        )

        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Detailed Student Scores")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No student data available.")

st.divider()
st.caption("Student Dashboard | Created with Python & Streamlit")
