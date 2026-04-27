import streamlit as st

from sop_core import apply_global_styles, render_copy_button


PROMPT_TEXT = """You are a senior Java software architect, test automation architect, and GitHub Copilot adoption coach.

Create a concise first version of `SKILL.md` for this repository.

Before writing `SKILL.md`, inspect the codebase and infer the project's actual patterns. Do not create a generic guide.

# Step 1 - Inspect the Repository First

Review the repository and summarize the actual patterns you find.

Inspect for:

- Build tool and main commands: Maven, Gradle, or both
- Java package structure
- Main application architecture
- Unit test framework and patterns
- Integration test framework and patterns
- Cucumber feature files, Gherkin style, tag usage, and folder structure
- Step definition structure, naming, and reuse patterns
- TestNG configuration and suite setup
- Selenium/page object structure
- API test structure
- Test data setup
- Environment/configuration files
- CI/CD files
- Cloud execution patterns
- Xray/Jira tags or traceability patterns
- Naming conventions
- Existing coding and testing style
- Security-sensitive areas such as secrets, tokens, URLs, users, passwords, and environment-specific IDs

After inspection, provide a brief summary:

1. Build and test setup
2. Java/project structure
3. Testing patterns
4. CI/CD or cloud execution patterns
5. Traceability patterns, if any
6. Key risks or unclear areas
7. Recommended rules to include in `SKILL.md`

# Step 2 - Generate `SKILL.md`

Using the inspection summary, generate a concise, practical `SKILL.md` tailored to this repository.

Because this repository already uses Cucumber and `.feature` files, include concrete Gherkin and step-definition rules in `SKILL.md` based on the patterns you find.

Include explicit guardrails that credentials, secrets, tokens, passwords, API keys, and environment-specific IDs must not be committed to version control. Require environment variables, secret managers, masked examples, or documented placeholder values instead.

Place those security guardrails in `Core Rules`, reinforce them in `Validation Rules`, and repeat the hard prohibition in `Do Not Do`.

Use this structure:

```md
# SKILL.md - Java Copilot Team Guide in the root folder.

## Purpose

## Maintenance and Review

## Repository Context

## Core Rules

## How Copilot Should Work

## Java Development Rules

## Testing Rules

## Debugging Rules

## Validation Rules

## Required Output Format

## Do Not Do
```"""


def ensure_generate_skill_state() -> None:
    if "generate_skill_file_prompt" not in st.session_state:
        st.session_state.generate_skill_file_prompt = ""


st.set_page_config(page_title="generate_SKILL_file", layout="wide")

apply_global_styles()
ensure_generate_skill_state()

st.title("generate_SKILL_file")
st.caption("Generate a repository-inspection prompt for creating SKILL.md in the root folder.")

st.markdown("### Purpose")
st.write("Use this page to generate the SKILL.md authoring prompt without using the step-based workflow framework.")

left_col, right_col = st.columns([1, 1])
with left_col:
    if st.button("Generate", type="primary", key="generate_skill_file_generate"):
        st.session_state.generate_skill_file_prompt = PROMPT_TEXT
with right_col:
    if st.button("Clear", key="generate_skill_file_clear"):
        st.session_state.generate_skill_file_prompt = ""
        st.rerun()

st.markdown("### Prompt Output")
st.markdown(
    'Save to: <span style="color: #1a6fcf; background-color: #d0e8ff; padding: 2px 8px; border-radius: 4px; font-weight: 600;">SKILL.md</span>',
    unsafe_allow_html=True,
)
st.text_area(
    "Generated Prompt",
    value=st.session_state.generate_skill_file_prompt,
    height=520,
)

copy_col, download_col = st.columns([1, 1])
with copy_col:
    render_copy_button("generate_SKILL_file", st.session_state.generate_skill_file_prompt)
with download_col:
    st.download_button(
        label="Download Prompt (.txt)",
        data=st.session_state.generate_skill_file_prompt.encode("utf-8"),
        file_name="generate_SKILL_file_prompt.txt",
        mime="text/plain",
        key="generate_skill_file_download",
    )