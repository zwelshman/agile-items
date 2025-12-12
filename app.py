"""
Agile Work Item Converter
Transforms rough work items into structured agile descriptions using Claude API.
"""

import streamlit as st
import anthropic
from typing import Optional

st.set_page_config(
    page_title="Agile Work Item Converter",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Blue-green gradient theme with legible text
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --teal-600: #0d9488;
    --teal-500: #14b8a6;
    --teal-400: #2dd4bf;
    --cyan-500: #06b6d4;
    --cyan-400: #22d3ee;
    --slate-900: #0f172a;
    --slate-700: #334155;
    --slate-600: #475569;
    --slate-500: #64748b;
    --slate-200: #e2e8f0;
    --slate-100: #f1f5f9;
    --slate-50: #f8fafc;
    --white: #ffffff;
    --radius: 12px;
}

/* Base */
.stApp {
    background: linear-gradient(135deg, var(--slate-50) 0%, #ecfeff 50%, #f0fdfa 100%);
    min-height: 100vh;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hide sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Header card */
.header-card {
    background: linear-gradient(135deg, var(--teal-600) 0%, var(--cyan-500) 100%);
    border-radius: var(--radius);
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px -10px rgba(13, 148, 136, 0.3);
}

.header-card h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--white);
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.02em;
}

.header-card p {
    font-size: 1.05rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    font-weight: 400;
}

/* Main card */
.main-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid var(--slate-200);
}

/* Labels */
.input-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--slate-700);
    margin-bottom: 0.5rem;
    display: block;
}

/* Text areas */
.stTextArea textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    color: var(--slate-900) !important;
    background: var(--slate-50) !important;
    border: 2px solid var(--slate-200) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: var(--teal-500) !important;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.15) !important;
    background: var(--white) !important;
}

.stTextArea textarea::placeholder {
    color: var(--slate-500) !important;
}

/* Hide default labels */
.stTextArea label {
    display: none !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, var(--teal-600) 0%, var(--teal-500) 100%) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(13, 148, 136, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(13, 148, 136, 0.35) !important;
}

/* Secondary button style for Clear */
.clear-btn button {
    background: var(--white) !important;
    color: var(--slate-600) !important;
    border: 2px solid var(--slate-200) !important;
    box-shadow: none !important;
}

.clear-btn button:hover {
    border-color: var(--slate-300) !important;
    background: var(--slate-50) !important;
    transform: none !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    background: var(--white) !important;
    color: var(--teal-600) !important;
    border: 2px solid var(--teal-500) !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.25rem !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: #f0fdfa !important;
}

/* Output section */
.output-header {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--slate-700);
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--slate-200);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.output-header::before {
    content: '';
    width: 4px;
    height: 1.2rem;
    background: linear-gradient(180deg, var(--teal-500) 0%, var(--cyan-500) 100%);
    border-radius: 2px;
}

/* Output content */
.output-content {
    background: var(--slate-50);
    border: 1px solid var(--slate-200);
    border-radius: 8px;
    padding: 1.5rem;
}

/* Markdown styling */
.stMarkdown {
    font-size: 1rem !important;
    line-height: 1.7 !important;
    color: var(--slate-700) !important;
}

.stMarkdown h2 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: var(--slate-900) !important;
    margin-top: 1.75rem !important;
    margin-bottom: 0.6rem !important;
    padding-bottom: 0.4rem !important;
    border-bottom: 1px solid var(--slate-200) !important;
}

.stMarkdown h2:first-child {
    margin-top: 0 !important;
}

.stMarkdown p {
    color: var(--slate-700) !important;
    margin-bottom: 0.75rem !important;
}

.stMarkdown ul {
    margin: 0.5rem 0 1rem 0 !important;
    padding-left: 1.25rem !important;
}

.stMarkdown li {
    color: var(--slate-700) !important;
    margin-bottom: 0.4rem !important;
}

.stMarkdown strong {
    color: var(--slate-900) !important;
    font-weight: 600 !important;
}

.stMarkdown code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.875rem !important;
    background: var(--slate-100) !important;
    color: var(--teal-600) !important;
    padding: 0.2rem 0.5rem !important;
    border-radius: 4px !important;
}

/* Placeholder */
.placeholder {
    background: var(--slate-50);
    border: 2px dashed var(--slate-300);
    border-radius: 8px;
    padding: 3rem 2rem;
    text-align: center;
}

.placeholder p {
    color: var(--slate-500);
    font-size: 1rem;
    margin: 0;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--slate-600) !important;
    background: var(--slate-50) !important;
    border-radius: 8px !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--teal-500) !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    margin-top: 2rem;
}

.footer p {
    font-size: 0.875rem;
    color: var(--slate-500);
    margin: 0;
}

.footer a {
    color: var(--teal-600);
    text-decoration: none;
}

.footer a:hover {
    text-decoration: underline;
}

/* Hide Streamlit defaults */
#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
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
    <div class="header-card">
        <h1>Agile Work Item Converter</h1>
        <p>Transform rough ideas into structured user stories with acceptance criteria</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API key check
    if not api_key:
        st.error("API key not found. Add `ANTHROPIC_API_KEY` to your Streamlit secrets.")
        st.stop()
    
    # Input
    st.markdown('<span class="input-label">Work Item</span>', unsafe_allow_html=True)
    work_item = st.text_area(
        "work_item",
        placeholder="Describe your work item here...\n\nExamples:\n• Fix the slow dashboard loading\n• Add export to CSV feature\n• Users can't login with SSO",
        height=140,
        label_visibility="collapsed"
    )
    
    # Optional context
    with st.expander("Add team context (optional)"):
        team_context = st.text_area(
            "context",
            placeholder="e.g., Python/React stack, 2-week sprints, healthcare domain",
            height=80,
            label_visibility="collapsed"
        )
    
    # Buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        generate = st.button("Generate", use_container_width=True)
    with col2:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("Clear", use_container_width=True):
            if 'output' in st.session_state:
                del st.session_state['output']
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate
    if generate and work_item:
        with st.spinner("Generating..."):
            ctx = team_context if 'team_context' in dir() and team_context else None
            st.session_state['output'] = get_agile_description(work_item, ctx, api_key)
    
    # Output
    st.markdown('<div class="output-header">Output</div>', unsafe_allow_html=True)
    
    if 'output' in st.session_state:
        st.markdown(f'<div class="output-content">', unsafe_allow_html=True)
        st.markdown(st.session_state['output'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button(
            "Download Markdown",
            st.session_state['output'],
            "agile_description.md",
            "text/markdown"
        )
    else:
        st.markdown("""
        <div class="placeholder">
            <p>Your structured agile description will appear here</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Powered by Claude API</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
