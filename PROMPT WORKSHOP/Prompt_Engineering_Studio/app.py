"""
==============================================================================
PROMPT ENGINEERING STUDIO - AI PROMPT REWRITER & LEARNING PLATFORM
==============================================================================
Author: Senior AI Engineer & Full Stack Specialist
Framework: Streamlit, Plotly, Pandas, Tiktoken, ReportLab
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import html

# Import custom modules
from prompt_engine import PromptEngine
from analyzer import PromptAnalyzer
from tokenizer import PromptTokenizer
from ascii_analyzer import ASCIIAnalyzer
from visualization import PromptVisualizer
from utils import PromptUtils

# ----------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION & CSS LOADING
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Prompt Engineering Studio | AI Prompt Rewriter",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom Glassmorphism CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ----------------------------------------------------------------------------
# INITIALIZE SESSION STATE
# ----------------------------------------------------------------------------
if "raw_input" not in st.session_state:
    st.session_state.raw_input = "Explain Python"

if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "general"

# Instantiate engine services
engine = PromptEngine()
analyzer = PromptAnalyzer()
tokenizer = PromptTokenizer()
ascii_proc = ASCIIAnalyzer()
visualizer = PromptVisualizer()
utils = PromptUtils()

# ----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & QUICK CONTROL PANEL
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">
            🚀 Prompt Studio
        </h2>
        <p style="font-size: 0.8rem; color: #9ca3af; margin-top: 4px;">AI Prompt Rewriter & Masterclass</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Navigation Menu
    nav_option = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "✨ Prompt Rewriter",
            "🧠 Prompt Analyzer",
            "🔤 Tokenization",
            "🔠 ASCII Analyzer",
            "📊 Prompt Comparison",
            "📖 Learn Prompt Engineering",
            "💡 Prompt Examples",
            "ℹ About"
        ],
        index=1
    )

    st.divider()

    # Quick Settings & Domain Selector
    st.markdown("### ⚙️ Engine Settings")
    domain_override = st.selectbox(
        "Target Persona Domain",
        ["Auto-Detect", "Coding", "Writing", "Analysis", "Summarization", "Education", "Business"]
    )
    selected_domain = None if domain_override == "Auto-Detect" else domain_override.lower()

    st.divider()

    # Quick Prompt Tips Sidebar Widget
    st.markdown("""
    <div class="glass-card" style="padding: 1rem; border-left: 3px solid #8b5cf6;">
        <h4 style="margin-top: 0; font-size: 0.95rem; color: #c084fc;">💡 Pro Prompting Tip</h4>
        <p style="font-size: 0.8rem; color: #d1d5db; margin-bottom: 0;">
            Specify clear constraints and structural output requirements (e.g. <i>"Respond in 3 bullet points with markdown tables"</i>) to dramatically reduce AI hallucinations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Input & Cache"):
        st.session_state.raw_input = ""
        st.rerun()

# ----------------------------------------------------------------------------
# SHARED PROCESSING FUNCTION
# ----------------------------------------------------------------------------
current_prompt = st.session_state.raw_input
rewrite_result = engine.rewrite_prompt(current_prompt, target_domain=selected_domain)

improved_prompt = rewrite_result["improved_prompt"]
detected_domain = rewrite_result["domain"]

orig_analysis = analyzer.analyze(current_prompt)
imp_analysis = analyzer.analyze(improved_prompt)

orig_tokens = tokenizer.tokenize(current_prompt)
imp_tokens = tokenizer.tokenize(improved_prompt)

orig_ascii = ascii_proc.analyze(current_prompt)
imp_ascii = ascii_proc.analyze(improved_prompt)

diff_result = utils.compute_diff(current_prompt, improved_prompt)

# Save into History if unique
if current_prompt and current_prompt != "Explain Python":
    history_item = {"orig": current_prompt, "imp": improved_prompt, "domain": detected_domain}
    if history_item not in st.session_state.history:
        st.session_state.history.insert(0, history_item)

# ----------------------------------------------------------------------------
# PAGE 1: HOME PAGE
# ----------------------------------------------------------------------------
if nav_option == "🏠 Home":
    st.markdown("""
    <div class="hero-container">
        <div class="badge badge-purple" style="margin-bottom: 12px;">AI Engineering & Prompt Design Platform</div>
        <h1 class="hero-title">Prompt Engineering Studio</h1>
        <p class="hero-subtitle">
            Transform simple, weak prompts into highly effective, production-grade instructions. 
            Learn prompt engineering rules, analyze token dynamics, inspect ASCII tables, and master LLM behavior interactively.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Quality Enhancement</div>
            <div class="metric-value-custom">+85%</div>
            <p style="font-size: 0.8rem; color: #9ca3af;">Avg Score Boost</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Rule Automation</div>
            <div class="metric-value-custom">9 Core</div>
            <p style="font-size: 0.8rem; color: #9ca3af;">Best Practice Rules</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Token Inspector</div>
            <div class="metric-value-custom">Tiktoken</div>
            <p style="font-size: 0.8rem; color: #9ca3af;">OpenAI cl100k Model</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Presets Library</div>
            <div class="metric-value-custom">30+</div>
            <p style="font-size: 0.8rem; color: #9ca3af;">Categorized Examples</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🌟 Feature Showcase")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown("""
        <div class="glass-card">
            <h3>✨ AI Prompt Rewriter</h3>
            <p>Automatically applies Role, Context, Goal, Output Format, Constraints, and Examples to instantly upgrade weak prompts.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with f_col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🧠 Deep Prompt Analyzer</h3>
            <p>Calculates Complexity, Specificity, Clarity, and Quality scores with interactive Plotly visual charts.</p>
        </div>
        """, unsafe_allow_html=True)

    with f_col3:
        st.markdown("""
        <div class="glass-card">
            <h3>📖 Interactive Masterclass</h3>
            <p>Understand Zero-Shot, Few-Shot, Chain-of-Thought, System Prompts, Tokens, and LLM temperature mechanics.</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PAGE 2: PROMPT REWRITER PAGE
# ----------------------------------------------------------------------------
elif nav_option == "✨ Prompt Rewriter":
    st.markdown("## ✨ AI Prompt Rewriter Studio")
    st.caption("Enter your draft prompt below to convert it into a structured, production-ready prompt.")

    # Form layout for prompt entry and rewriting
    with st.form(key="prompt_rewrite_form"):
        prompt_input = st.text_area(
            "Input Prompt (Weak / Draft Prompt):",
            value=st.session_state.raw_input,
            height=140,
            placeholder="e.g. Explain Python or Write code for web scraper..."
        )
        submit_clicked = st.form_submit_button("⚡ REWRITE PROMPT", type="primary", use_container_width=True)

    if submit_clicked:
        st.session_state.raw_input = prompt_input
        st.rerun()

    st.divider()

    # Display Side-by-Side Results
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("### ❌ Original Prompt")
        st.markdown(f"""
        <div class="prompt-box-original">
            {html.escape(current_prompt) if current_prompt else "<i>No prompt entered.</i>"}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Word Count:** {orig_analysis['word_count']} | **Est. Tokens:** {orig_analysis['estimated_tokens']}")

    with res_col2:
        st.markdown("### ✅ Strong Production Prompt")
        st.markdown(f"""
        <div class="prompt-box-improved">
            <pre style="white-space: pre-wrap; font-family: var(--font-body); color: #6ee7b7; margin: 0;">{html.escape(improved_prompt)}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Word Count:** {imp_analysis['word_count']} | **Est. Tokens:** {imp_analysis['estimated_tokens']}")

    # Copy & Export Buttons
    st.markdown("#### 📥 Actions & Exporters")
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

    with btn_col1:
        if st.button("📋 Copy Improved Prompt"):
            try:
                import pyperclip
                pyperclip.copy(improved_prompt)
                st.toast("Copied to clipboard!", icon="✅")
            except Exception:
                st.code(improved_prompt, language="markdown")
                st.toast("Selected code block above to copy!", icon="ℹ️")

    with btn_col2:
        txt_bytes = improved_prompt.encode('utf-8')
        st.download_button(
            label="📄 Export as TXT",
            data=txt_bytes,
            file_name="improved_prompt.txt",
            mime="text/plain"
        )

    with btn_col3:
        pdf_metrics = {
            "orig_quality": orig_analysis["quality_score"],
            "imp_quality": imp_analysis["quality_score"],
            "orig_words": orig_analysis["word_count"],
            "imp_words": imp_analysis["word_count"],
            "orig_chars": orig_analysis["char_count"],
            "imp_chars": imp_analysis["char_count"],
            "orig_tokens": orig_analysis["estimated_tokens"],
            "imp_tokens": imp_analysis["estimated_tokens"]
        }
        pdf_data = utils.generate_pdf(current_prompt, improved_prompt, pdf_metrics, detected_domain)
        st.download_button(
            label="📑 Export PDF Report",
            data=pdf_data,
            file_name="prompt_audit_report.pdf",
            mime="application/pdf"
        )

    with btn_col4:
        if st.button("⭐ Save to Favorites"):
            fav_item = {"prompt": improved_prompt, "domain": detected_domain}
            if fav_item not in st.session_state.favorites:
                st.session_state.favorites.append(fav_item)
                st.toast("Saved to Favorites!", icon="⭐")

    # Granular Rule Explanation Accordion
    st.divider()
    st.markdown("### 🛠️ Rule-by-Rule Improvement Breakdown")
    for r in rewrite_result["rules_applied"]:
        with st.expander(f"{r['status']} - {r['rule']}", expanded=True):
            st.write(r["description"])

# ----------------------------------------------------------------------------
# PAGE 3: PROMPT ANALYZER PAGE
# ----------------------------------------------------------------------------
elif nav_option == "🧠 Prompt Analyzer":
    st.markdown("## 🧠 Prompt Analytics & Metrics Engine")
    st.caption("Comprehensive qualitative and quantitative breakdown of prompt structure.")

    # Metric Cards Row
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Quality Score</div>
            <div class="metric-value-custom">{imp_analysis['quality_score']}%</div>
            <p style="font-size: 0.8rem; color: #34d399;">Before: {orig_analysis['quality_score']}%</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Specificity</div>
            <div class="metric-value-custom">{imp_analysis['specificity_score']}</div>
            <p style="font-size: 0.8rem; color: #a855f7;">Before: {orig_analysis['specificity_score']}</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Clarity</div>
            <div class="metric-value-custom">{imp_analysis['clarity_score']}</div>
            <p style="font-size: 0.8rem; color: #60a5fa;">Before: {orig_analysis['clarity_score']}</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Est. Tokens</div>
            <div class="metric-value-custom">{imp_analysis['estimated_tokens']}</div>
            <p style="font-size: 0.8rem; color: #fbbf24;">Before: {orig_analysis['estimated_tokens']}</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col5:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="metric-label-custom">Reading Time</div>
            <div class="metric-value-custom">{imp_analysis['reading_time_sec']}s</div>
            <p style="font-size: 0.8rem; color: #f472b6;">Words: {imp_analysis['word_count']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("### 🕸️ Quality & Metric Radar")
        radar_fig = visualizer.create_radar_chart(orig_analysis, imp_analysis)
        st.plotly_chart(radar_fig, use_container_width=True)

    with chart_col2:
        st.markdown("### 📊 Metrics Count Comparison")
        bar_fig = visualizer.create_comparison_bar(orig_analysis, imp_analysis)
        st.plotly_chart(bar_fig, use_container_width=True)

    # Structural Checklist Matrix
    st.markdown("### 🏗️ Structural Element Audit")
    element_cols = st.columns(2)
    with element_cols[0]:
        st.markdown("#### Original Prompt Checklist")
        for elem, status in orig_analysis["structural_elements"].items():
            icon = "✅" if status else "❌"
            st.write(f"{icon} **{elem}**")
    with element_cols[1]:
        st.markdown("#### Improved Prompt Checklist")
        for elem, status in imp_analysis["structural_elements"].items():
            icon = "✅" if status else "❌"
            st.write(f"{icon} **{elem}**")

# ----------------------------------------------------------------------------
# PAGE 4: TOKENIZATION PAGE
# ----------------------------------------------------------------------------
elif nav_option == "🔤 Tokenization":
    st.markdown("## 🔤 LLM Tokenization Inspector")
    st.caption("Displays exact sub-word tokenization produced by OpenAI tiktoken (cl100k_base).")

    # Token summary metrics
    tok_col1, tok_col2, tok_col3, tok_col4 = st.columns(4)
    with tok_col1:
        st.metric("Total Tokens (Improved)", imp_tokens["total_tokens"], delta=f"+{imp_tokens['total_tokens'] - orig_tokens['total_tokens']}")
    with tok_col2:
        st.metric("Avg Token Length", f"{imp_tokens['avg_token_len']} chars")
    with tok_col3:
        st.metric("Unique Tokens", imp_tokens["unique_tokens"])
    with tok_col4:
        st.metric("Repeat Ratio", f"{imp_tokens['repeat_ratio']}%")

    st.divider()

    t_tab1, t_tab2 = st.columns(2)
    with t_tab1:
        st.markdown("### ❌ Original Prompt Tokens")
        if not orig_tokens["token_df"].empty:
            st.dataframe(orig_tokens["token_df"], use_container_width=True, height=350)
            st.markdown("#### Token Visualization")
            colored_tokens = "".join([f'<span class="badge badge-purple" style="margin:2px;">{t}</span>' for t in orig_tokens["tokens_list"]])
            st.markdown(colored_tokens, unsafe_allow_html=True)
        else:
            st.info("Enter text to view tokenization.")

    with t_tab2:
        st.markdown("### ✅ Improved Prompt Tokens")
        if not imp_tokens["token_df"].empty:
            st.dataframe(imp_tokens["token_df"], use_container_width=True, height=350)
            st.markdown("#### Token Visualization")
            colored_tokens = "".join([f'<span class="badge badge-green" style="margin:2px;">{t}</span>' for t in imp_tokens["tokens_list"][:40]])
            st.markdown(colored_tokens + ("..." if len(imp_tokens["tokens_list"]) > 40 else ""), unsafe_allow_html=True)
        else:
            st.info("Enter text to view tokenization.")

    st.divider()
    st.markdown("### 📊 Token Length Distribution Chart")
    dist_fig = visualizer.create_token_length_distribution(imp_tokens["token_df"])
    st.plotly_chart(dist_fig, use_container_width=True)

# ----------------------------------------------------------------------------
# PAGE 5: ASCII ANALYZER PAGE
# ----------------------------------------------------------------------------
elif nav_option == "🔠 ASCII Analyzer":
    st.markdown("## 🔠 Character-Level ASCII Analyzer")
    st.caption("Inspects ASCII decimal, hex, binary, and category codes for every character in the prompt.")

    a_col1, a_col2 = st.columns(2)
    with a_col1:
        st.markdown("### ❌ Original Prompt ASCII Table")
        if not orig_ascii["ascii_df"].empty:
            st.dataframe(orig_ascii["ascii_df"], use_container_width=True, height=380)
        else:
            st.info("No input provided.")

    with a_col2:
        st.markdown("### ✅ Improved Prompt ASCII Table")
        if not imp_ascii["ascii_df"].empty:
            st.dataframe(imp_ascii["ascii_df"], use_container_width=True, height=380)
        else:
            st.info("No improved prompt generated.")

    st.divider()
    st.markdown("### 📈 ASCII Distribution Histogram")
    ascii_hist = visualizer.create_ascii_distribution(imp_ascii["ascii_df"])
    st.plotly_chart(ascii_hist, use_container_width=True)

# ----------------------------------------------------------------------------
# PAGE 6: PROMPT COMPARISON PAGE
# ----------------------------------------------------------------------------
elif nav_option == "📊 Prompt Comparison":
    st.markdown("## 📊 Side-by-Side Prompt Diff & Comparison")
    st.caption("Highlights exact word additions, deletions, and structural enhancements.")

    diff_col1, diff_col2, diff_col3, diff_col4 = st.columns(4)
    with diff_col1:
        st.metric("Added Words", f"+{diff_result['added_words']}")
    with diff_col2:
        st.metric("Removed / Replaced", f"-{diff_result['removed_words']}")
    with diff_col3:
        st.metric("Detail Increase", f"+{diff_result['detail_increase_pct']}%")
    with diff_col4:
        score_diff = round(imp_analysis['quality_score'] - orig_analysis['quality_score'], 1)
        st.metric("Score Delta", f"+{score_diff}%", delta=f"{score_diff}%")

    st.divider()
    st.markdown("### 🔍 Inline Word-Level Diff")
    st.markdown(f"""
    <div class="glass-card" style="font-family: var(--font-body); font-size: 1.05rem; line-height: 1.8;">
        {diff_result['diff_html']}
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📈 Keyword Treemap Analysis")
    treemap_fig = visualizer.create_word_freq_treemap(improved_prompt)
    st.plotly_chart(treemap_fig, use_container_width=True)

# ----------------------------------------------------------------------------
# PAGE 7: LEARN PROMPT ENGINEERING PAGE
# ----------------------------------------------------------------------------
elif nav_option == "📖 Learn Prompt Engineering":
    st.markdown("## 📖 Prompt Engineering Masterclass")
    st.caption("A beginner-to-advanced visual guide explaining fundamental concepts of AI Prompting.")

    topics = [
        ("🧠 What is Prompt Engineering?", "Prompt Engineering is the art and science of structuring text inputs (prompts) to guide Generative AI models (LLMs) toward producing accurate, relevant, and high-quality outputs."),
        ("⚡ Why Prompt Engineering Matters", "LLMs do not have human intuition. Clear role definition, contextual framing, explicit constraints, and target formatting eliminate ambiguity and reduce hallucinations."),
        ("🔤 How LLMs Process Text (Tokens)", "LLMs do not read words directly. They break text into sub-word units called **Tokens**. 1000 tokens ≈ 750 English words. Understanding token efficiency helps optimize cost and context windows."),
        ("🌡️ LLM Temperature & Top-P", "Temperature controls output randomness. **0.0 - 0.3**: Deterministic, analytical, factual. **0.7 - 1.0**: Creative, varied, exploratory."),
        ("🎭 Role Prompting", "Assigning a specific persona (e.g. *'Act as a Senior Python Architect'*) sets the model's vocabulary, reasoning depth, and standard of quality."),
        ("🎯 Zero-Shot vs Few-Shot Prompting", "**Zero-Shot**: Direct instruction without examples. **Few-Shot**: Providing 2-3 input/output examples inside the prompt to guide output structure."),
        ("🔗 Chain-of-Thought (CoT)", "Asking the model to *'Think step by step'* forces explicit reasoning before outputting the final answer, dramatically increasing accuracy in logic and math.")
    ]

    for title, desc in topics:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: #c084fc; margin-top: 0;">{title}</h3>
            <p style="color: #e2e8f0; font-size: 0.98rem; line-height: 1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PAGE 8: PROMPT EXAMPLES PAGE
# ----------------------------------------------------------------------------
elif nav_option == "💡 Prompt Examples":
    st.markdown("## 💡 Prompt Engineering Examples Library (30+ Presets)")
    st.caption("Click any example to load it directly into the Prompt Rewriter Studio.")

    examples_list = utils.get_30_examples()
    categories = list(set([e["category"] for e in examples_list]))
    
    selected_cat = st.selectbox("Filter Category:", ["All Categories"] + categories)
    
    filtered_examples = examples_list if selected_cat == "All Categories" else [e for e in examples_list if e["category"] == selected_cat]

    for ex in filtered_examples:
        with st.expander(f"[{ex['category']}] #{ex['id']}: {ex['weak']}", expanded=False):
            ex_col1, ex_col2 = st.columns(2)
            with ex_col1:
                st.markdown(f"**❌ Weak Prompt:**\n`{ex['weak']}`")
            with ex_col2:
                st.markdown(f"**✅ Strong Prompt:**\n`{ex['strong']}`")
            
            if st.button(f"🚀 Load Example #{ex['id']} into Rewriter", key=f"ex_btn_{ex['id']}"):
                st.session_state.raw_input = ex["weak"]
                st.toast(f"Loaded Example #{ex['id']}!", icon="🚀")
                st.rerun()

# ----------------------------------------------------------------------------
# PAGE 9: ABOUT PAGE
# ----------------------------------------------------------------------------
elif nav_option == "ℹ About":
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 2.5rem;">
        <h1 style="background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Prompt Engineering Studio v2.0
        </h1>
        <p style="font-size: 1.1rem; color: #9ca3af; max-width: 650px; margin: 0 auto 1.5rem auto;">
            Designed as an intuitive, high-performance teaching and production environment for AI engineers, prompt designers, and developers.
        </p>
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <span class="badge badge-purple">Python 3.10+</span>
            <span class="badge badge-green">Streamlit</span>
            <span class="badge badge-cyan">Plotly</span>
            <span class="badge badge-amber">Tiktoken</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
