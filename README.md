# RevealMe 🕵️‍♂️🔍

RevealMe is an **OSINT** (Open Source Intelligence) tool designed to help users discover and analyze public information available about them online. By leveraging advanced AI models such as **GPTo1** and **GPTo1-preview** from OpenAI, RevealMe provides an efficient solution to examine digital footprints and manage online privacy.

> **Tester l'application en ligne** : [RevealMe](https://revealme.streamlit.app/)
---

## 🎯 Project Objective

RevealMe aims to provide an intuitive platform that allows users to discover publicly available information about themselves from various online sources. The tool helps users better understand, and potentially act on, the public information visible about them, contributing to improved online privacy management.

---

## 🚀 Key Features

- **Automated Data Collection**: Mini-agents gather information from various sources, such as social media, public databases, and search engines.
- **Advanced AI Analysis**: Utilizes OpenAI models to analyze and structure the retrieved data.
- **Privacy Management**: Identifies sensitive information and provides recommendations to enhance privacy control.
- **User-Friendly Interface**: A simple interface to query and explore the gathered results.

---

## 📂 Project Structure

```
RevealMe/
├── agents/                     # Folder for specialized agents
│   ├── base_agent.py           # Base class for all agents
│   ├── breachData_agent.py     # Agent for breach data searches
│   ├── facebook_agent.py       # Agent for Facebook searches
│   ├── github_agent.py         # Agent for GitHub searches
│   ├── googleSearch_agent.py   # Agent for Google searches
│   ├── instagram_agent.py      # Agent for Instagram searches
│   ├── linkedin_agent.py       # Agent for LinkedIn searches
│   ├── pipl_agent.py           # Agent for Pipl searches
│   ├── twitter_agent.py        # Agent for Twitter searches
│   └── whois_agent.py          # Agent for WHOIS queries
├── core/                       # Core functionalities of the application
│   ├── __init__.py
│   ├── agent.py                # Main agent handler
├── llm/                        # Modules for Large Language Models (LLM)
│   ├── base_llm.py             # Base for LLMs
│   ├── gemini.py               # Gemini model
│   └── gpt_o1.py               # GPT-O1 model
├── templates/                  # HTML template files
│   └── root.jinja2             # Main template
├── utils/                      # Utility functions
│   ├── .env                    # Environment variables
│   └── app.py                  # Main application file
└── requirements.txt            # List of dependencies
```

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- Dependencies listed in `requirements.txt`

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TitanSage02/RevealMe.git
   cd RevealMe
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment**:
   Create a `.env` file in the root of the project with the required information (e.g., API keys):
   ```bash
    OPENAI_API_KEY = ""

    SERP_API_KEY = ""
   ```

4. **Run the application**:
   ```bash
   python streamlit app.py
   ```

---

## 🗄️ Adding New Sources

RevealMe allows you to easily add new information collection agents or modify existing ones. Here's how to add a new information source:

### Steps to Add an Agent

1. **Create a new agent file** in the `agents/` folder following the structure of `base_agent.py`.

2. **Add your agent** to the `core/agent.py` file so it will be recognized during execution.

3. **Restart the application**:
   ```bash
   python streamlit app.py
   ```

---

## 📊 Interface Demo

[assets/demo.mp4]  
*Coming soon...*

---

## 🤖 Usage

Once the application is running, you can interact with RevealMe to retrieve information such as:

- *What Google results are associated with my name?*
- *Which accounts are linked to my email address?*
- *Does my information appear in any data breaches?*

RevealMe scans available sources and provides a structured analysis of the results.

---

## 👥 Contributions

Contributions are welcome! Here's how you can contribute:

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-new-agent`).
3. **Commit your changes** (`git commit -m 'Added new agent'`).
4. **Push the branch** (`git push origin feature-new-agent`).
5. **Open a Pull Request** and describe your changes.

---

## 📄 License

This project is licensed under the MIT License. 
See the [LICENSE.md](LICENSE.md) file for more details.

---