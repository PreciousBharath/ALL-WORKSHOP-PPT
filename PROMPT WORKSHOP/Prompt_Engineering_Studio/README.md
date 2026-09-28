# Prompt Engineering Studio - AI Prompt Rewriter 🚀

A full-featured, interactive, premium web application built with **Python**, **Streamlit**, and **Plotly** designed to help developers, AI engineers, and prompt designers learn, analyze, and optimize Generative AI prompts.

---

## 🌟 Key Features

1. **✨ AI Prompt Rewriter**
   - Converts draft/weak prompts into structured, highly optimized prompts.
   - Enforces 9 core prompt engineering rules: *Role, Context, Goal, Output Format, Constraints, Examples, Detail Level, Clarity, Specificity*.
   - Explains every enhancement with a rule-by-rule breakdown.

2. **🧠 Prompt Analyzer**
   - Calculates **Quality Score**, **Specificity**, **Clarity**, **Complexity**, **Estimated Tokens**, and **Reading Time**.
   - Performs structural audit across 6 critical prompt components.

3. **🔤 Tiktoken Tokenization Inspector**
   - Tokenizes prompts using OpenAI's `tiktoken` (`cl100k_base` model).
   - Generates interactive token tables with Token ID, Byte representation, Token Length, Repeat Ratios, and token length distribution charts.

4. **🔠 ASCII Character Analyzer**
   - Displays character-by-character ASCII decimal, hexadecimal, binary, and category classifications (Uppercase, Lowercase, Digits, Symbols, Spaces).

5. **📊 Side-by-Side Prompt Comparison & Diff**
   - Highlights added, removed, and changed words using `difflib`.
   - Displays keyword treemaps and metric progress bars.

6. **📖 Prompt Engineering Masterclass**
   - Educational guide covering Zero-shot, Few-shot, Chain-of-Thought, System Prompts, Temperature, and Token mechanics.

7. **💡 30+ Interactive Examples**
   - Categorized repository across Coding, Writing, Data Science, Summarization, Business, and Education.

8. **📥 Exports & Utilities**
   - Export prompts and metric audits as **PDF Reports** or **TXT files**.
   - Copy to clipboard and favorite prompts management.

---

## 📁 Project Architecture

```
Prompt_Engineering_Studio/
├── app.py                   # Main Streamlit web application & UI layout
├── prompt_engine.py         # Multi-rule prompt rewriting engine & domain detector
├── analyzer.py              # Qualitative & quantitative metric algorithms
├── tokenizer.py             # Tiktoken & regex sub-word tokenization engine
├── ascii_analyzer.py        # ASCII table generator & classification parser
├── visualization.py         # Plotly visual charts (Radar, Bar, Treemap, Histogram)
├── utils.py                 # PDF exporter, difflib word diff, 30+ examples library
├── style.css                # Custom Dark Glassmorphism CSS design system
├── requirements.txt         # Dependencies list
└── README.md                # Documentation & setup guide
```

---

## ⚙️ Installation & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Launch Application
Run the Streamlit app:
```bash
streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend / App Framework**: Streamlit
- **Visualization**: Plotly Express & Plotly Graph Objects
- **Data Handling**: Pandas & NumPy
- **Tokenization**: OpenAI Tiktoken
- **PDF Exporting**: ReportLab
- **Styling**: Custom CSS (Glassmorphism & Glowing Gradients)

---

## 📄 License
Created for AI Prompt Engineers and Developers. Feel free to use, modify, and extend!
