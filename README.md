# 🧹 AI-Powered Data Cleaning Assistant

A no-code assistant to clean your messy CSV datasets using intelligent profiling and AI-generated code suggestions.

---

## 📌 Introduction

### 🔍 The Problem
Data professionals often spend **60–80% of their time** just cleaning and preparing data before they can analyze or model it. Datasets frequently include:
- Missing, duplicate, or inconsistent values
- Malformed date formats and encoding issues
- Incorrect data types or string-numeric mismatches
- Nulls, outliers, and redundant columns

This repetitive and error-prone work slows down projects and consumes valuable analyst hours.

### 🤖 The Solution
The **AI Data Cleaning Assistant** tackles this problem by:
- Profiling the dataset intelligently
- Identifying issues like nulls, duplicates, and type mismatches
- Generating Python code to fix these issues using an LLM
- Presenting actionable summaries and ready-to-use cleaning code in a user-friendly web interface

Users simply upload a CSV file, and the tool does the rest—no coding required.

---

## ⚙️ How to Run the Project

### 🔧 Step 1: Clone the Repository
```bash
git clone https://github.com/DSM2499/AI_Data_Cleaner.git
cd AI_Data_Cleaner
```
### 🐍 Step 2: Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
### 🚀 Step 3: Launch the Streamlit App
```bash
streamlit run app.py
```
Upload a CSV file through the interface and receive data insights + cleaning code in seconds.

---

## 🛠️ Tech Stack & Skills
- Frontend/UI: Streamlit
- Backend: Python 3.11+
- Data Profiling: ```pandas```, ```pyjanitor```
- AI Model: Open AI GPT-3.5-Turbo (can be switched out with a more efficient model)
- Modular Python with CLI and UI separation

---

## 📸 Screenshots
![]()

## 📹 YouTube Tutorial
📺 ()

---

## 📈 Impact & Value

- ⏱️ ***Time Saved***: Reduces 60–80% of manual cleaning time.
- 📊 ***Better Insights***: Starts with clean data, leading to more reliable analytics.
- 👥 ***Team Productivity***: Standardizes preprocessing workflows across analysts.
- 🚀 ***Upskilling***: Helps beginners learn cleaning techniques via readable code.
- ⚙️ ***Automation***: Makes data pipelines more efficient and less error-prone

---

## 🧾 Conclusion
This AI-powered tool bridges the gap between raw data and actionable insights—removing the grunt work and letting analysts focus on strategy and decision-making. It serves as both a learning tool and a real-world automation system for streamlining the data cleaning process.

⭐️ Feel free to fork this repo, suggest enhancements, or open issues for bugs and ideas!

