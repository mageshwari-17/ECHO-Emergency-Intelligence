
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

from agents import run_echo_agents
from weather import get_weather
from map_agent import show_emergency_map

st.set_page_config(
    page_title="ECHO Emergency Intelligence",
    page_icon="🚨",
    layout="wide"
)

# =====================================================
# CSS - FIX WHITE BOX + INVISIBLE WORDINGS
# =====================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: #0B1120 !important;
    color: #F8FAFC !important;
}

/* MAIN CONTENT */
[data-testid="stMain"] {
    background: #0B1120 !important;
}

/* TEXT VISIBILITY */
.stApp p,
.stApp label,
.stApp li,
.stMarkdown p,
.stMarkdown li {
    color: #E5E7EB !important;
}

/* HEADINGS */
h1 {
    color: #FF4545 !important;
}

h2 {
    color: #FF7043 !important;
}

h3, h4 {
    color: #FFB347 !important;
}

/* REMOVE WHITE CONTAINERS */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background-color: transparent !important;
}

/* CARDS AND CONTAINERS */
[data-testid="stContainer"] {
    background: #111C2E !important;
    border: 1px solid #29374C !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 2px solid #EF4444 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
}

/* METRICS */
[data-testid="stMetric"] {
    background: #172337 !important;
    border: 1px solid #EF4444 !important;
    border-radius: 14px !important;
    padding: 18px !important;
}

[data-testid="stMetricLabel"] {
    color: #FFB4A2 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* BUTTONS */
.stButton > button {
    background: #DC2626 !important;
    color: white !important;
    border: 1px solid #F97316 !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    min-height: 42px !important;
}

.stButton > button:hover {
    background: #F97316 !important;
    color: white !important;
}

/* TEXT INPUT */
.stTextInput input {
    background: #172337 !important;
    color: #FFFFFF !important;
    border: 1px solid #475569 !important;
}

/* TEXT AREA */
.stTextArea textarea {
    background: #172337 !important;
    color: #FFFFFF !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    caret-color: white !important;
}

/* INPUT PLACEHOLDER */
input::placeholder,
textarea::placeholder {
    color: #AAB4C5 !important;
    opacity: 1 !important;
}

/* SELECTBOX */
[data-baseweb="select"] > div {
    background: #172337 !important;
    color: white !important;
    border-color: #475569 !important;
}

/* DROPDOWN MENU */
[data-baseweb="popover"] {
    background: #172337 !important;
}

[data-baseweb="menu"] {
    background: #172337 !important;
}

[role="option"] {
    background: #172337 !important;
    color: #FFFFFF !important;
}

[role="option"]:hover {
    background: #334155 !important;
}

/* CHECKBOX */
[data-testid="stCheckbox"] label {
    color: #FFFFFF !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    background: #172337 !important;
    border-radius: 10px !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background: #172337 !important;
}

/* TABS */
button[data-baseweb="tab"] {
    color: #FFFFFF !important;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div {
    background: #EF4444 !important;
}

/* DIVIDER */
hr {
    border-color: #334155 !important;
}

/* FOOTER */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "tasks": [],
    "logs": [],
    "incidents": [],
    "analysis": None,
    "last_description": "",
    "last_location": "Chennai",
    "last_actions": [],
    "analysis_count": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# HELPERS
# =====================================================

def add_log(message):
    st.session_state.logs.insert(
        0,
        f"{datetime.now().strftime('%H:%M:%S')} - {message}"
    )


def get_value(keys, default=None):
    result = st.session_state.analysis or {}

    for key in keys:
        if key in result and result[key] is not None:
            return result[key]

    return default


def get_risk_score():
    try:
        return int(get_value(["risk_score", "score"], 50))
    except (ValueError, TypeError):
        return 50


def get_risk_level():
    return str(
        get_value(["risk_level", "severity", "priority"], "MEDIUM")
    ).upper()


def get_incident_type():
    return str(
        get_value(["incident_type", "type", "category"], "Emergency")
    )


def get_team():
    return str(
        get_value(
            ["recommended_team", "team", "response_team"],
            "Emergency Response Team"
        )
    )


def get_actions():
    actions = get_value(
        ["recommended_actions", "actions", "response_actions"],
        []
    )

    if isinstance(actions, str):
        return [actions]

    return actions if isinstance(actions, list) else []


def analyze_incident(description, location):

    st.session_state.last_description = description
    st.session_state.last_location = location

    add_log("Incident analysis started")

    try:
        result = run_echo_agents(description)

        if not isinstance(result, dict):
            result = {}

        result.setdefault("incident_type", "Emergency")
        result.setdefault("risk_level", "MEDIUM")
        result.setdefault("risk_score", 50)
        result.setdefault("recommended_team", "Emergency Response Team")
        result.setdefault("recommended_actions", [])

        st.session_state.analysis = result
        st.session_state.last_actions = get_actions()
        st.session_state.analysis_count += 1

        st.session_state.incidents.append({
            "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "location": location,
            "incident_type": get_incident_type(),
            "risk_level": get_risk_level(),
            "risk_score": get_risk_score(),
            "description": description
        })

        add_log("Incident analysis completed")
        return True

    except Exception as e:
        st.error(f"Analysis error: {e}")
        add_log(f"Analysis failed: {e}")
        return False


def create_task():

    task = {
        "id": "ECHO-" + uuid.uuid4().hex[:8].upper(),
        "incident_type": get_incident_type(),
        "location": st.session_state.last_location,
        "status": "OPEN",
        "priority": get_risk_level(),
        "team": get_team(),
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "actions": [
            {"action": str(a), "completed": False}
            for a in get_actions()
        ]
    }

    st.session_state.tasks.append(task)
    add_log(f"Task created: {task['id']}")

    return task


# =====================================================
# HEADER
# =====================================================

st.markdown("# 🚨 ECHO")
st.markdown("### Emergency Intelligence Platform")

st.markdown(
    "AI-powered emergency monitoring, incident analysis, and response coordination."
)

st.caption("Hackathon prototype | Not connected to official emergency services")

st.divider()


# =====================================================
# NAVIGATION
# =====================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Command Center",
        "Incident Analyzer",
        "Response Tasks",
        "Advanced Analytics",
        "Agent Activity"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 🟢 System Status")
st.sidebar.success("Prototype Operational")
st.sidebar.metric("Incidents Analyzed", st.session_state.analysis_count)
st.sidebar.metric("Response Tasks", len(st.session_state.tasks))


# =====================================================
# 1. COMMAND CENTER
# =====================================================

if page == "Command Center":

    st.header("🚨 ECHO Command Center")

    total = len(st.session_state.incidents)

    high = sum(
        i["risk_level"] == "HIGH"
        for i in st.session_state.incidents
    )

    active = sum(
        t["status"] != "COMPLETED"
        for t in st.session_state.tasks
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Incidents", total)
    c2.metric("High Risk", high)
    c3.metric("Response Tasks", len(st.session_state.tasks))
    c4.metric("Active Tasks", active)

    st.divider()

    st.subheader("📊 Emergency Risk Overview")

    if st.session_state.incidents:

        df = pd.DataFrame(st.session_state.incidents)

        st.bar_chart(df.set_index("time")["risk_score"])

        st.subheader("Recent Incidents")

        st.dataframe(
            df[["time", "location", "incident_type", "risk_level", "risk_score"]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No incidents analyzed yet.")

    st.divider()

    st.subheader("🧪 Emergency Simulation")

    simulation = st.selectbox(
        "Select Emergency",
        [
            "Fire Emergency",
            "Flood Emergency",
            "Road Accident",
            "Medical Emergency",
            "Building Collapse"
        ]
    )

    location = st.selectbox(
        "Location",
        ["Chennai", "Coimbatore", "Madurai", "Vellore"]
    )

    descriptions = {
        "Fire Emergency":
            "A major fire accident occurred in a residential building. "
            "People may be trapped inside and smoke is spreading.",

        "Flood Emergency":
            "Heavy rainfall has caused flooding in low-lying areas. "
            "People are stranded and roads are flooded.",

        "Road Accident":
            "A major road accident involving multiple vehicles. "
            "People are injured and traffic is blocked.",

        "Medical Emergency":
            "Multiple people require immediate medical assistance.",

        "Building Collapse":
            "A building has collapsed. People may be trapped under debris."
    }

    if st.button("🚨 Run Emergency Simulation"):

        success = analyze_incident(
            descriptions[simulation],
            location
        )

        if success:
            st.success("Simulation completed!")
            st.rerun()


# =====================================================
# 2. INCIDENT ANALYZER
# =====================================================

elif page == "Incident Analyzer":

    st.header("🔍 Incident Analyzer")

    description = st.text_area(
        "Incident Description",
        placeholder="Describe the emergency situation...",
        height=180
    )

    location = st.selectbox(
        "Location",
        [
            "Chennai",
            "Coimbatore",
            "Madurai",
            "Vellore",
            "Tiruvallur",
            "Salem",
            "Trichy",
            "Other"
        ]
    )

    if st.button("🧠 Analyze Incident"):

        if description.strip():

            success = analyze_incident(description, location)

            if success:
                st.success("Analysis completed!")
                st.rerun()

        else:
            st.warning("Please enter incident details.")

    if st.session_state.analysis:

        st.divider()
        st.subheader("📋 Analysis Results")

        c1, c2, c3 = st.columns(3)

        c1.metric("Incident Type", get_incident_type())
        c2.metric("Risk Score", f"{get_risk_score()} / 100")
        c3.metric("Risk Level", get_risk_level())

        st.progress(max(0, min(100, get_risk_score())) / 100)

        st.subheader("👨‍🚒 Recommended Team")
        st.info(get_team())

        st.subheader("📝 Recommended Actions")

        for index, action in enumerate(get_actions(), 1):
            st.markdown(f"**{index}.** {action}")

        st.divider()

        st.subheader("🗺️ Emergency Map")

        try:
            show_emergency_map(
                st.session_state.last_location,
                get_risk_level(),
                get_incident_type()
            )
        except Exception as e:
            st.warning(f"Map unavailable: {e}")

        st.subheader("🌦️ Weather")

        try:
            weather = get_weather(st.session_state.last_location)

            if weather:
                st.write(weather)
            else:
                st.info("Weather data unavailable.")

        except Exception:
            st.info("Weather API unavailable.")

        st.divider()

        if st.button("➕ Create Response Task"):

            task = create_task()

            st.success(f"Created: {task['id']}")
            st.rerun()


# =====================================================
# 3. RESPONSE TASKS
# =====================================================

elif page == "Response Tasks":

    st.header("📋 Emergency Response Task Management")

    tasks = st.session_state.tasks

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Tasks", len(tasks))
    c2.metric("Open Tasks", sum(t["status"] == "OPEN" for t in tasks))
    c3.metric("Completed", sum(t["status"] == "COMPLETED" for t in tasks))

    st.divider()

    if not tasks:
        st.info("No response tasks available.")

    for index, task in enumerate(tasks):

        with st.container(border=True):

            st.subheader(f"🚨 {task['id']}")

            st.write(f"Incident: {task['incident_type']}")
            st.write(f"Location: {task['location']}")
            st.write(f"Team: {task['team']}")
            st.write(f"Priority: {task['priority']}")

            status_options = ["OPEN", "IN PROGRESS", "COMPLETED"]

            selected = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(task["status"]),
                key=f"status_{task['id']}"
            )

            task["status"] = selected

            st.subheader("Action Checklist")

            for ai, action in enumerate(task["actions"]):

                action["completed"] = st.checkbox(
                    action["action"],
                    value=action["completed"],
                    key=f"action_{task['id']}_{ai}"
                )

            completed = sum(a["completed"] for a in task["actions"])
            total_actions = len(task["actions"])

            progress = completed / total_actions if total_actions else 0

            st.progress(progress)
            st.write(f"Progress: {completed} / {total_actions}")

            if total_actions and completed == total_actions:
                task["status"] = "COMPLETED"

            if st.button("🗑️ Delete Task", key=f"delete_{task['id']}"):

                st.session_state.tasks.pop(index)
                add_log(f"Deleted task: {task['id']}")
                st.rerun()


# =====================================================
# 4. ADVANCED ANALYTICS
# =====================================================

elif page == "Advanced Analytics":

    st.header("📊 Advanced Analytics")

    incidents = st.session_state.incidents
    tasks = st.session_state.tasks

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Incidents", len(incidents))
    c2.metric("High Risk", sum(i["risk_level"] == "HIGH" for i in incidents))
    c3.metric("Tasks", len(tasks))
    c4.metric("Completed Tasks", sum(t["status"] == "COMPLETED" for t in tasks))

    st.divider()

    if incidents:

        df = pd.DataFrame(incidents)

        st.subheader("Risk Score Analysis")
        st.bar_chart(df.set_index("time")["risk_score"])

        st.subheader("Risk Level Distribution")
        st.bar_chart(df["risk_level"].value_counts())

        st.subheader("Location Analysis")
        st.bar_chart(df["location"].value_counts())

        st.subheader("Incident Types")
        st.bar_chart(df["incident_type"].value_counts())

        st.subheader("Incident History")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Download Incident CSV",
            df.to_csv(index=False),
            "echo_incidents.csv",
            "text/csv"
        )

    else:
        st.info("Analyze incidents to view analytics.")

    st.divider()

    st.subheader("Task Analytics")

    if tasks:

        task_df = pd.DataFrame([
            {
                "Task ID": t["id"],
                "Incident": t["incident_type"],
                "Location": t["location"],
                "Team": t["team"],
                "Status": t["status"],
                "Priority": t["priority"]
            }
            for t in tasks
        ])

        st.dataframe(task_df, use_container_width=True, hide_index=True)

        st.bar_chart(task_df["Status"].value_counts())

        st.download_button(
            "⬇️ Download Task CSV",
            task_df.to_csv(index=False),
            "echo_tasks.csv",
            "text/csv"
        )

    else:
        st.info("No response tasks created yet.")


# =====================================================
# 5. AGENT ACTIVITY
# =====================================================

elif page == "Agent Activity":

    st.header("🤖 ECHO Agent Activity")

    c1, c2, c3 = st.columns(3)

    c1.metric("Analysis Runs", st.session_state.analysis_count)
    c2.metric("Activity Logs", len(st.session_state.logs))
    c3.metric("Response Tasks", len(st.session_state.tasks))

    st.divider()

    st.subheader("🧠 AI Agents")

    agents = [
        "Incident Analysis Agent",
        "Risk Assessment Agent",
        "Weather Intelligence Agent",
        "Emergency Response Agent",
        "Task Monitoring Agent"
    ]

    for agent in agents:

        st.markdown(
            f"""
            <div style="
                background:#172337;
                padding:15px;
                border:1px solid #EF4444;
                border-radius:12px;
                margin-bottom:10px;
            ">
                <h4 style="color:#FFB347 !important;">
                    🤖 {agent}
                </h4>
                <p style="color:#FFFFFF !important;">
                    🟢 Status: Operational
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("📜 Activity Logs")

    if st.session_state.logs:

        for log in st.session_state.logs:

            st.markdown(
                f"""
                <div style="
                    background:#172337;
                    border-left:4px solid #FF4545;
                    padding:10px;
                    margin-bottom:8px;
                    border-radius:6px;
                ">
                    <p style="color:#FFFFFF !important;">{log}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No activity logs yet.")

    if st.button("🧹 Clear Activity Logs"):
        st.session_state.logs.clear()
        st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; background:#111C2E; padding:20px; border-radius:12px;">
    <h3 style="color:#FF4545 !important;">🚨 ECHO Emergency Intelligence</h3>
    <p style="color:#FFFFFF !important;">
        AI-powered emergency analysis and response coordination
    </p>
    <p style="color:#94A3B8 !important;">
        Hackathon Prototype | Demo Only | Not connected to official emergency services
    </p>
</div>
""", unsafe_allow_html=True)
