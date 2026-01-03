# MindChat

AI-based psycho therapy chat application for self-analysis and mental health support. This does NOT replace professional help.

## Features

- Fill out a self-disclosure form
- Chat with an AI "therapist" that uses your self-disclosure as context for personalized conversations and suggestions

## Privacy

- Your data is only processed in memory, not stored on the server or in database and all is deleted at logout and session end.
- Your data is processed by OpenAI LLM GPT-5 via their API.
- Communication is encrypted via HTTPS.
- The source code is publicly available on [GitHub](https://github.com/entorb/mindchat) for transparency.

## Tools

- Python 3.11 (as Uberspace currently only supports up to 3.11)
- [Streamlit](https://streamlit.io)
- [UV](https://docs.astral.sh/uv/)
- [SonarQube](https://sonarcloud.io/project/overview?id=entorb_mindchat) for Static Code analysis
- Matomo (local instance) for access stats without personal data
- [Sentry](https://sentry.io) for exception alerts (not logging any user data)
