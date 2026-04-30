import json
import re
from typing import Any, Dict, List

import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
<style>
.stApp, .stApp * {
    font-size: 12pt !important;
}

.stApp {
    background: linear-gradient(180deg, #f6f8fc 0%, #eef3fb 100%);
}

h1, h2, h3 {
    color: #173b63;
    letter-spacing: 0.2px;
}

[data-testid="stCaptionContainer"] {
    background: #e7f0ff;
    border: 1px solid #c8dcff;
    border-radius: 10px;
    padding: 8px 10px;
}

.sop-field-label {
    font-weight: 700;
    color: #173b63;
    margin: 8px 0 4px;
}

[data-testid="stTextArea"] textarea {
    border: 1px solid #bdd0ee !important;
    border-radius: 10px !important;
    background: #ffffff !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: #2e6fd8 !important;
    box-shadow: 0 0 0 2px rgba(46, 111, 216, 0.15) !important;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px !important;
    border: 1px solid #2e6fd8 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #2e6fd8 0%, #2f8dbf 100%) !important;
    color: #ffffff !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(0.98);
}
</style>
""",
        unsafe_allow_html=True,
    )

SOP_TITLE = "AI-Enabled Agile Java SDLC Workflow"

SHARED_CONTEXT = {
    "team_context": "You are an AI delivery copilot for a SAFe Agile Java engineering team.",
    "sequence": "Define -> Clarify -> Design -> Build -> Test -> Release",
    "stack": "This SOP supports a test stack based on Java, Cucumber, TestNG, Selenium, and Xray.",
}

DEFAULT_RULES = [
    "Do not invent facts.",
    "Before generating each step output, check whether SKILL.md exists and use its latest content as the primary source for reusable workflow patterns. After each completed step, append only confirmed learnings to SKILL.md with a dated changelog entry. If SKILL.md conflicts with current confirmed inputs, prioritize current confirmed inputs and note the conflict.",
    "Use only provided input and prior step outputs.",
    "Keep outputs concise, practical, and reviewable.",
    "Use AI for drafting and analysis; final decisions stay with the team.",
    "Follow provided standards, file formats, and engineering principles.",
    "If input, assumptions, or 3-Amigo alignment is missing, call it out clearly.",
    "Reuse existing framework assets and patterns when possible.",
    "Do not fix unrelated existing issues unless they are simple, safe, and directly helpful to the requested change.",
    "Highlight placeholders, fake/sample values, hard-coded usernames/passwords, URLs, IDs, names, links, and similar items in the summary whenever found.",
    "No secrets or sensitive production data.",
]

MARKDOWN_STYLE = [
    "keep .md output light and easy to scan",
    "use one # title and ## sections",
    "prefer short bullets and short paragraphs",
    "use fenced code blocks with language tags when needed",
    "label Assumptions, Risks, Dependencies, and Open Questions when relevant",
]

COMMON_INPUT_PLACEHOLDERS = [
    "Jira / story / notes",
    "expected behavior",
    "actual behavior",
    "screenshots / logs / errors",
    "existing files / classes / methods to reuse",
    "target file path or package if known",
    "3 amigos notes if available",
]

STEP_CONFIG: Dict[str, Dict[str, Any]] = {
    "step_0": {
        "name": "Master Prompt",
        "role": "AI delivery copilot for a SAFe Agile Java engineering team",
        "task": "Support only the requested step and keep outputs aligned across Define, Clarify, Design, Build, Test, and Release.",
        "inputs": [
            "[project/system name]",
            "[business domain/feature area]",
            "[application type]",
            "[tech stack]",
            "[repo/module context if known]",
            "[team conventions, coding standards, architecture rules, or tech deck]",
        ],
        "outputs": [
            "Baseline context and rules for all downstream steps",
        ],
        "rules": [
            "Do not invent facts.",
            "Use only provided input and prior step outputs.",
            "Keep outputs concise, practical, and reviewable.",
            "Use AI for drafting and analysis; final decisions stay with the team.",
            "Follow provided standards, file formats, and engineering principles.",
            "If input, assumptions, or 3-Amigo alignment is missing, call it out clearly.",
            "Reuse existing framework assets and patterns when possible.",
            "Do not fix unrelated existing issues unless they are simple, safe, and directly helpful to the requested change.",
            "Highlight placeholders, fake/sample values, hard-coded usernames/passwords, URLs, IDs, names, links, and similar items in the summary whenever found.",
            "No secrets or sensitive production data.",
        ],
        "save_to": "(no required output file)",
    },
    "step_1": {
        "name": "Define",
        "role": "Senior Agile Java engineering lead",
        "task": "Turn the raw request into a sprint-ready Jira item.",
        "inputs": [],
        "optional_inputs": [
            "[story]",
            "[bug]",
            "[notes]",
            "[logs]",
            "[screenshots text]",
            "[business context]",
            "[related ticket IDs]",
            "[business priority]",
            "[known impacted systems/modules]",
            "[deadline or target release]",
            "[3-Amigo notes]",
            "[reviewer notes]",
        ],
        "outputs": [
            "Title, Business goal, Problem statement",
            "Scope, Out of scope",
            "Assumptions, Risks",
            "Impacted systems/modules",
            "Priority or severity recommendation",
            "Open questions for grooming",
            "Definition of Ready checklist",
        ],
        "rules": [
            "Do not invent facts.",
            "Keep it concise.",
            "Reflect 3-Amigo outcomes when available.",
            "If input or alignment is weak, list the gaps clearly.",
            "Preserve traceability to the original story or request.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_1_output.md",
    },
    "step_2": {
        "name": "Clarify",
        "role": "Senior QA analyst",
        "task": "Turn Step 1 into clear, test-ready requirements and acceptance criteria.",
        "inputs": "dev_step_1_output.md",
        "optional_inputs": [
            "[reviewer corrections]",
            "[business clarifications]",
            "[policy/compliance constraints]",
            "[user roles/personas]",
            "[known edge cases]",
            "[3-Amigo decisions or open items]",
        ],
        "outputs": [
            "Functional requirements, Non-functional requirements",
            "Business rules",
            "Success scenarios, Failure scenarios",
            "Edge cases",
            "Acceptance criteria labeled AC1, AC2, AC3...",
            "Draft Definition of Done",
        ],
        "rules": [
            "No code.",
            "No implementation details.",
            "Make each acceptance criterion observable and testable.",
            "Call out any Product/PO, Dev, and QA/Test misalignment clearly.",
            "Include relevant non-functional requirements.",
            "Preserve traceability back to the story and acceptance criteria.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_2_output.md",
    },
    "step_3": {
        "name": "Design",
        "role": "Senior Java software architect",
        "task": "Turn Step 2 into a practical Java solution design and sprint task plan.",
        "inputs": "dev_step_2_output.md",
        "optional_inputs": [
            "[repo/package structure]",
            "[architecture patterns]",
            "[integration details]",
            "[API/schema constraints]",
            "[non-functional priorities]",
            "[tech deck or engineering principles]",
            "[reviewer corrections]",
        ],
        "outputs": [
            "Architecture overview",
            "Impacted layers: controller, service, repository, domain/model, integrations",
            "API, schema, or contract changes",
            "Validation and exception handling approach",
            "Logging and observability approach",
            "Backward compatibility and rollback considerations",
            "Implementation plan",
            "Sprint task breakdown in order",
            "Expected files/modules to change",
            "Technical risks and dependencies",
        ],
        "rules": [
            "Java-oriented design.",
            "Do not generate full code.",
            "Keep it practical and low-risk.",
            "Reuse existing patterns and framework assets where possible.",
            "Preserve traceability to requirements and acceptance criteria.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_3_output.md",
    },
    "step_4": {
        "name": "Build",
        "role": "Senior Java developer",
        "task": "Turn Step 3 into implementation-ready code output and produce concrete code changes.",
        "inputs": "dev_step_3_output.md",
        "optional_inputs": [
            "[repo structure/module paths]",
            "[existing class names/file paths]",
            "[framework/library constraints]",
            "[coding standards]",
            "[special file formats or implementation principles]",
            "[branch naming conventions]",
            "[reviewer corrections]",
        ],
        "outputs": [
            "Code changes for affected layers",
            "Complete compilable code snippets (not pseudocode) for each changed file",
            "Validation, exception handling, and logging updates",
            "Required config changes",
            "Branch name, commit message, and PR title suggestions",
            "Review-needed hard-coded or placeholder items",
        ],
        "rules": [
            "Never create a file unless it contains complete, functional content. Do not create placeholder classes, stub methods with only a TODO body, empty config files, or empty directories. If a file cannot be fully implemented in the current step, skip it and note it as pending instead.",
            "No unnecessary refactoring.",
            "Keep code readable and production-oriented.",
            "Identify each code block with file path.",
            "Generate complete code blocks with proper language tags (for example: java, xml, yaml, properties, sql).",
            "For each changed file, provide full method/class-level code needed to implement the change, including imports and signatures.",
            "Do not return design-only text or pseudocode unless explicitly requested.",
            "Do not skip key imports or helper methods.",
            "Reuse existing framework components and patterns first.",
            "Do not fix unrelated existing issues unless they are simple, safe, and directly helpful to the requested change.",
            "Clearly summarize any fake, sample, placeholder, or hard-coded values found in the code output.",
            "Stay within scope.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_4_output.md",
    },
    "step_5": {
        "name": "Test",
        "role": "Senior Java QA automation engineer",
        "task": "Turn Step 4 into test assets and a validation plan.",
        "inputs": "dev_step_4_output.md",
        "optional_inputs": [
            "[repo-specific usage or deviations from Java/Cucumber/TestNG/Selenium/Xray stack]",
            "[test folder structure]",
            "[parallel execution constraints]",
            "[environment or test data constraints]",
            "[known flaky areas]",
            "[test design principles or tech deck]",
            "[reviewer corrections]",
        ],
        "outputs": [
            "Unit and API/integration test cases",
            "UI tests only if needed; Gherkin only if explicitly requested",
            "Test data examples and regression impact",
            "Quality risks, quality gates, and execution checklist",
        ],
        "rules": [
            "Prefer unit and API coverage over UI.",
            "No Thread.sleep.",
            "Support parallel execution where applicable.",
            "Keep tests stable, maintainable, and parallel-safe.",
            "Use approved or masked test data only.",
            "Include file path suggestions.",
            "Preserve traceability to acceptance criteria and Xray evidence.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_5_output.md",
    },
    "step_6": {
        "name": "Release",
        "role": "Senior engineering manager and release reviewer",
        "task": "Turn Step 5 into a final PR and sprint-closure package.",
        "inputs": "dev_step_5_output.md",
        "optional_inputs": [
            "[deployment environment]",
            "[release process notes]",
            "[monitoring/alerting tools]",
            "[rollback expectations]",
            "[Jira/Xray closure format]",
            "[reviewer corrections]",
        ],
        "outputs": [
            "PR and release summary",
            "Business value and key technical changes",
            "Test/acceptance coverage and release evidence",
            "Risks, deployment/rollback notes, and validation checks",
            "Reviewer checklist, closure comment, and demo summary",
            "Outstanding hard-coded or placeholder items",
        ],
        "rules": [
            "Be concise but complete.",
            "Focus on release readiness.",
            "Separate confirmed facts from risks or follow-up items.",
            "Include release evidence and traceability to tests/Xray where applicable.",
            "Identify rollback and validation ownership when relevant.",
            "Carry forward and summarize any placeholder or hard-coded items that still need review.",
            "Use the Step 0 markdown style.",
        ],
        "save_to": "dev_step_6_output.md",
    },
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return slug.strip("_")


def default_field_value(field: str) -> str:
    return f"[{field}]"


def is_required_md_field(field: str) -> bool:
    normalized = field.strip()
    return bool(re.fullmatch(r"dev_step_[1-6]_(output|feature_file)\.md", normalized))


def get_effective_field_value(step_key: str, field: str) -> str:
    field_key = slugify(field)
    value = st.session_state.form_data.get(step_key, {}).get(field_key, "")
    return str(value).strip()


def normalize_fields(fields: Any) -> List[str]:
    if isinstance(fields, str):
        stripped = fields.strip()
        return [stripped] if stripped else []
    if isinstance(fields, list):
        return [str(item).strip() for item in fields if str(item).strip()]
    return []


def get_step_inputs(step_key: str) -> List[str]:
    return normalize_fields(STEP_CONFIG[step_key].get("inputs"))


def get_step_optional_inputs(step_key: str) -> List[str]:
    return normalize_fields(STEP_CONFIG[step_key].get("optional_inputs"))


def uses_fixed_input_mode(step_key: str) -> bool:
    step_inputs = get_step_inputs(step_key)
    has_optional_inputs = bool(get_step_optional_inputs(step_key))
    has_md_only_inputs = bool(step_inputs) and all(is_required_md_field(field) for field in step_inputs)
    return has_optional_inputs or has_md_only_inputs


def ensure_state() -> None:
    if "form_data" not in st.session_state:
        st.session_state.form_data = {step_key: {} for step_key in STEP_CONFIG.keys()}

    for step_key, _config in STEP_CONFIG.items():
        if step_key not in st.session_state.form_data:
            st.session_state.form_data[step_key] = {}
        editable_fields = get_step_inputs(step_key) + get_step_optional_inputs(step_key)
        for field in editable_fields:
            field_key = slugify(field)
            if field_key not in st.session_state.form_data[step_key]:
                st.session_state.form_data[step_key][field_key] = ""

    if "generated_prompt_by_step" not in st.session_state:
        st.session_state.generated_prompt_by_step = {step_key: "" for step_key in STEP_CONFIG.keys()}

    if "done_flags" not in st.session_state:
        st.session_state.done_flags = {step_key: False for step_key in STEP_CONFIG.keys()}

    for step_key in STEP_CONFIG.keys():
        prompt_text = st.session_state.generated_prompt_by_step.get(step_key, "")
        if str(prompt_text).strip():
            st.session_state.done_flags[step_key] = True


def build_done_subtitle() -> str:
    parts: List[str] = []
    for step_key, config in STEP_CONFIG.items():
        is_done = st.session_state.done_flags.get(step_key, False)
        if is_done:
            parts.append(f"{step_key}({config['name']}) (Done)")
        else:
            parts.append(f"{step_key}({config['name']})")
    return ", ".join(parts)


def reset_step_fields(step_key: str) -> None:
    st.session_state.form_data[step_key] = {}
    editable_fields = get_step_inputs(step_key) + get_step_optional_inputs(step_key)
    for field in editable_fields:
        field_key = slugify(field)
        st.session_state.form_data[step_key][field_key] = ""
        state_key = f"{step_key}_{slugify(field)}"
        st.session_state[state_key] = ""


def _render_field(step_key: str, field: str, required: bool) -> None:
    field_key = slugify(field)
    state_key = f"{step_key}_{field_key}"
    current_value = st.session_state.form_data[step_key].get(field_key, "")
    label = f"{field} *" if required else field
    st.markdown(f"<div class='sop-field-label'>{label}</div>", unsafe_allow_html=True)
    entered = st.text_area(
        label=label,
        key=state_key,
        value=current_value,
        height=110,
        placeholder=f"Paste {field} content here..." if required else f"Optional — {field}",
        label_visibility="collapsed",
    )
    st.session_state.form_data[step_key][field_key] = entered


def render_step_form(step_key: str) -> None:
    config = STEP_CONFIG[step_key]
    st.subheader(f"{step_key}({config['name']})")
    st.write(f"Role: {config['role']}")
    st.write(f"Task: {config['task']}")

    step_inputs = get_step_inputs(step_key)
    step_optional_inputs = get_step_optional_inputs(step_key)

    # Special handling for step_0: render inputs as editable fields
    if step_key == "step_0":
        if step_inputs:
            st.markdown("### Input")
            st.caption("Provide values for each context item.")
            for field in step_inputs:
                _render_field(step_key, field, required=False)

        if step_optional_inputs:
            st.markdown("### Additional Context")
            st.caption("Optional — leave blank to omit from the generated prompt.")
            for field in step_optional_inputs:
                _render_field(step_key, field, required=False)
    elif uses_fixed_input_mode(step_key):
        if step_inputs:
            st.markdown("### Input")
            for field in step_inputs:
                if field.strip().lower().endswith(".md"):
                    st.markdown(
                        f'- <span style="color: #1a6fcf; background-color: #d0e8ff; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{field}</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(f"- {field}")

        if step_optional_inputs:
            st.markdown("### Input Placeholders")
            st.caption("Optional — leave blank to omit from the generated prompt.")
            for field in step_optional_inputs:
                _render_field(step_key, field, required=False)
    else:
        required_fields = [f for f in step_inputs if is_required_md_field(f)]
        optional_fields = [f for f in step_inputs if not is_required_md_field(f)]

        if required_fields:
            st.markdown("### Required Input Files")
            st.caption("Paste the full content of each required file. Fields marked * must not be empty.")
            for field in required_fields:
                _render_field(step_key, field, required=True)

        if optional_fields:
            st.markdown("### Input Placeholders")
            st.caption("Optional — leave blank to omit from the generated prompt.")
            for field in optional_fields:
                _render_field(step_key, field, required=False)


def validate_required_inputs(step_key: str) -> List[str]:
    missing: List[str] = []
    step_inputs = get_step_inputs(step_key)

    if uses_fixed_input_mode(step_key):
        required_fields = step_inputs
    else:
        required_fields = [f for f in step_inputs if is_required_md_field(f)]

    for field in required_fields:
        if field.strip().lower().endswith(".md"):
            # Markdown inputs are assumed to be available from prior workflow.
            continue
        value = st.session_state.form_data.get(step_key, {}).get(slugify(field), "")
        if not str(value).strip():
            missing.append(field)
    return missing


def build_step_0_prompt() -> str:
    lines: List[str] = []
    lines.append(SHARED_CONTEXT["team_context"])
    lines.append("")
    lines.append("This is a sequential 6-step SOP:")
    lines.append("")
    lines.append(SHARED_CONTEXT["sequence"])
    lines.append("")
    lines.append(SHARED_CONTEXT["stack"])
    lines.append("")

    lines.append("Default rules for all steps")
    lines.append("")
    for item in DEFAULT_RULES:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("Markdown style")
    lines.append("")
    for item in MARKDOWN_STYLE:
        lines.append(f"- {item}")
    lines.append("")

    # Read step_0 inputs
    step_inputs = get_step_inputs("step_0")
    if step_inputs:
        lines.append("Input context")
        lines.append("")
        for field in step_inputs:
            value = get_effective_field_value("step_0", field)
            if value:
                lines.append(f"- {field}: {value}")
            else:
                lines.append(f"- {field}")
        lines.append("")

    lines.append("Common input placeholders")
    lines.append("")
    for item in COMMON_INPUT_PLACEHOLDERS:
        lines.append(f"- [{item}]")
    lines.append("")

    notes_value = get_effective_field_value("step_0", "additional shared context notes")
    if notes_value:
        lines.append("Additional shared context notes")
        lines.append("")
        lines.append(notes_value)
        lines.append("")

    lines.append("Do not do anything yet.")
    return "\n".join(lines).strip() + "\n"


def build_step_prompt(step_key: str) -> str:
    config = STEP_CONFIG[step_key]

    lines: List[str] = []
    lines.append(f"Role: {config['role']}")
    lines.append("")
    lines.append(f"Task: {config['task']}")
    lines.append("")

    lines.append("Input")
    lines.append("")
    step_inputs = get_step_inputs(step_key)
    step_optional_inputs = get_step_optional_inputs(step_key)

    if uses_fixed_input_mode(step_key):
        for item in step_inputs:
            lines.append(f"- {item}")

        for item in step_optional_inputs:
            value = get_effective_field_value(step_key, item)
            if value:
                lines.append(f"- {value}")
    else:
        for item in step_inputs:
            value = get_effective_field_value(step_key, item)
            if value:
                lines.append(f"- {value}")
    lines.append("")

    lines.append("Output")
    lines.append("")
    for item in config["outputs"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append("Rules")
    lines.append("")
    for item in config["rules"]:
        lines.append(f"- {item}")
    lines.append("")

    lines.append(f"Save to: {config['save_to']}")
    return "\n".join(lines).strip() + "\n"


def build_prompt(current_step_key: str) -> str:
    if current_step_key == "step_0":
        return build_step_0_prompt()
    if current_step_key in {"step_1", "step_2", "step_3", "step_4", "step_5", "step_6"}:
        return build_step_prompt(current_step_key)
    return ""


def render_copy_button(step_key: str, text: str) -> None:
        button_id = f"copy-btn-{step_key}"
        escaped_text = json.dumps(text)
        disabled_attr = "disabled" if not text else ""

        st.components.v1.html(
                f"""
<div>
    <button id="{button_id}" {disabled_attr}
        style="
            width: auto;
            min-width: 96px;
            height: 2.5rem;
            border-radius: 10px;
            border: 1px solid #de8a8a;
            padding: 0 0.9rem;
            background: linear-gradient(90deg, #f7caca 0%, #f3b5b5 100%);
            color: #7a1f1f;
            font-weight: 600;
            cursor: pointer;
        ">
        Copy
    </button>
</div>
<script>
    (function() {{
        const btn = document.getElementById({json.dumps(button_id)});
        const text = {escaped_text};
        if (!btn) return;
        btn.addEventListener('mouseenter', function() {{
            if (!btn.disabled) btn.style.filter = 'brightness(0.98)';
        }});
        btn.addEventListener('mouseleave', function() {{
            btn.style.filter = 'none';
        }});
        if (btn.disabled) {{
            btn.style.opacity = '0.55';
            btn.style.cursor = 'not-allowed';
        }}
        btn.addEventListener('click', async function() {{
            const originalText = btn.textContent;
            try {{
                await navigator.clipboard.writeText(text);
                btn.textContent = 'Copied';
            }} catch (err) {{
                const ta = document.createElement('textarea');
                ta.value = text;
                document.body.appendChild(ta);
                ta.select();
                try {{
                    document.execCommand('copy');
                    btn.textContent = 'Copied';
                }} finally {{
                    document.body.removeChild(ta);
                }}
            }}
            setTimeout(function() {{ btn.textContent = originalText; }}, 1200);
        }});
    }})();
</script>
""",
                height=44,
        )


def render_step_page(step_key: str) -> None:
    apply_global_styles()
    ensure_state()
    config = STEP_CONFIG[step_key]

    st.title(f"{step_key}({config['name']})")
    st.caption(build_done_subtitle())
    st.caption("Use Generate to build the prompt. Done flag is set automatically per step.")

    render_step_form(step_key)

    left_col, right_col, status_col = st.columns([1, 1, 1])
    with left_col:
        if st.button("Generate", type="primary", key=f"generate_{step_key}"):
            missing_required = validate_required_inputs(step_key)
            if missing_required:
                missing_display = ", ".join(missing_required)
                st.error(f"Required input missing: {missing_display}")
                st.session_state.done_flags[step_key] = False
                return
            st.session_state.generated_prompt_by_step[step_key] = build_prompt(step_key)
            st.session_state.done_flags[step_key] = True
    with right_col:
        if st.button("Clear Current Step Fields", key=f"clear_{step_key}"):
            reset_step_fields(step_key)
            st.session_state.generated_prompt_by_step[step_key] = ""
            st.session_state.done_flags[step_key] = False
            st.rerun()
    with status_col:
        st.checkbox("Done", value=st.session_state.done_flags[step_key], disabled=True, key=f"done_{step_key}")

    st.markdown("### Prompt Output")
    save_to = config.get("save_to", "")
    if save_to and save_to != "(no required output file)":
        st.markdown(
            f'Save to: <span style="color: #1a6fcf; background-color: #d0e8ff; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{save_to}</span>',
            unsafe_allow_html=True,
        )
    st.text_area(
        "Generated Prompt",
        value=st.session_state.generated_prompt_by_step[step_key],
        height=420,
    )

    output_copy_col, output_download_col = st.columns([1, 1])
    with output_copy_col:
        render_copy_button(step_key, st.session_state.generated_prompt_by_step[step_key])
    with output_download_col:
        st.download_button(
            label="Download Prompt (.txt)",
            data=st.session_state.generated_prompt_by_step[step_key].encode("utf-8"),
            file_name=f"{step_key}_prompt.txt",
            mime="text/plain",
            key=f"download_{step_key}",
        )
