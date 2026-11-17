"""BridgeNote Lab - a separate, privacy-first PulseArk research companion."""

import streamlit as st

from agent import generate_lesson_routine, generate_sos_protocol, SOS_SCENARIOS
from lab_data import inquiries, metrics, observations, portfolio_markdown, save_inquiry, save_observation
from student_db import load_students


st.set_page_config(page_title="BridgeNote Lab | PulseArk", page_icon="🧪", layout="wide")

st.markdown("""
<style>
.hero {padding:1.6rem 0 .4rem}.eyebrow {color:#3a7167;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:.78rem}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero"><div class="eyebrow">PulseArk · Music, observation, inquiry</div>
<h1>BridgeNote Lab</h1><p>A privacy-first field notebook for turning compassionate music sessions into careful questions, small adjustments, and honest evidence.</p></div>
""", unsafe_allow_html=True)
st.info("BridgeNote Lab supports reflection and program learning. It is not a diagnostic, therapeutic, or clinical decision tool.")

tab_session, tab_observe, tab_inquiry, tab_impact, tab_portfolio = st.tabs(
    ["🎻 Field session", "🔎 Observe", "🧠 Inquiry log", "📊 Impact", "📄 Portfolio"]
)

with tab_session:
    st.subheader("Adapt a music session with care")
    st.caption("Demo profiles are included only to demonstrate the workflow. Use de-identified participant codes for real sessions.")
    students = load_students()
    names = {f"{s['name']} · demo profile": s for s in students}
    left, right = st.columns([2, 1])
    with left:
        chosen_name = st.selectbox("Choose a demo profile", list(names))
        student = names[chosen_name]
    with right:
        length = st.select_slider("Session length", options=[15, 20, 25, 30], value=20)
    if st.button("Build a gentle session routine", type="primary"):
        st.session_state["lab_routine"] = generate_lesson_routine(student, total_min=length)
    routine = st.session_state.get("lab_routine")
    if routine:
        for block in routine["blocks"]:
            st.markdown(f"**{block['order']}. {block['title']}** · {block['duration_min']} min")
            st.caption(block["description"])
    st.divider()
    st.markdown("**If the participant is distressed, pause and involve the appropriate supervising adult.**")
    scenario = st.selectbox("Choose a situation for a demo de-escalation prompt", SOS_SCENARIOS)
    if st.button("Show safety-oriented prompt"):
        protocol = generate_sos_protocol(student, scenario)
        st.warning(protocol["principle"])
        for number, step in enumerate(protocol["steps"], start=1):
            st.write(f"{number}. {step}")
        st.caption(protocol["disclaimer"])

with tab_observe:
    st.subheader("Record one de-identified observation")
    st.caption("Record what was observable, not a diagnosis or a judgment. Do not enter names, medical details, recordings, or contact information.")
    consent = st.checkbox("I confirm this entry is de-identified and recorded under the program's approved consent process.")
    with st.form("observation_form", clear_on_submit=True):
        participant_code = st.text_input("Participant code", placeholder="e.g. PA-014")
        session_date = st.date_input("Session date")
        context = st.text_input("Activity or context", placeholder="e.g. violin warm-up with visual schedule")
        one, two, three = st.columns(3)
        with one:
            engagement = st.slider("Observable engagement", 1, 5, 3, help="1 = rarely joined; 5 = consistently joined")
        with two:
            regulation = st.slider("Observable regulation", 1, 5, 3, help="1 = needed frequent pause/support; 5 = sustained comfort")
        with three:
            communication = st.slider("Communication access", 1, 5, 3, help="1 = access was limited; 5 = preferences were readily expressed")
        adjustment = st.text_area("What adjustment did you try?", placeholder="e.g. shortened the task and offered a visual choice")
        observed = st.text_area("What happened next?", placeholder="Describe only what you observed.")
        submit_observation = st.form_submit_button("Save observation")
    if submit_observation:
        if not consent:
            st.error("Confirm de-identification and approved consent before saving.")
        elif not participant_code.strip() or not context.strip() or not observed.strip():
            st.error("Participant code, context, and observation are required.")
        else:
            save_observation({"participant_code": participant_code.strip(), "session_date": str(session_date), "context": context.strip(), "engagement": engagement, "regulation": regulation, "communication": communication, "adjustment": adjustment.strip(), "observed": observed.strip()})
            st.success("Observation saved to this local pilot record.")

with tab_inquiry:
    st.subheader("Move from a pattern to a testable question")
    st.caption("An inquiry log makes the reasoning visible: question → small adjustment → reflection. It does not prove causation.")
    with st.form("inquiry_form", clear_on_submit=True):
        question = st.text_input("Question", placeholder="What happens when we offer a visual choice before a transition?")
        hypothesis = st.text_area("Working hypothesis", placeholder="A visual choice may make the transition easier to anticipate.")
        adjustment = st.text_area("Small adjustment to try", placeholder="Offer two picture-card options before changing activities.")
        reflection = st.text_area("Reflection after observation", placeholder="What did you observe? What remains uncertain?")
        submit_inquiry = st.form_submit_button("Save inquiry cycle")
    if submit_inquiry:
        if not all([question.strip(), hypothesis.strip(), adjustment.strip(), reflection.strip()]):
            st.error("Complete all four fields so the reasoning stays auditable.")
        else:
            save_inquiry({"question": question.strip(), "hypothesis": hypothesis.strip(), "adjustment": adjustment.strip(), "reflection": reflection.strip()})
            st.success("Inquiry cycle saved.")
    saved_inquiries = inquiries()
    if saved_inquiries:
        st.divider()
        st.markdown("**Recent inquiry cycles**")
        for item in saved_inquiries[-3:][::-1]:
            with st.expander(item["question"]):
                st.write("**Hypothesis:**", item["hypothesis"])
                st.write("**Adjustment:**", item["adjustment"])
                st.write("**Reflection:**", item["reflection"])

with tab_impact:
    st.subheader("See signals, not claims")
    stats = metrics()
    a, b, c, d = st.columns(4)
    a.metric("Structured sessions", stats["sessions"])
    b.metric("Participant codes", stats["participants"])
    c.metric("Mean engagement", "—" if stats["engagement"] is None else f"{stats['engagement']} / 5")
    d.metric("Mean regulation", "—" if stats["regulation"] is None else f"{stats['regulation']} / 5")
    records = observations()
    if records:
        st.caption("These are descriptive observer scores, not clinical outcomes.")
        chart_data = [{"session": i + 1, "engagement": r["engagement"], "regulation": r["regulation"], "communication": r["communication"]} for i, r in enumerate(records)]
        st.line_chart(chart_data, x="session", y=["engagement", "regulation", "communication"])
        st.dataframe([{k: r[k] for k in ("session_date", "participant_code", "context", "engagement", "regulation", "communication")} for r in records], use_container_width=True, hide_index=True)
    else:
        st.info("Save de-identified observations to begin a descriptive trend view.")

with tab_portfolio:
    st.subheader("Turn work into an evidence portfolio")
    st.caption("Use this as a factual starting point for a college activity description or project reflection — not as a substitute for your own writing.")
    portfolio = portfolio_markdown()
    st.code(portfolio, language="markdown")
    st.download_button("Download portfolio summary (.md)", data=portfolio, file_name="bridgenote-lab-evidence-portfolio.md", mime="text/markdown")
    st.markdown("**Suggested essay framing:** notice a real barrier → design a small, ethical support → document what changed and what stayed uncertain → pursue the next question.")

st.divider()
st.caption("BridgeNote Lab · PulseArk pilot companion · Keep real participant data de-identified, minimal, consented, and locally governed.")

