# MindChat - Agent Instructions

## Project Overview

AI-based chat application for self-analysis and mental health support using Streamlit.

**Key Features:**

1. Self-disclosure form using structured markdown template
2. AI chat with personalized context from self-disclosure
3. Multi-LLM provider support (Ollama, OpenAI, Mistral, Google)

## Tech Stack

- **Python 3.11** (Uberspace hosting constraint)
- **Streamlit** - Web framework
- **UV** - Package management
- **Ruff** - Linting and formatting
- **SonarQube** - Static code analysis

## Code Quality Standards

### Ruff Linter Compliance

Code **must** be compliant with ruff linter.

**After each change:**

```bash
uv run ruff format
uv run ruff check
```

Fix all issues before committing.

### No Type Ignores

Avoid `# type: ignore` comments. Use proper type hints with `from typing import Any` when needed.

## Project Structure

### Configuration Files

- **`config.py`** - Contains all configuration variables. Use these instead of hardcoding values.
  - Session state keys (SS_KEY_*)
  - Environment detection (Prod vs Local)
  - LLM provider lists
  - File paths

- **`texts.py`** - Contains all text constants for UI. Use these instead of hardcoding text.
  - Purpose: Simplifies later translation to other languages
  - Currently German language only

### Key Directories

- **`src/`** - Main application code
  - `main.py` - Entry point with navigation and LLM selection
  - `helper.py` - Utility functions (logging, navigation, login)
  - `llm.py` - Abstract LLM provider interface
  - `llm_*.py` - Concrete LLM provider implementations
  - `models.py` - Pydantic data models
  - `reports/` - Page implementations (r00_info, r01_self, r02_chat, r99_logout)
  - `prompts/` - LLM prompt templates

## Streamlit Best Practices (2025)

### Session State Management

- Use widget `key` parameter for automatic state binding
- Avoid manual session state sync and unnecessary `st.rerun()` calls
- Let Streamlit handle state changes automatically

### Performance Optimization

- Use `@st.fragment` decorator for isolated UI updates
- Cache expensive operations in session state
- Use `@st.dialog` for modal dialogs (e.g., login)

### Error Handling

- Use `st.error()` for user-facing errors
- Hide stack traces in production (`ENV == "Prod"`)
- Log detailed errors for debugging

## Privacy & Security

### Critical Considerations

- **No persistent storage** - All data is temporary, held only in session state
- **API security** - Secrets must be in `st.secrets` (not hardcoded)
- **Data minimization** - User data sent to LLM APIs should be clearly documented
- **HTTPS** - All communication must be encrypted

### Data Flow

1. User enters self-disclosure → Stored in session state only
2. Chat interactions → Sent to LLM API (OpenAI, etc.)
3. Session end/logout → All data automatically cleared

## Development Workflow

1. **Make changes** - Follow coding standards above
2. **Format code** - `uv run ruff format`
3. **Check linting** - `uv run ruff check`
4. **Test locally** - Verify changes work
5. **Check errors** - Ensure no type errors or warnings

## Testing

- Test file: `tests/test_run_all_pages.py`
- Run with pytest: `uv run pytest`
- Manual testing: `uv run streamlit run src/main.py`

## Important Notes

- **Language**: Currently German only, but texts centralized for easy translation
- **Disclaimer**: App does NOT replace professional mental health care
- **Transparency**: Source code is public on GitHub
- **LLM Providers**: Production uses OpenAI only; local dev supports multiple providers
