📊 Function Flow Analyzer

A Streamlit web app that analyzes source code from uploaded files or GitHub repositories and provides powered by Amazon Q:

- **Project Summary**
- **Function Call Flow Diagrams**
- **Security Risk Detection**
- **Performance Bottleneck Suggestions**

---

Features

- Upload a folder of code files (supports multi-file upload)
- Clone and analyze a GitHub repository
- Supported languages:
  - Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Shell, Swift, Kotlin
- Amazon Q-generated output includes:
  - Function flow diagrams
  - Security risk reports
  - Performance optimization tips

---

Installation

1. Clone the Repository

bash
git clone https://github.com/SamboPalAccenture/CodeBaseAnalyzer
cd CodeBaseAnalyzer

2. Install Python Dependencies:

Make sure you have Python 3.8+ installed.
pip install -r requirements.txt

3. Install External AI CLI (q):

This project uses an external CLI tool (q chat) to analyze code via AI.
Install q:

# macOS (Homebrew)
brew install q-chat-ai/q/q
# or via other methods
# Visit: https://github.com/q-chat-ai/q


Check it works:
q chat --help

▶️ Usage

Run the app with:

streamlit run app.py
Then open your browser to:
http://localhost:8501

📁 Project Structure

├── app.py               # Main Streamlit app
├── analyzer.py          # AI-powered code analysis logic
├── requirements.txt     # Python dependencies
└── README.md            # Project info
