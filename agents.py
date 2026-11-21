
# ==========================================================
# ECHO - SMART INCIDENT INTELLIGENCE ENGINE
# ==========================================================

import re


# ----------------------------------------------------------
# 1. SMART INCIDENT DETECTION AGENT
# ----------------------------------------------------------

def detection_agent(incident):

    text = incident.lower()

    categories = {
        "Flood / Weather Emergency": [
            "flood", "flooding", "rain", "heavy rain",
            "storm", "water level", "overflow",
            "water rising", "waterlogging"
        ],

        "Fire Emergency": [
            "fire", "smoke", "burn", "explosion",
            "blaze", "flames", "fire accident"
        ],

        "Road Accident": [
            "accident", "crash", "collision",
            "vehicle", "road accident", "car accident",
            "bike accident", "truck accident"
        ],

        "Medical Emergency": [
            "unconscious", "medical", "injury",
            "collapsed", "heart attack", "bleeding",
            "breathing difficulty", "chest pain",
            "fainted", "seizure"
        ]
    }

    scores = {}

    for category, keywords in categories.items():

        matches = [
            keyword for keyword in keywords
            if keyword in text
        ]

        scores[category] = len(matches)

    detected_type = max(
        scores,
        key=scores.get
    )

    if scores[detected_type] == 0:
        detected_type = "General Emergency"

    return detected_type


# ----------------------------------------------------------
# 2. RISK ASSESSMENT AGENT
# ----------------------------------------------------------

def risk_agent(incident):

    text = incident.lower()

    score = 20
    reasons = []

    critical_indicators = [
        "trapped",
        "stranded",
        "unconscious",
        "drowning",
        "collapsed",
        "people stuck",
        "unable to escape",
        "missing people",
        "children trapped"
    ]

    high_danger_indicators = [
        "severe",
        "critical",
        "life threatening",
        "multiple people",
        "heavy damage",
        "rising water",
        "large fire",
        "spreading fire",
        "major accident"
    ]

    emergency_indicators = [
        "flood",
        "flooding",
        "fire",
        "accident",
        "storm",
        "explosion",
        "crash",
        "injury",
        "bleeding"
    ]

    # Critical danger indicators
    for keyword in critical_indicators:

        if keyword in text:

            score += 15

            reasons.append(
                "Critical threat detected: " + keyword
            )

    # High danger indicators
    for keyword in high_danger_indicators:

        if keyword in text:

            score += 15

            reasons.append(
                "High danger condition: " + keyword
            )

    # Emergency event indicators
    for keyword in emergency_indicators:

        if keyword in text:

            score += 10

            reasons.append(
                "Emergency event detected: " + keyword
            )

    # Additional context-based risk
    if any(word in text for word in [
        "several people", "many people",
        "crowd", "public"
    ]):

        score += 10

        reasons.append(
            "Multiple people may be affected"
        )

    if any(word in text for word in [
        "night", "dark", "no visibility"
    ]):

        score += 5

        reasons.append(
            "Low visibility may increase response difficulty"
        )

    score = min(score, 100)

    # Risk classification
    if score >= 80:

        level = "CRITICAL"

    elif score >= 60:

        level = "HIGH"

    elif score >= 40:

        level = "MEDIUM"

    else:

        level = "LOW"

    if not reasons:

        reasons.append(
            "No major risk indicators detected. "
            "Continue monitoring."
        )

    return score, level, reasons


# ----------------------------------------------------------
# 3. RESPONSE PLANNING AGENT
# ----------------------------------------------------------

def response_agent(incident_type, risk_level):

    response_plans = {

        "Flood / Weather Emergency": [
            "Move away from flooded areas",
            "Avoid flooded roads",
            "Stay away from electrical equipment and floodwater",
            "Identify safe elevated locations",
            "Request rescue assistance if people are trapped"
        ],

        "Fire Emergency": [
            "Evacuate the affected area if safe",
            "Avoid smoke inhalation",
            "Do not use elevators",
            "Contact fire and rescue services",
            "Keep away from the burning structure"
        ],

        "Road Accident": [
            "Secure the accident area if safe",
            "Contact emergency medical services",
            "Avoid moving seriously injured persons",
            "Keep traffic away from the incident",
            "Provide location details to responders"
        ],

        "Medical Emergency": [
            "Contact emergency medical services",
            "Check responsiveness if safe",
            "Follow emergency dispatcher instructions",
            "Keep the person safe until help arrives",
            "Provide accurate location information"
        ],

        "General Emergency": [
            "Assess the situation",
            "Identify immediate hazards",
            "Contact appropriate emergency services",
            "Keep people away from danger",
            "Monitor the incident"
        ]
    }

    actions = response_plans.get(
        incident_type,
        response_plans["General Emergency"]
    ).copy()

    if risk_level == "CRITICAL":

        actions.insert(
            0,
            "URGENT: Seek immediate professional emergency assistance"
        )

    elif risk_level == "HIGH":

        actions.insert(
            0,
            "PRIORITY: Escalate for urgent assessment"
        )

    return actions


# ----------------------------------------------------------
# 4. AI DECISION EXPLANATION AGENT
# ----------------------------------------------------------

def explanation_agent(
    incident,
    incident_type,
    risk_level,
    reasons
):

    explanations = {

        "CRITICAL": (
            "Multiple severe risk indicators were identified. "
            "Immediate professional emergency assessment is recommended."
        ),

        "HIGH": (
            "Significant risk indicators were detected. "
            "Urgent assessment and response planning are recommended."
        ),

        "MEDIUM": (
            "Potential danger indicators were detected. "
            "Monitoring and preventive action are recommended."
        ),

        "LOW": (
            "The incident currently has a lower detected risk. "
            "Continue monitoring and reassess if the situation changes."
        )
    }

    return {
        "explanation": explanations.get(
            risk_level,
            explanations["LOW"]
        ),
        "risk_reasons": reasons
    }


# ----------------------------------------------------------
# 5. PRIORITY DECISION AGENT
# ----------------------------------------------------------

def priority_agent(risk_level, incident_type):

    priority_table = {

        "CRITICAL": {
            "priority": "P1 - IMMEDIATE",
            "response_time": "Immediate assessment",
            "team": "Emergency Rescue Team"
        },

        "HIGH": {
            "priority": "P2 - URGENT",
            "response_time": "Urgent assessment",
            "team": "Rapid Response Team"
        },

        "MEDIUM": {
            "priority": "P3 - MODERATE",
            "response_time": "Monitoring and assessment",
            "team": "Field Assessment Team"
        },

        "LOW": {
            "priority": "P4 - NORMAL",
            "response_time": "Routine monitoring",
            "team": "Local Monitoring Team"
        }
    }

    decision = priority_table.get(
        risk_level,
        priority_table["LOW"]
    ).copy()

    team_mapping = {

        "Flood / Weather Emergency":
            "Flood Rescue & Disaster Response Team",

        "Fire Emergency":
            "Fire & Rescue Team",

        "Road Accident":
            "Road Safety & Medical Team",

        "Medical Emergency":
            "Medical Response Team",

        "General Emergency":
            "Emergency Assessment Team"
    }

    decision["team"] = team_mapping.get(
        incident_type,
        "Emergency Assessment Team"
    )

    return decision


# ----------------------------------------------------------
# 6. MASTER ECHO ORCHESTRATOR
# ----------------------------------------------------------

def run_echo_agents(incident):

    # Agent 1
    incident_type = detection_agent(incident)

    # Agent 2
    score, risk_level, reasons = risk_agent(incident)

    # Agent 3
    actions = response_agent(
        incident_type,
        risk_level
    )

    # Agent 4
    explanation = explanation_agent(
        incident,
        incident_type,
        risk_level,
        reasons
    )

    # Agent 5
    priority = priority_agent(
        risk_level,
        incident_type
    )

    # Final intelligence output
    result = {

        "incident_type": incident_type,

        "risk_score": score,

        "risk_level": risk_level,

        "actions": actions,

        "explanation": explanation["explanation"],

        "reasons": explanation["risk_reasons"],

        "priority": priority["priority"],

        "response_time": priority["response_time"],

        "recommended_team": priority["team"]
    }

    return result
