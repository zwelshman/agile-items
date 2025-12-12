"""
Agile Work Item Converter
BHF Data Science Centre
Transforms rough work items into structured agile descriptions using Claude API.
"""

import streamlit as st
import anthropic
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Agile Work Item Converter | BHF DSC",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean, legible CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bhf-red: #C8102E;
    --bhf-red-dark: #A00D24;
    --color-text: #1a1a1a;
    --color-text-muted: #555555;
    --color-bg: #ffffff;
    --color-border: #e0e0e0;
    --radius: 8px;
}

/* Base */
.stApp {
    background: var(--color-bg);
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--color-text);
}

/* Hide sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Header */
.app-header {
    border-bottom: 3px solid var(--bhf-red);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}

.app-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 0.5rem 0;
}

.app-header p {
    font-size: 1rem;
    color: var(--color-text-muted);
    margin: 0;
}

.bhf-badge {
    display: inline-block;
    background: var(--bhf-red);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    margin-bottom: 0.75rem;
}

/* Form elements */
.stTextArea textarea {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.5 !important;
    border: 2px solid var(--color-border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: var(--bhf-red) !important;
    box-shadow: none !important;
}

/* Labels */
.stTextArea label, .stSelectbox label {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--color-text) !important;
    margin-bottom: 0.5rem !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    background: var(--bhf-red) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: var(--bhf-red-dark) !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    background: white !important;
    color: var(--bhf-red) !important;
    border: 2px solid var(--bhf-red) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem 1rem !important;
}

.stDownloadButton > button:hover {
    background: #fef2f2 !important;
}

/* Section headers */
.section-header {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text);
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--color-border);
}

/* Markdown output */
.stMarkdown {
    font-size: 1rem !important;
    line-height: 1.6 !important;
}

.stMarkdown h2 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    color: var(--color-text) !important;
    margin-top: 1.5rem !important;
    margin-bottom: 0.5rem !important;
}

.stMarkdown p {
    margin-bottom: 0.75rem !important;
}

.stMarkdown ul {
    margin: 0.5rem 0 1rem 0 !important;
    padding-left: 1.5rem !important;
}

.stMarkdown li {
    margin-bottom: 0.35rem !important;
}

/* Placeholder */
.placeholder-box {
    background: #f8f8f8;
    border: 2px dashed #d0d0d0;
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    color: var(--color-text-muted);
}

.placeholder-box p {
    margin: 0;
    font-size: 1rem;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--color-text) !important;
    background: #f8f8f8 !important;
}

/* Footer */
.app-footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--color-border);
    text-align: center;
}

.app-footer p {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    margin: 0;
}

.app-footer a {
    color: var(--bhf-red);
    text-decoration: none;
}

/* Hide default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# System prompt
SYSTEM_PROMPT = """You are an agile coach helping transform rough work items into clear, actionable agile descriptions. 

For each work item provided, produce a well-structured output following this exact format:

## Title
A concise, action-oriented title (max 10 words)

## User Story
As a [specific user/role], I want [goal/desire], so that [benefit/value].

## Description
2-3 sentences providing context and scope. Include what's in and out of scope if relevant.

## Acceptance Criteria
- [ ] Criterion 1 (specific, testable)
- [ ] Criterion 2
- [ ] Criterion 3
(Add more as needed, aim for 3-5)

## Technical Notes
Brief technical considerations, dependencies, or implementation hints (if applicable).

## Definition of Done
- Code complete and reviewed
- Tests passing
- Documentation updated (if applicable)
- Deployed to [environment]

## Suggested Story Points
Estimate using Fibonacci (1, 2, 3, 5, 8, 13) with brief rationale.

---

Guidelines:
1. Be specific - Replace vague terms with concrete actions
2. Focus on value - Always articulate the "why"
3. Make it testable - Acceptance criteria should be binary (done/not done)
4. Right-size it - If >8 points, suggest splitting into smaller items
5. Identify dependencies - Flag blockers or related work
6. Use domain language - Match the team's terminology when context is provided"""


def get_api_key() -> Optional[str]:
    """Get API key from Streamlit secrets."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None


def get_agile_description(work_item: str, context: Optional[str], api_key: str) -> str:
    """Generate an agile description from a work item using Claude API."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        user_message = f"Work Item:\n{work_item}"
        if context:
            user_message = f"Team/Project Context:\n{context}\n\n{user_message}"
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return message.content[0].text
        
    except anthropic.AuthenticationError:
        return "**Error:** Invalid API key. Check your Streamlit secrets."
    except anthropic.RateLimitError:
        return "**Error:** Rate limit exceeded. Please wait and try again."
    except Exception as e:
        return f"**Error:** {str(e)}"


def main():
    api_key = get_api_key()
    
    # Header
    st.markdown("""
    <div class="app-header">
        <span class="bhf-badge">BHF Data Science Centre</span>
        <h1>Agile Work Item Converter</h1>
        <p>Transform rough work items into structured agile descriptions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not api_key:
        st.error("API key not found. Add ANTHROPIC_API_KEY to your Streamlit secrets.")
        st.stop()
    
    # Input section
    work_item = st.text_area(
        "Work Item",
        placeholder="Enter your work item here. Examples:\n\n• Fix the slow phenotype search\n• Add ICD-10 validation to the toolkit\n• Users getting timeout errors on large queries",
        height=150
    )
    
    with st.expander("Add team context (optional)"):
        team_context = st.text_area(
            "Context",
            placeholder="e.g., Healthcare data science team. Stack: Python/PySpark/Databricks. Working with NHS datasets.",
            height=100,
            label_visibility="collapsed"
        )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        generate = st.button("Generate", use_container_width=True)
    with col2:
        if st.button("Clear", use_container_width=True):
            if 'output' in st.session_state:
                del st.session_state['output']
            st.rerun()
    
    # Generate output
    if generate and work_item:
        with st.spinner("Generating..."):
            context = team_context if 'team_context' in dir() and team_context else None
            st.session_state['output'] = get_agile_description(work_item, context, api_key)
    
    # Output section
    st.markdown('<p class="section-header">Output</p>', unsafe_allow_html=True)
    
    if 'output' in st.session_state:
        st.markdown(st.session_state['output'])
        st.download_button(
            "Download as Markdown",
            st.session_state['output'],
            "agile_description.md",
            "text/markdown"
        )
    else:
        st.markdown("""
        <div class="placeholder-box">
            <p>Enter a work item and click Generate</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="app-footer">
        <p>Built with Claude API • <a href="https://bhfdatasciencecentre.org">BHF Data Science Centre</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
