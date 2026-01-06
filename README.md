# MindChat

AI-based chat application for self-analysis and mental health support.
**⚠️ Important Disclaimer:** This is an AI-based chat application that can provide suggestions and tips. It does NOT replace professional help. If you are experiencing serious mental health issues or are in a crisis situation, please contact qualified professionals.

## Features

Currently only German language is implemented, but all texts are in one [central file](src/texts.py), so it is very simple to translate or to add multi-language support.

1. **Self-Disclosure Form:** Fill out a [structured self-disclosure form](src/prompts/self-disclosure-template.md) describing yourself, your situation, and your concerns
2. **AI Chat:** Chat with an AI that uses your self-disclosure as context to provide personalized conversations and suggestions

## Privacy & Data Protection

### Data Storage on This Server

- ✅ Your data is **not** permanently stored, but only held temporarily in memory
- ✅ All data is automatically deleted on logout and session end
- ✅ The developer of this app has **no access** to your inputs or chat history

### Processing by OpenAI

- ⚠️ **Important:** Your inputs are sent to OpenAI's (paid) API for processing in GPT model
- [OpenAI states](https://platform.openai.com/docs/guides/your-data): "Your data is your data. As of March 1, 2023, data sent to the OpenAI API is not used to train or improve OpenAI models (unless you explicitly opt in to share data with us)."
- ✅ **Alternative 1: Personal AI Account** With a personal ChatGPT or similar account you could achieve the same results, but with the big drawback, that the AI service can associate your inputs with your person
- ✅ **Alternative 2: Local** Run this app locally, see below.

### Transparency

- ✅ All communication is encrypted via HTTPS
- ✅ The source code is publicly available on [GitHub](https://github.com/entorb/mindchat) for transparency and review

## Tech stack

- [UV](https://docs.astral.sh/uv/)
- Python 3.11 (as Uberspace currently only supports up to 3.11)
- [Streamlit](https://streamlit.io)
- [SonarQube](https://sonarcloud.io/project/overview?id=entorb_mindchat) for static code analysis
