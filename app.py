import streamlit as st
import plotly.express as px
import datetime
import json
import os

st.set_page_config(page_title="Work Place Incident", page_icon= "🚨", layout="wide")

st.sidebar.title("Navigation")

page=st.sidebar.radio("Go to", ["Incident Report", "View the incident", "Analysis of the incident"])

if page == "Incident Report":
    st.title("Report an incident here")
    with st.form("Report_Incident"):
        col1,col2 = st.columns(2)
        with col1:
            report_name = st.text_input("Enter your report name here :")
            incident_date = st.date_input("Enter the date of the incident here :")
            incident_time = st.time_input("Enter the time of the incident here :")
            location = st.text_input("Enter the location of the incident :")
        with col2:
            incident_type = st.selectbox("Incident Type", ["Injury", "Assault", "Verbal Abuse", "Property Damage", "Discrimination", "Stealing Credit"])
            pvrt_label = st.selectbox("Severity",["Low", "Medium", "High", "Priority"])
            description = st.text_area("Enter the details and events of the incident here :")
            department = st.text_input("Department Name :")
        submitbutton = st.form_submit_button("Submit incident")
        if submitbutton:
            info ={"reporter_name":report_name,
             "incident_date":str(incident_date),
             "incident_time":str(incident_time),
             "location":location,
             "incident_type":incident_type,
             "pvrt_label":pvrt_label,
             "description":description,
             "department":department}
            with open(f"incidence/report-{report_name}-{incident_date}-{incident_time}.json".replace(":", ""),"w") as file:
                json.dump(info, file)
                st.success("Incident reported successfully!")

elif page =="View the incident":
    st.title("View information of previously logged incidents")

elif page =="Analysis of the incident":
    st.title("View analytics of previously logged incidents")