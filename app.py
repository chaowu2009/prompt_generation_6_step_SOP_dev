import streamlit as st

from sop_core import STEP_CONFIG, apply_global_styles, ensure_state

st.set_page_config(page_title="AI-Enabled Agile Java SDLC Workflow", layout="wide")

apply_global_styles()
ensure_state()

st.title("AI-Enabled Agile Java SDLC Workflow Prompt Generator")
st.caption("Use the left Pages menu to open step_0(name) through step_6(name), plus generate_SKILL_file. No dropdown is used.")

st.markdown("### Overall Progress")
for step_key, config in STEP_CONFIG.items():
    is_done = st.session_state.done_flags.get(step_key, False)
    status = "Done" if is_done else "Pending"
    st.write(f"- {step_key}({config['name']}): {status}")
