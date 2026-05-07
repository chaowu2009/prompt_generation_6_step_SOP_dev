# AI-Enabled Agile Java SDLC Workflow Prompt Generator

This repository is a Streamlit app that helps teams generate structured prompts for a 6-step SDLC workflow:

1. Define
2. Clarify
3. Design
4. Build
5. Test
6. Release

It also provides a separate page to generate a repository-inspection prompt for creating a `SKILL.md` team guide.

## What This App Does

1. Provides one page per workflow step (`step_0` to `step_6`) in Streamlit Pages navigation.
2. Renders role/task/input/output/rules from a centralized configuration in `sop_core.py`.
3. Generates copyable/downloadable prompt text per step.
4. Tracks step completion state in `st.session_state`.
5. Includes a dedicated `generate_SKILL_file` page for producing a curated `SKILL.md` authoring prompt.

## Tech Stack

1. Python 3.9+
2. Streamlit (`streamlit>=1.35.0`)

## Project Structure

```text
.
├── app.py
├── sop_core.py
├── requirements.txt
├── README.md
└── pages/
	 ├── step_0(Master Prompt).py
	 ├── step_1(Define).py
	 ├── step_2(Clarify).py
	 ├── step_3(Design).py
	 ├── step_4(Build).py
	 ├── step_5(Test).py
	 ├── step_6(Release).py
	 └── generate_SKILL_file.py
```

## How It Works

### 1) `app.py` (home page)

1. Sets app title and layout.
2. Applies global UI styling.
3. Initializes session state.
4. Shows overall progress for every configured step.

### 2) `sop_core.py` (core engine)

This file contains nearly all business logic:

1. `STEP_CONFIG`:
	1. Declares each step's role, task, input model, output checklist, rules, and save target.
2. State management:
	1. `ensure_state()` initializes and normalizes `form_data`, generated prompts, and done flags.
3. Rendering:
	1. `render_step_form()` dynamically renders fields based on step mode.
	2. `render_step_page()` handles Generate/Clear actions and output area.
4. Prompt generation:
	1. `build_step_0_prompt()` builds shared baseline context and universal rules.
	2. `build_step_prompt()` builds step-specific prompt blocks.
	3. `build_prompt()` routes to correct prompt builder.
5. Utilities:
	1. `slugify()`, field normalization helpers, required-input validation.
	2. Custom HTML/JS copy button via `render_copy_button()`.

### 3) `pages/step_*.py` (step pages)

Each step page is intentionally minimal:

1. Sets the page title.
2. Calls `render_step_page("step_n")` from `sop_core.py`.

### 4) `pages/generate_SKILL_file.py`

1. Contains a long, curated prompt template (`PROMPT_TEXT`).
2. Generates or clears this text via buttons.
3. Shows output with copy/download actions.
4. Indicates target output file as `SKILL.md`.

## Step Model Summary

### `step_0 (Master Prompt)`

1. Collects shared context values (project/system name, domain, app type, stack, etc.).
2. Produces a baseline prompt with:
	1. Team context
	2. SOP sequence
	3. Stack note
	4. Default rules
	5. Markdown style rules
	6. Common placeholders

### `step_1` to `step_6`

1. Render role/task/input/output/rules from `STEP_CONFIG`.
2. Generate prompt text using step-specific configuration.
3. Mark step done automatically after successful generation.
4. Provide `.txt` download per step.

## Input Behavior

The app has two input modes:

1. Fixed-input mode:
	1. Used when a step has optional placeholders or `.md`-only required inputs.
	2. Required markdown file names are displayed as fixed items (assumed to come from prior workflow outputs).
2. Field-entry mode:
	1. Used when non-markdown required fields need direct user input.

Validation notes:

1. Non-markdown required fields are validated for non-empty content.
2. `.md` required inputs are treated as workflow artifacts and not validated as pasted text.

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies.
3. Start Streamlit.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage Flow

1. Open the app in browser (Streamlit will provide the URL).
2. Use the left Pages menu.
3. Start with `step_0(Master Prompt)` and click Generate.
4. Continue `step_1` to `step_6`.
5. For each step:
	1. Fill optional placeholders if needed.
	2. Click Generate.
	3. Copy or download the prompt.
6. Optionally open `generate_SKILL_file` to generate the `SKILL.md` authoring prompt.

## Output Targets (Configured)

The app displays these save targets in the UI:

1. `step_0`: `(no required output file)`
2. `step_1`: `dev_step_1_output.md`
3. `step_2`: `dev_step_2_output.md`
4. `step_3`: `dev_step_3_output.md`
5. `step_4`: `dev_step_4_output.md`
6. `step_5`: `dev_step_5_output.md`
7. `step_6`: `dev_step_6_output.md`
8. `generate_SKILL_file`: `SKILL.md`

## Current Limitations

1. No persistence layer: data is kept in Streamlit session state only.
2. No automatic file write-back for generated markdown targets.
3. No automated test suite included in this repository.

## Dependency

```text
streamlit>=1.35.0
```
