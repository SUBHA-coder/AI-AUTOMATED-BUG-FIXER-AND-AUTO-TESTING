# AI Auto Debugger & Testing Project

## 📌 Overview
This project demonstrates an automated self-healing code pipeline. It intentionally contains a buggy Python application and a suite of test cases that fail initially. An AI agent (powered by Groq LLM) is triggered to analyze the failures, fix the code, and verify the fixes by re-running the tests.

## 🚀 Features
- **Buggy Application**: A Python module (`app/buggy_app.py`) with intentional logical errors and missing validations.
- **Automated Testing**: `pytest` suite (`tests/test_buggy_app.py`) covering edge cases and valid inputs.
- **AI Debugger**: A module (`ai_debugger.py`) that uses the Groq API to fix code based on test reports.
- **Test Runner**: An orchestrator (`test_runner.py`) that manages the test-fix-retest loop.
- **Reporting**: Generates `initial_test_report.txt` (failures) and `final_test_report.txt` (success).

## 📂 Project Structure
```
ai_auto_debugger/
│
├── app/
│   ├── buggy_app.py       # The application code (starts buggy, gets fixed)
│
├── tests/
│   ├── test_buggy_app.py  # Test suite
│
├── reports/               # Test execution reports
│
├── ai_debugger.py         # AI interaction logic
├── test_runner.py         # Main execution script
├── requirements.txt       # Dependencies
├── .env                   # API Keys (not committed)
└── README.md
```

## 🛠️ Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Rename `.env.example` to `.env` and add your Groq API Key:
```bash
cp .env.example .env
```
Edit `.env`:
```
GROQ_API_KEY=your_actual_api_key
GROQ_MODEL=llama3-8b-8192
```

### 3. Run the Automation
Execute the test runner:
```bash
python test_runner.py
```

## 🔄 How It Works
1. **Initial Run**: `test_runner.py` runs `pytest`. Tests fail due to intentional bugs. Output is saved to `reports/initial_test_report.txt`.
2. **AI Analysis**: `ai_debugger.py` reads the buggy code and the failure report. It constructs a prompt for the LLM.
3. **Auto-Fix**: The LLM generates corrected code, which overwrites `app/buggy_app.py`.
4. **Verification**: `test_runner.py` re-runs `pytest`. If successful, `reports/final_test_report.txt` will show all tests passing.

## ⚠️ Notes
- Ensure you have a valid Groq API key with access to the specified model.
- The AI blindly overwrites the file based on the prompt. In a production environment, this should include more safeguards (git branch, diff review).
