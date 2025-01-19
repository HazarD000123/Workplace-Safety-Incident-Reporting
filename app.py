import streamlit as st
import plotly.express as px
import datetime
import json
import os
import pandas as pd

st.set_page_config(page_title="Work Place Incident", page_icon= "🚨", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

def load_credentials():
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
            return json.load(f)
    return {"users": []}

def validate_login(username, password):
    credentials = load_credentials()
    
    for user in credentials['users']:
        if user['username'] == username and user['password'] == password:
            return True, user['role']
    return False, None

if not st.session_state.logged_in:
    st.title("🔐Log in ")
    with st.form("login_form"):
        user_name = st.text_input("Enter username :")
        user_pwd = st.text_input("Enter password:", type="password")
        loginbutton = st.form_submit_button(label="Login")
        if loginbutton:
            is_valid, role = validate_login(user_name, user_pwd)
            if is_valid:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.user_name = user_name
                st.success("Log in successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")
else:
    st.sidebar.markdown(f"Current User : {st.session_state.user_name}")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_role = None 
        st.session_state.user_name = None
        st.rerun()

    if st.session_state.user_role == "admin":
        st.sidebar.title("Navigation")
        page=st.sidebar.radio("Go to", ["Incident Report", "View the incident", "Analysis of the incident"])
    else:
        page="Incident Report"

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
            with open(f"incidence/{incident_files}") as file:
                info = json.load(file)
            incident = st.expander(f"Reporter : {reporter}       Current Status : {info["status"]}")
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
            status = incident.selectbox("Status", ["Resolved", "Unresolved"], key=str(count)+info["status"])
            count+=1
            resolvers_comment = incident.text_input("Enter comment here :", key=str(count)+"resolvers_comment")
            count+=1

            updatebutton = incident.button("Update", key=str(count))
            if updatebutton:
                info ={"reporter_name":info["reporter_name"],
                "incident_date":str(info["incident_date"]),
                "incident_time":str(info["incident_time"]),
                "location":info["location"],
                "incident_type":info["incident_type"],
                "pvrt_label":info["pvrt_label"],
                "description":info["description"],
                "department":info["department"],
                "status":status,
                "resolvers_comment":resolvers_comment}
                with open(f"incidence/{incident_files}", "w") as file:
                    json.dump(info, file)
                    incident.success("Incident updated successfully!")


    elif page =="Analysis of the incident":
        st.title("View analytics of previously logged incidents")

        analysisdict = {"department":[],
                        "incident_type":[],
                        "incident_date":[],
                        "pvrt_label":[],
                        "status":[]}

        for incident_files in os.listdir("incidence"):
            with open(f"incidence/{incident_files}") as file:
                info = json.load(file)

            analysisdict["department"].append(info["department"])
            analysisdict["incident_type"].append(info["incident_type"])
            analysisdict["pvrt_label"].append(info["pvrt_label"])
            analysisdict["incident_date"].append(info["incident_date"])
            analysisdict["status"].append(info["status"])

        analysisdf = pd.DataFrame(analysisdict)
        
        fig1 = px.line(analysisdf.groupby("incident_date").size().reset_index(name="count"), x="incident_date", y="count")
        st.plotly_chart(fig1, use_container_width=True)
        col1,col2 = st.columns(2)
        fig2 = px.pie(analysisdf, names="incident_type", title="Incident by Type")
        col1.plotly_chart(fig2)
        fig3 = px.pie(analysisdf, names="pvrt_label", title="Incident by Severity")
        col2.plotly_chart(fig3)

        fig4 = px.bar(analysisdf["department"].value_counts(), title="Incident by Department")
        st.plotly_chart(fig4, use_container_width=True)

        col3,col4,col5= st.columns(3)
        col3.metric("Total incidence :", len(analysisdf))
        col4.metric("Open incidence :", len(analysisdf[analysisdf["status"]== "Unresolved"]))
        col5.metric("Critical incidence :", len(analysisdf[analysisdf["pvrt_label"]== "Priority"]))