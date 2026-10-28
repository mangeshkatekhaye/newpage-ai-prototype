# app.py - Part B: Medical Inquiry Handling Interactive Prototype (Fully Audited Demo)
# Run with: py -m streamlit run app.py

import streamlit as st
import datetime

st.set_page_config(
    page_title="Medical Inquiry Triage - Compliant AI Prototype",
    page_icon="🩺",
    layout="wide"
)

# Enterprise UI Styling
st.markdown("""
<style>
    .main-header { font-size: 24px; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .sub-header { font-size: 13px; color: #64748b; margin-bottom: 16px; }
    .demo-banner { background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 10px 14px; border-radius: 6px; font-size: 12px; color: #1e40af; margin-bottom: 18px; }
    .card-box { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 16px; border-radius: 8px; margin-bottom: 14px; }
    .citation-box { background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px; border-radius: 4px; font-size: 13px; }
    .warning-box { background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 12px; border-radius: 4px; font-size: 13px; }
    .abstain-box { background-color: #fffbebfb; border-left: 4px solid #d97706; padding: 12px; border-radius: 4px; font-size: 13px; }
    .badge { background:#e2e8f0; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:600; color:#334155; }
</style>
""", unsafe_allow_html=True)

# Synthetic Non-Clinical MLR Content Repository (Medical Education & Administrative Guidelines)
SYNTHETIC_VAULT_DB = {
    "DOC-DEMO-US-001": {
        "title": "[SYNTHETIC DEMO DATA] DemoMed-X Medical Education Grant & Symposia Guidelines",
        "mlr_code": "US-DEMO-2025-09142",
        "approval_status": "APPROVED",
        "country_scope": "US",
        "expiration_date": "2027-12-31",
        "program_scope": "HCP Educational Grants & Speaking Eligibility",
        "content_chunk": "Section 3.1 Eligibility Criteria: Licensed HCPs in active oncology practice are eligible to request educational grants for independent symposia. Requests exceeding $5,000 or involving non-US attendees require additional regional compliance committee review."
    },
    "DOC-DEMO-US-002": {
        "title": "[SYNTHETIC DEMO DATA] DemoMed-X Educational Guidelines (Archived 2023)",
        "mlr_code": "US-DEMO-2023-00119",
        "approval_status": "EXPIRED",
        "country_scope": "US",
        "expiration_date": "2024-05-01",
        "program_scope": "HCP Educational Grants",
        "content_chunk": "Archived Section 3.1: Educational grant cap was previously set at $2,500 without committee review."
    }
}

# Synthetic Test Scenarios (Explicitly Non-Clinical & Unmistakably Synthetic Identities)
INQUIRY_SCENARIOS = {
    "Scenario 1: Verified Administrative Inquiry (Education Grant)": {
        "hcp_name": "[SYNTHETIC-HCP] Dr. Alex Morgan, MD",
        "hcp_npi": "SYN-NPI-999001",
        "channel": "HCP Digital Portal",
        "country": "US",
        "inquiry_text": "At what grant amount or attendee scope is additional compliance committee review required?",
        "intent_type": "IN_LABEL_MATCH",
        "doc_id": "DOC-DEMO-US-001"
    },
    "Scenario 2: Out-of-Bounds Request (Unapproved Non-US Scope)": {
        "hcp_name": "[SYNTHETIC-HCP] Dr. Taylor Reed, MD",
        "hcp_npi": "SYN-NPI-999002",
        "channel": "Contact Center Escalation",
        "country": "US",
        "inquiry_text": "Can a US educational grant be awarded to host an unaccredited student workshop in an unauthorized overseas jurisdiction?",
        "intent_type": "OFF_LABEL_HALT",
        "doc_id": None
    },
    "Scenario 3: Expired Guidance Document (System Abstention)": {
        "hcp_name": "[SYNTHETIC-HCP] Dr. Jordan Lee, MD",
        "hcp_npi": "SYN-NPI-999003",
        "channel": "HCP Digital Portal",
        "country": "US",
        "inquiry_text": "Requesting confirmation on legacy $2,500 threshold limit for local educational grant approvals.",
        "intent_type": "EXPIRED_SOURCE_ABSTAIN",
        "doc_id": "DOC-DEMO-US-002"
    }
}

# Dynamic Eligibility Verification Function
def evaluate_source_eligibility(doc_metadata, target_country):
    if not doc_metadata:
        return False, "No source document retrieved for this query intent."
    
    today = datetime.date.today()
    exp_date = datetime.datetime.strptime(doc_metadata["expiration_date"], "%Y-%m-%d").date()
    
    if doc_metadata["approval_status"] != "APPROVED":
        return False, f"MLR status is '{doc_metadata['approval_status']}' (Requires APPROVED)."
    if exp_date < today:
        return False, f"MLR clearance expired on {exp_date}."
    if doc_metadata["country_scope"] != target_country:
        return False, f"Country mismatch (Doc: {doc_metadata['country_scope']} vs Inquiry: {target_country})."
    
    return True, "Source fully eligible and active."

# Audit Session State Initializer
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# Sidebar Navigation & Utilities
st.sidebar.title("Newpage AI Prototype")
st.sidebar.caption("Idea 1: Medical Inquiry Triage")

selected_scenario_key = st.sidebar.selectbox("Select Test Scenario:", list(INQUIRY_SCENARIOS.keys()))
scenario = INQUIRY_SCENARIOS[selected_scenario_key]

st.sidebar.markdown("---")
if st.sidebar.button("Clear Session Audit Ledger", use_container_width=True):
    st.session_state.audit_log = []
    st.rerun()

# Header & Architecture Disclosure Banner
st.markdown('<div class="main-header">Medical Information Request (MIR) Triage Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Demonstrating Dynamic Source Eligibility, Safety Guardrails, and Enforced HITL Governance</div>', unsafe_allow_html=True)

st.markdown("""
<div class="demo-banner">
    <strong>📌 Architecture Note for Reviewers:</strong> This prototype is a <em>deterministic scenario simulation</em> designed to demonstrate UI flows, compliance gates, and human-in-the-loop review controls. Production could use an event-driven AWS architecture (for example, EventBridge, LangGraph orchestration, OpenSearch vector indexing, and persistent, access-controlled audit logging).
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

# Left Column: Incoming Query & Dynamic Rule Evaluation
with col1:
    st.subheader("1. Inbound HCP Inquiry Details")
    st.markdown(f"""
    <div class="card-box">
        <p><strong>HCP Identifier:</strong> {scenario['hcp_name']} <span class="badge">{scenario['hcp_npi']}</span></p>
        <p><strong>Channel & Region:</strong> {scenario['channel']} | Scope: <code>{scenario['country']}</code></p>
        <p><strong>Timestamp:</strong> {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        <hr style="margin: 8px 0;">
        <p><strong>Inquiry Message:</strong></p>
        <blockquote style="background: #fff; padding: 8px; border-left: 3px solid #0284c7; font-style: italic; margin: 0;">
            "{scenario['inquiry_text']}"
        </blockquote>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("2. Agentic Retrieval & Safety Rules")
    
    if scenario['intent_type'] == "OFF_LABEL_HALT":
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin: 0; color: #991b1b;">⚠️ OUT-OF-BOUNDS / POLICY TRIGGER</h4>
            <p style="margin-top: 4px;">Intent detected: <strong>Unauthorized jurisdictional scope or unaccredited program</strong>.</p>
            <p style="margin-bottom: 0;"><strong>System Decision:</strong> Automated drafting halted. Ticket routed to Medical Affairs Escalation Queue.</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        doc = SYNTHETIC_VAULT_DB[scenario['doc_id']]
        is_valid, check_reason = evaluate_source_eligibility(doc, scenario['country'])
        
        if not is_valid:
            st.markdown(f"""
            <div class="abstain-box">
                <h4 style="margin: 0; color: #b45309;">⚠️ SYSTEM ABSTENTION: INELIGIBLE SOURCE</h4>
                <p style="margin-top: 4px;">Retrieved document <code>{doc['mlr_code']}</code> failed eligibility check.</p>
                <p style="margin-bottom: 0;"><strong>Reason:</strong> {check_reason}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="citation-box">
                <h4 style="margin: 0; color: #166534;">✅ SOURCE ELIGIBLE & IN-SCOPE VERIFIED</h4>
                <p style="margin-top: 4px;">Scope: <em>{doc['program_scope']}</em>.</p>
                <p style="margin-bottom: 0;"><strong>Active MLR Code:</strong> <code>{doc['mlr_code']}</code> | Rule Engine Check: <strong>PASS</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📄 View Verified MLR Document Source (Synthetic Data)", expanded=True):
                st.write(f"**Document Title:** {doc['title']}")
                st.write(f"**MLR Code:** `{doc['mlr_code']}` | **Status:** {doc['approval_status']}")
                st.write(f"**Active Expiry:** {doc['expiration_date']} | **Region:** {doc['country_scope']}")
                st.write(f"**Exact Source Chunk:** _{doc['content_chunk']}_")

# Right Column: Human-in-the-Loop Reviewer Workspace
with col2:
    st.subheader("3. Medical Reviewer HITL Workspace")
    
    current_doc = SYNTHETIC_VAULT_DB.get(scenario['doc_id']) if scenario['doc_id'] else None
    is_eligible = False
    if current_doc:
        is_eligible, _ = evaluate_source_eligibility(current_doc, scenario['country'])
    
    if scenario['intent_type'] == "OFF_LABEL_HALT" or not is_eligible:
        st.warning("Automated draft response generation is disabled for this inquiry state.")
        msl_note = st.text_area("Escalation Documentation Note:", f"Inquiry flagged due to {scenario['intent_type']}. Escalating to Medical Compliance lead for manual evaluation.", height=120)
        
        if st.button("Escalate to Medical Compliance Specialist Queue", type="primary"):
            st.session_state.audit_log.append({
                "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S UTC'),
                "hcp_id": scenario['hcp_name'],
                "action": "ESCALATED_TO_SPECIALIST",
                "eligibility_result": "FAIL / BLOCKED",
                "mlr_code": current_doc['mlr_code'] if current_doc else "NONE",
                "reviewer_note": msl_note
            })
            st.success("Case escalated. Complete audit entry logged in session state.")

    else:
        default_draft = f"""Dear {scenario['hcp_name']},

Thank you for contacting Medical Information regarding DemoMed-X educational grant policies.

In response to your inquiry regarding independent educational symposium grants:
Per Section 3.1 of the approved guidelines, licensed HCPs in active oncology practice are eligible to request educational grants. Requests exceeding $5,000 or involving non-US attendees require additional regional compliance committee review [Ref: {current_doc['mlr_code']}].

Please consult the complete Educational Grant Policy for further details.

Sincerely,
Medical Information Services"""

        user_draft = st.text_area("Draft Response (Simulated; Editable):", default_draft, height=200)
        
        st.info("Simulation only: approving records a demo audit event. No message is sent to an HCP and no live CRM integration is called.")

        st.markdown("##### Enforced Mandatory Sign-Off Checks")
        chk1 = st.checkbox("I verify the cited MLR code matches active approved policy guidance", value=False)
        chk2 = st.checkbox("I confirm no out-of-scope or unapproved claims are present in this draft", value=False)
        
        can_approve = chk1 and chk2
        
        c_app, c_rej = st.columns(2)
        with c_app:
            if st.button("Approve & Record Release", type="primary", disabled=not can_approve, use_container_width=True):
                st.session_state.audit_log.append({
                    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S UTC'),
                    "hcp_id": scenario['hcp_name'],
                    "action": "APPROVED_RELEASE",
                    "eligibility_result": "PASS",
                    "mlr_code": current_doc['mlr_code'],
                    "reviewer_note": "Sign-off completed with mandatory compliance checks verified."
                })
                st.balloons()
                st.success("Response approved! Simulated Veeva CRM interaction audit entry logged.")
        with c_rej:
            if st.button("Reject & Request Redraft", use_container_width=True):
                st.session_state.audit_log.append({
                    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S UTC'),
                    "hcp_id": scenario['hcp_name'],
                    "action": "REJECTED_REDRAFT",
                    "eligibility_result": "FAIL / REJECTED_BY_REVIEWER",
                    "mlr_code": current_doc['mlr_code'],
                    "reviewer_note": "Reviewer rejected draft for redrafting."
                })
                st.error("Draft rejected and logged to evaluation feedback loop.")

# Audit Ledger Display
st.divider()
st.subheader("Session Audit Ledger (Simulated In-Memory Store)")
st.caption("This demo stores events in Streamlit session state only. A production design should use persistent, access-controlled audit storage with appropriate tamper-evidence, retention, and monitoring controls.")
if st.session_state.audit_log:
    st.table(st.session_state.audit_log)
else:
    st.caption("No reviewer actions recorded in this session yet.")