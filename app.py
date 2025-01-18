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
            status = st.selectbox("Enter the status of the incident :", ["Resolved", "Unresolved"])
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
             "department":department,
             "status":status}
            with open(f"incidence/report-{report_name}-{incident_date}-{incident_time}.json".replace(":", ""),"w") as file:
                json.dump(info, file)
                st.success("Incident reported successfully!")

elif page =="View the incident":
    st.title("View information of previously logged incidents")
    count=0
    for incident_files in os.listdir("incidence"):
        reporter = incident_files.split("-")[1]
        incident = st.expander(f"Reporter : {reporter}")
        with open(f"incidence/{incident_files}") as file:
            info = json.load(file)
        incident.text_input("Reporter Name", value=info["reporter_name"], key=str(count)+info["incident_time"]+info["incident_date"], disabled=True)
        count+=1
        incident.date_input("Incident Date", value=datetime.date(year=int(info["incident_date"].split("-")[0]), month=int(info["incident_date"].split("-")[1]), day=int(info["incident_date"].split("-")[2])), key=str(count)+info["incident_date"], disabled=True)
        count+=1
        incident.text_input("Incident Time",value=info["incident_time"],key=str(count)+info["incident_time"], disabled=True)
        count+=1
        incident.text_input("Incident Type",value=info["incident_type"], key=str(count)+info["incident_type"], disabled=True)
        count+=1
        incident.text_input("Location",value=info["location"], key=str(count)+info["location"], disabled=True)
        count+=1
        incident.text_input("PVRT Label",value=info["pvrt_label"], key=str(count)+info["pvrt_label"], disabled=True)
        count+=1
        incident.text_input("Description",value=info["description"],key=str(count)+info["description"], disabled=True)
        count+=1
        incident.text_input("Department", value=info["department"], key=str(count)+info["department"], disabled=True)
        count+=1
        status = incident.text_input("Status", value=info["status"], key=str(count)+info["status"])
        count+=1

        updatebutton = st.button("Update", key=str(count))
        if updatebutton:
            info ={"reporter_name":info["reporter_name"],
             "incident_date":str(info["incident_date"]),
             "incident_time":str(info["incident_time"]),
             "location":info["location"],
             "incident_type":info["incident_type"],
             "pvrt_label":info["pvrt_label"],
             "description":info["description"],
             "department":info["department"],
             "status":status}
            with open(incident_files, "w") as file:
                json.dump(info, file)
                st.success("Incident updated successfully!")

elif page =="Analysis of the incident":
    st.title("View analytics of previously logged incidents")