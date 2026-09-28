"""
Prompt Engineering Studio - Prompt Engine Core
Provides multi-rule automatic prompt enhancement, domain detection, 
and rule breakdown explanations.
"""

import re

class PromptEngine:
    """
    Intelligent Prompt Engineering System that rewrites raw/weak prompts
    into highly effective, structured, context-rich production prompts.
    """

    DOMAINS = {
        "coding": ["python", "code", "programming", "function", "bug", "script", "sql", "api", "react", "html", "algorithm", "developer", "java", "css"],
        "writing": ["write", "essay", "blog", "article", "copy", "email", "letter", "poem", "content", "story"],
        "analysis": ["analyze", "data", "metrics", "chart", "evaluate", "compare", "trend", "report", "insights"],
        "summarization": ["summarize", "summary", "pdf", "transcript", "bullets", "key points", "tl;dr", "condense"],
        "education": ["explain", "teach", "learn", "concept", "beginner", "tutorial", "guide", "difference", "what is", "how to"],
        "business": ["marketing", "sales", "proposal", "pitch", "strategy", "roadmap", "plan", "business"]
    }

    def __init__(self):
        pass

    def detect_domain(self, prompt: str) -> str:
        """Detect the domain of the prompt based on keyword frequency."""
        prompt_lower = prompt.lower()
        scores = {}
        for domain, keywords in self.DOMAINS.items():
            score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', prompt_lower))
            scores[domain] = score
        
        max_domain = max(scores, key=scores.get)
        return max_domain if scores[max_domain] > 0 else "general"

    def rewrite_prompt(self, raw_prompt: str, target_role: str = None, target_domain: str = None) -> dict:
        """
        Rewrite a weak prompt into a structured, highly optimized prompt 
        following standard prompt engineering best practices.
        """
        if not raw_prompt or not raw_prompt.strip():
            return {
                "original_prompt": "",
                "improved_prompt": "",
                "domain": "general",
                "rules_applied": []
            }

        clean_prompt = raw_prompt.strip()
        domain = target_domain if target_domain else self.detect_domain(clean_prompt)
        
        # 1. Role Assignment
        role = target_role if target_role else self._get_role_for_domain(domain, clean_prompt)
        
        # 2. Context & Background
        context = self._build_context(clean_prompt, domain)
        
        # 3. Objective & Goal
        goal = self._build_goal(clean_prompt, domain)
        
        # 4. Output Formatting & Structure
        output_format = self._build_output_format(domain)
        
        # 5. Constraints & Exclusions
        constraints = self._build_constraints(domain)
        
        # 6. Illustrative Examples
        examples = self._build_examples(domain)
        
        # 7. Detail & Tone Specification
        detail_spec = self._build_detail_level(domain)

        # Assemble the Strong Structured Prompt
        structured_prompt = f"""### SYSTEM ROLE:
{role}

### CONTEXT & BACKGROUND:
{context}

### PRIMARY OBJECTIVE:
{goal}

### OUTPUT FORMAT REQUIREMENTS:
{output_format}

### CONSTRAINTS & BEST PRACTICES:
{constraints}

### ILLUSTRATIVE EXAMPLES / TEMPLATE:
{examples}

### DETAIL LEVEL & TONE:
{detail_spec}"""

        # Rule applications breakdown
        rules_applied = [
            {"rule": "Role Definition", "description": f"Assigned explicit persona: '{role}' to steer model perspective.", "status": "✔ Applied"},
            {"rule": "Context Framing", "description": "Added background situational context to anchor the response domain.", "status": "✔ Applied"},
            {"rule": "Goal Specificity", "description": "Transformed vague instruction into a concrete, measurable core objective.", "status": "✔ Applied"},
            {"rule": "Structured Output Format", "description": "Specified Markdown headers, bullet points, and code block expectations.", "status": "✔ Applied"},
            {"rule": "Constraints & Guardrails", "description": "Enforced negative constraints, edge-case coverage, and tone restrictions.", "status": "✔ Applied"},
            {"rule": "Few-Shot / Template Examples", "description": "Included structured formatting guidelines and example output expectations.", "status": "✔ Applied"},
            {"rule": "Detail Level & Clarity", "description": "Explicitly requested step-by-step breakdown and beginner-friendly depth.", "status": "✔ Applied"}
        ]

        return {
            "original_prompt": clean_prompt,
            "improved_prompt": structured_prompt.strip(),
            "domain": domain,
            "role": role,
            "rules_applied": rules_applied
        }

    def _get_role_for_domain(self, domain: str, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "python" in prompt_lower:
            return "Senior Python Engineer, Software Architect, and Computer Science Educator with 10+ years of production experience."
        
        roles = {
            "coding": "Senior Software Architect and Technical Lead with expertise in clean code, design patterns, and debugging.",
            "writing": "Expert Content Strategist, Senior Copywriter, and Communications Specialist.",
            "analysis": "Lead Data Scientist and Quantitative Analyst skilled in statistical modeling and business metrics.",
            "summarization": "Executive Assistant and Information Synthesis Specialist.",
            "education": "Expert University Instructor and Technical Communicator known for simplifying complex topics.",
            "business": "Management Consultant and Strategic Product Specialist.",
            "general": "World-class Domain Specialist and AI Assistant with comprehensive subject knowledge."
        }
        return roles.get(domain, roles["general"])

    def _build_context(self, prompt: str, domain: str) -> str:
        return f"The user requires a thorough, production-grade resolution for the task: '{prompt}'. Target audience needs a clear, structured, and highly practical resource with zero jargon ambiguity."

    def _build_goal(self, prompt: str, domain: str) -> str:
        if domain == "coding":
            return f"Provide a complete, bug-free, fully documented implementation addressing: '{prompt}'. Cover architecture, syntax, line-by-line comments, potential edge cases, and runtime efficiency."
        elif domain == "education":
            return f"Explain the core concepts of '{prompt}' step-by-step in a beginner-friendly manner. Cover fundamental principles, real-world analogies, code/text examples, and practical applications."
        elif domain == "summarization":
            return f"Provide an executive summary of '{prompt}' highlighting key takeaways, actionable insights, and structured bullet points."
        else:
            return f"Deliver an in-depth, clear, and comprehensive response addressing '{prompt}', covering key principles, actionable advice, and step-by-step execution details."

    def _build_output_format(self, domain: str) -> str:
        return """1. **Executive Overview / TL;DR**: A 2-3 sentence high-level summary.
2. **Core Concepts & Deep Dive**: Use clear markdown headers (H2/H3) and organized sections.
3. **Practical Examples**: Include executable code blocks (with language tags) or structured text examples.
4. **Best Practices & Common Pitfalls**: Highlight anti-patterns, traps to avoid, and performance tips.
5. **Conclusion & Key Takeaways**: Brief recap with recommended next steps."""

    def _build_constraints(self, domain: str) -> str:
        return """- **Clarity First**: Avoid unexplained jargon or overly dense academic prose.
- **Accurate & Tested**: Ensure all code/examples are syntactically sound and up-to-date.
- **Structured**: Use bold text for key terms, bullet points for lists, and callout sections for tips.
- **No Hallucinations**: State limitations explicitly if assumptions must be made."""

    def _build_examples(self, domain: str) -> str:
        if domain == "coding":
            return """```python
# Standard Documented Pattern Example:
def calculate_metrics(data: list) -> dict:
    \"\"\"Calculates summary metrics for input data list.\"\"\"
    if not data:
        return {"count": 0, "mean": 0.0}
    return {"count": len(data), "mean": sum(data) / len(data)}
```"""
        else:
            return """> **Example Section Structure**:
> - **Concept**: Simple definition with an intuitive real-world analogy.
> - **Application**: Concrete scenario demonstrating how and when to use it."""

    def _build_detail_level(self, domain: str) -> str:
        return "Comprehensive and beginner-friendly depth. Provide thorough explanations with concise, well-formatted snippets."
