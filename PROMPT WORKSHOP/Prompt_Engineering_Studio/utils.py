"""
Prompt Engineering Studio - Utilities & Exporters Engine
Provides difflib word comparison, PDF export generation, text formatting,
and 30+ comprehensive Prompt Engineering educational examples.
"""

import difflib
import re
import io
import html

class PromptUtils:
    """
    Helper utilities for diff calculation, export rendering, and prompt examples repository.
    """

    def __init__(self):
        pass

    @staticmethod
    def compute_diff(orig_text: str, imp_text: str) -> dict:
        """
        Calculates word-level additions, deletions, modifications, and renders HTML diff.
        """
        orig_words = orig_text.split()
        imp_words = imp_text.split()

        matcher = difflib.SequenceMatcher(None, orig_words, imp_words)
        
        added_count = 0
        removed_count = 0
        html_chunks = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                html_chunks.append(" ".join(html.escape(w) for w in orig_words[i1:i2]))
            elif tag == 'replace':
                del_str = " ".join(html.escape(w) for w in orig_words[i1:i2])
                add_str = " ".join(html.escape(w) for w in imp_words[j1:j2])
                html_chunks.append(f'<span class="diff-del">{del_str}</span> <span class="diff-add">{add_str}</span>')
                removed_count += (i2 - i1)
                added_count += (j2 - j1)
            elif tag == 'delete':
                del_str = " ".join(html.escape(w) for w in orig_words[i1:i2])
                html_chunks.append(f'<span class="diff-del">{del_str}</span>')
                removed_count += (i2 - i1)
            elif tag == 'insert':
                add_str = " ".join(html.escape(w) for w in imp_words[j1:j2])
                html_chunks.append(f'<span class="diff-add">{add_str}</span>')
                added_count += (j2 - j1)

        diff_html = " ".join(html_chunks)
        word_count_orig = max(len(orig_words), 1)
        word_count_imp = max(len(imp_words), 1)
        
        increase_in_detail_pct = round(((word_count_imp - word_count_orig) / word_count_orig) * 100, 1)

        return {
            "diff_html": diff_html,
            "added_words": added_count,
            "removed_words": removed_count,
            "word_count_orig": word_count_orig,
            "word_count_imp": word_count_imp,
            "detail_increase_pct": max(increase_in_detail_pct, 0.0)
        }

    @staticmethod
    def generate_pdf(orig_prompt: str, imp_prompt: str, metrics: dict, domain: str) -> bytes:
        """
        Generates a PDF document summary of the prompt rewriting session.
        """
        buffer = io.BytesIO()
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                'DocTitle',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#6366f1'),
                spaceAfter=12
            )
            h2_style = ParagraphStyle(
                'DocH2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#a855f7'),
                spaceBefore=10,
                spaceAfter=6
            )
            body_style = styles['BodyText']

            story.append(Paragraph("Prompt Engineering Studio - Audit Report", title_style))
            story.append(Paragraph(f"<b>Domain:</b> {domain.capitalize()} | <b>Generated Report</b>", body_style))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Original Prompt", h2_style))
            story.append(Paragraph(html.escape(orig_prompt).replace('\n', '<br/>'), body_style))
            story.append(Spacer(1, 12))

            story.append(Paragraph("Improved Production Prompt", h2_style))
            story.append(Paragraph(html.escape(imp_prompt).replace('\n', '<br/>'), body_style))
            story.append(Spacer(1, 14))

            # Metrics Table
            story.append(Paragraph("Prompt Quality Metrics", h2_style))
            data = [
                ["Metric", "Original Value", "Improved Value"],
                ["Quality Score", f"{metrics.get('orig_quality', 0)}%", f"{metrics.get('imp_quality', 0)}%"],
                ["Word Count", str(metrics.get('orig_words', 0)), str(metrics.get('imp_words', 0))],
                ["Character Count", str(metrics.get('orig_chars', 0)), str(metrics.get('imp_chars', 0))],
                ["Estimated Tokens", str(metrics.get('orig_tokens', 0)), str(metrics.get('imp_tokens', 0))]
            ]
            t = Table(data, colWidths=[180, 150, 150])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
            ]))
            story.append(t)

            doc.build(story)
            pdf = buffer.getvalue()
            buffer.close()
            return pdf
        except Exception:
            # Fallback simple text bytes if reportlab has any issue
            fallback_text = f"PROMPT ENGINEERING STUDIO REPORT\n\nORIGINAL:\n{orig_prompt}\n\nIMPROVED:\n{imp_prompt}"
            return fallback_text.encode('utf-8')

    @staticmethod
    def get_30_examples() -> list:
        """
        Returns 30 comprehensive, categorized examples of weak vs strong prompts.
        """
        examples = [
            # Coding (1-5)
            {"id": 1, "category": "Coding", "weak": "Explain Python", "strong": "Explain Python fundamentals for absolute beginners. Cover history, key features, variables, data types, functions, loops, and OOP with step-by-step code snippets."},
            {"id": 2, "category": "Coding", "weak": "Write code", "strong": "Write a modular Python script to fetch stock prices from a REST API, parse JSON response into a pandas DataFrame, and handle network connection errors gracefully."},
            {"id": 3, "category": "Coding", "weak": "Fix bug in script", "strong": "Act as a Senior Python Debugger. Analyze the following code snippet for memory leaks and off-by-one errors. Provide refactored code and an inline explanation of the fix."},
            {"id": 4, "category": "Coding", "weak": "Create SQL query", "strong": "Write an optimized PostgreSQL query joining orders and customers tables to aggregate monthly revenue per region for 2025. Include subqueries and indexes."},
            {"id": 5, "category": "Coding", "weak": "React component", "strong": "Create a reusable React (TypeScript) navbar component with dark mode toggle, dynamic dropdown menus, responsive hamburger menu, and TailwindCSS styling."},

            # Data Analysis & Science (6-10)
            {"id": 6, "category": "Data Analysis", "weak": "Analyze dataset", "strong": "Act as a Lead Data Scientist. Analyze a CSV dataset containing customer churn. Outline missing value handling, feature engineering, baseline models, and evaluation metrics."},
            {"id": 7, "category": "Data Analysis", "weak": "What is machine learning?", "strong": "Explain machine learning concepts distinguishing Supervised, Unsupervised, and Reinforcement learning with real-world industry applications and algorithm examples."},
            {"id": 8, "category": "Data Analysis", "weak": "Plot graph", "strong": "Write a Python Plotly script to generate an interactive 3D scatter plot of user engagement metrics with custom tooltips, legend, and dark theme palette."},
            {"id": 9, "category": "Data Analysis", "weak": "Clean data", "strong": "Provide a step-by-step Pandas data cleaning pipeline handling duplicate entries, date formatting, outlier detection using IQR, and categorical encoding."},
            {"id": 10, "category": "Data Analysis", "weak": "SQL vs NoSQL", "strong": "Compare SQL vs NoSQL databases across scalability, ACID compliance, schema flexibility, and query performance. Include a decision matrix table."},

            # Summarization & PDF (11-15)
            {"id": 11, "category": "Summarization", "weak": "Summarize PDF", "strong": "Summarize the uploaded financial report PDF into an executive summary. Group findings by Key Highlights, Financial Growth, Risk Factors, and Strategic Objectives."},
            {"id": 12, "category": "Summarization", "weak": "TLDR article", "strong": "Synthesize this 5-page AI research paper into a 3-bullet point executive TL;DR, followed by a breakdown of methodology, experimental benchmark results, and future work."},
            {"id": 13, "category": "Summarization", "weak": "Meeting notes summary", "strong": "Convert raw transcript meeting notes into actionable minutes including: Attendees, Decisions Made, Action Items (with assigned owners & deadlines), and Open Questions."},
            {"id": 14, "category": "Summarization", "weak": "Book summary", "strong": "Provide a comprehensive chapter-by-chapter core concept breakdown of 'Atomic Habits' by James Clear, emphasizing actionable mindset shifts and implementation strategies."},
            {"id": 15, "category": "Summarization", "weak": "Condense email thread", "strong": "Condense a 10-email customer support thread into a short issue resolution log detailing: Problem statement, Troubleshooting steps taken, and Final resolution status."},

            # Writing & Content (16-20)
            {"id": 16, "category": "Writing", "weak": "Write cold email", "strong": "Draft a personalized, high-converting B2B SaaS cold outreach email targetting Chief Technology Officers. Keep length under 150 words with a clear, low-friction CTA."},
            {"id": 17, "category": "Writing", "weak": "Write blog post", "strong": "Write a 1200-word SEO-optimized blog post titled 'The Future of Generative AI in 2026'. Include H2/H3 headers, meta description, key takeaways, and internal link suggestions."},
            {"id": 18, "category": "Writing", "weak": "Improve resume bullet", "strong": "Rewrite my resume experience bullets using the Google XYZ action formula ('Accomplished [X] as measured by [Y], by doing [Z]') tailored for a Senior Full Stack Engineer role."},
            {"id": 19, "category": "Writing", "weak": "Product launch post", "strong": "Create an engaging LinkedIn announcement post launching our new AI Prompt Rewriter app. Use bold hooks, bullet points, relevant hashtags, and call to action."},
            {"id": 20, "category": "Writing", "weak": "Write cover letter", "strong": "Write a compelling, professional cover letter for an AI Prompt Engineer application emphasizing LLM evaluation expertise, python development skills, and passion for AI UX."},

            # Business & Strategy (21-25)
            {"id": 21, "category": "Business", "weak": "Business plan", "strong": "Create an executive business plan outline for an AI-powered SaaS startup including Value Proposition, Market Analysis, Revenue Model, Go-To-Market Strategy, and Funding Requirements."},
            {"id": 22, "category": "Business", "weak": "Competitor analysis", "strong": "Conduct a SWOT analysis comparing top AI coding assistants (GitHub Copilot, Cursor, Antigravity, Claude Code). Present results in a clear comparison matrix."},
            {"id": 23, "category": "Business", "weak": "Marketing strategy", "strong": "Formulate a 90-day growth marketing strategy for an educational tech platform combining content marketing, organic search, referral programs, and email nurturing sequences."},
            {"id": 24, "category": "Business", "weak": "Pitch deck outline", "strong": "Structure a 10-slide startup pitch deck for seed investors, detailing problem, solution, market size, product demo, business model, traction, and team background."},
            {"id": 25, "category": "Business", "weak": "Customer survey", "strong": "Design a 5-question customer satisfaction survey assessing user experience, feature demand, NPS score, and qualitative feedback for an AI productivity app."},

            # Education & Science (26-30)
            {"id": 26, "category": "Education", "weak": "Explain Quantum Computing", "strong": "Explain Quantum Computing to a high school student using intuitive analogies (e.g. coin flip vs superposition). Cover qubits, entanglement, quantum speedup, and cryptography."},
            {"id": 27, "category": "Education", "weak": "What is Docker?", "strong": "Explain Docker containers vs Virtual Machines using a shipping container analogy. Detail Dockerfile, Images, Containers, and Docker Compose in clear simple language."},
            {"id": 28, "category": "Education", "weak": "How APIs work", "strong": "Explain REST APIs to a non-technical manager using a restaurant waiter analogy. Define Endpoints, HTTP Methods (GET/POST), Request Payloads, and Response Codes."},
            {"id": 29, "category": "Education", "weak": "Explain Neural Networks", "strong": "Explain artificial neural networks from scratch. Define perceptrons, weights, biases, activation functions (ReLU, Sigmoid), and backpropagation with diagrams."},
            {"id": 30, "category": "Education", "weak": "Blockchain simple", "strong": "Explain blockchain technology through a decentralized shared ledger notebook analogy. Explain hashing, blocks, mining, consensus, and smart contracts step-by-step."}
        ]
        return examples
