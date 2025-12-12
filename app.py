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
    layout="wide",
    initial_sidebar_state="expanded"
)

# BHF DSC Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bhf-red: #C8102E;
    --bhf-red-dark: #A00D24;
    --bhf-red-light: #E8394F;
    --color-primary: #C8102E;
    --color-secondary: #2D3436;
    --color-bg: #FAFAFA;
    --color-bg-warm: #FFF9F9;
    --color-bg-card: #FFFFFF;
    --color-bg-dark: #1A1A2E;
    --color-text: #2D3436;
    --color-text-muted: #636E72;
    --color-border: #E8E8E8;
    --font-display: 'Source Serif 4', Georgia, serif;
    --font-body: 'Source Sans 3', -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --shadow-sm: 0 1px 3px rgba(200, 16, 46, 0.06);
    --shadow-md: 0 4px 12px rgba(200, 16, 46, 0.08);
    --shadow-red: 0 4px 20px rgba(200, 16, 46, 0.15);
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
}

.stApp {
    background: linear-gradient(180deg, var(--color-bg) 0%, var(--color-bg-warm) 100%);
}

.main .block-container {
    max-width: 1200px;
    padding: 2rem 3rem 4rem;
}

h1, h2, h3, h4 {
    font-family: var(--font-display) !important;
    color: var(--color-secondary) !important;
}

p, li, td, th, label, .stMarkdown {
    font-family: var(--font-body) !important;
    color: var(--color-text);
    line-height: 1.65;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, var(--color-bg-dark) 0%, #2D1F2F 30%, var(--bhf-red-dark) 70%, var(--bhf-red) 100%);
    border-radius: var(--radius-lg);
    padding: 3rem;
    margin: -1rem -1rem 2rem;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at 20% 80%, rgba(255, 107, 107, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 80% 20%, rgba(242, 84, 91, 0.15) 0%, transparent 40%);
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #ffffff;
    font-family: var(--font-body);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.5rem 1.25rem;
    border-radius: 50px;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: var(--font-display);
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.75rem;
}

.hero-subtitle {
    font-family: var(--font-body);
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.6;
    max-width: 600px;
}

/* Cards */
.input-card, .output-card {
    background: var(--color-bg-card);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    height: 100%;
    box-shadow: var(--shadow-sm);
}

.input-card:hover, .output-card:hover {
    border-color: rgba(200, 16, 46, 0.3);
    box-shadow: var(--shadow-md);
}

.card-header {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--color-secondary);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--color-border);
}

.card-header-icon {
    margin-right: 0.5rem;
}

/* Text Areas */
.stTextArea textarea {
    font-family: var(--font-mono) !important;
    font-size: 0.9rem !important;
    border-radius: var(--radius-sm) !important;
    border: 2px solid var(--color-border) !important;
    background: var(--color-bg) !important;
}

.stTextArea textarea:focus {
    border-color: var(--bhf-red) !important;
    box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.1) !important;
}

/* Buttons */
.stButton > button {
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, var(--bhf-red) 0%, var(--bhf-red-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.75rem 2rem !important;
    font-size: 0.95rem !important;
    transition: all 0.25s ease !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-red) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download button */
.stDownloadButton > button {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    background: rgba(200, 16, 46, 0.08) !important;
    color: var(--bhf-red) !important;
    border: 1px solid rgba(200, 16, 46, 0.2) !important;
    border-radius: 50px !important;
    padding: 0.5rem 1.25rem !important;
    font-size: 0.85rem !important;
}

.stDownloadButton > button:hover {
    background: rgba(200, 16, 46, 0.12) !important;
    border-color: var(--bhf-red) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--color-bg-card);
    border-right: 1px solid var(--color-border);
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-display) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: var(--color-secondary) !important;
    margin-bottom: 0.75rem;
}

/* Service intro box */
.service-intro {
    background: linear-gradient(135deg, rgba(200, 16, 46, 0.04) 0%, rgba(242, 84, 91, 0.04) 100%);
    border-left: 3px solid var(--bhf-red);
    padding: 1rem 1.25rem;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin-bottom: 1rem;
}

.service-intro p {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    margin: 0;
}

/* Output placeholder */
.output-placeholder {
    background: var(--color-bg);
    border: 2px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: 3rem;
    text-align: center;
    color: var(--color-text-muted);
}

.output-placeholder-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.output-placeholder-text {
    font-family: var(--font-body);
    font-size: 1rem;
    margin-bottom: 0.25rem;
}

.output-placeholder-hint {
    font-family: var(--font-body);
    font-size: 0.85rem;
    color: var(--color-text-muted);
    opacity: 0.7;
}

/* Example chips */
.example-chip {
    display: inline-block;
    background: rgba(200, 16, 46, 0.06);
    color: var(--bhf-red);
    border: 1px solid rgba(200, 16, 46, 0.15);
    padding: 0.35rem 0.75rem;
    border-radius: 50px;
    font-family: var(--font-body);
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.example-chip:hover {
    background: rgba(200, 16, 46, 0.12);
    border-color: var(--bhf-red);
}

/* Expander styling */
.streamlit-expanderHeader {
    font-family: var(--font-body) !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    color: var(--color-secondary) !important;
    background: rgba(200, 16, 46, 0.03) !important;
    border-radius: var(--radius-sm) !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--bhf-red) !important;
}

/* Footer */
.footer-minimal {
    text-align: center;
    padding: 2rem 0 1rem;
    margin-top: 2rem;
    border-top: 1px solid var(--color-border);
}

.footer-minimal p {
    font-family: var(--font-body);
    font-size: 0.85rem;
    color: var(--color-text-muted);
}

.footer-minimal a {
    color: var(--bhf-red);
    text-decoration: none;
}

.footer-minimal a:hover {
    text-decoration: underline;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Responsive */
@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1.5rem;
    }
    .hero-title {
        font-size: 1.75rem;
    }
    .main .block-container {
        padding: 1rem 1.5rem 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# System prompt for Claude
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


def get_agile_description(
    work_item: str,
    context: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """Generate an agile description from a work item using Claude API."""
    
    if not api_key:
        return "❌ API key not configured. Please add ANTHROPIC_API_KEY to your Streamlit secrets."
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build the user message
        user_message = f"Work Item:\n{work_item}"
        if context:
            user_message = f"Team/Project Context:\n{context}\n\n{user_message}"
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return message.content[0].text
        
    except anthropic.AuthenticationError:
        return "❌ Invalid API key. Please check your Anthropic API key in Streamlit secrets."
    except anthropic.RateLimitError:
        return "❌ Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def main():
    # Get API key from secrets
    api_key = get_api_key()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📝 Team Context")
        st.markdown('<div class="service-intro"><p>Add context about your team, project, or domain to get more relevant descriptions.</p></div>', unsafe_allow_html=True)
        
        team_context = st.text_area(
            "Context (optional)",
            placeholder="e.g., Healthcare data science team at BHF DSC. Stack: Python/PySpark/Databricks. 2-week sprints. Working with NHS datasets and phenotype definitions.",
            height=140,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("### 💡 Quick Examples")
        st.markdown("""
        Click to try:
        - "Fix the slow dashboard"
        - "Add phenotype search"
        - "Export to CSV not working"
        - "Need better error messages"
        """)
        
        st.markdown("---")
        
        # API status indicator
        if api_key:
            st.success("✓ API Connected", icon="🔗")
        else:
            st.warning("API key not found in secrets", icon="⚠️")
        
        st.markdown("---")
        st.caption("BHF Data Science Centre")
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <span class="hero-badge">🏥 BHF Data Science Centre</span>
            <h1 class="hero-title">Agile Work Item Converter</h1>
            <p class="hero-subtitle">Transform rough ideas, Jira titles, Slack messages, or meeting notes into structured, actionable agile descriptions with user stories, acceptance criteria, and story point estimates.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content columns
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card-header"><span class="card-header-icon">📥</span>Input</div>', unsafe_allow_html=True)
        
        work_item = st.text_area(
            "Work item input",
            placeholder="Paste a rough work item here...\n\nExamples:\n• 'Fix the slow phenotype search'\n• 'Add ICD-10 validation to the toolkit'\n• 'Users getting timeout errors on large queries'\n• 'Need to support SNOMED CT codes'",
            height=280,
            label_visibility="collapsed"
        )
        
        # Action buttons
        btn_col1, btn_col2 = st.columns([1, 1])
        
        with btn_col1:
            generate_btn = st.button("🚀 Generate Description", use_container_width=True)
        
        with btn_col2:
            if st.button("🗑️ Clear", use_container_width=True):
                if 'last_output' in st.session_state:
                    del st.session_state['last_output']
                st.rerun()
    
    with col2:
        st.markdown('<div class="card-header"><span class="card-header-icon">📤</span>Output</div>', unsafe_allow_html=True)
        
        output_placeholder = st.empty()
        
        if generate_btn and work_item:
            with st.spinner("Generating agile description..."):
                result = get_agile_description(
                    work_item=work_item,
                    context=team_context if team_context else None,
                    api_key=api_key
                )
                st.session_state['last_output'] = result
        
        # Display output
        if 'last_output' in st.session_state:
            output_placeholder.markdown(st.session_state['last_output'])
            
            st.download_button(
                label="📥 Download as Markdown",
                data=st.session_state['last_output'],
                file_name="agile_description.md",
                mime="text/markdown"
            )
        else:
            output_placeholder.markdown("""
            <div class="output-placeholder">
                <div class="output-placeholder-icon">📋</div>
                <p class="output-placeholder-text">Your agile description will appear here</p>
                <p class="output-placeholder-hint">Enter a work item and click Generate</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Example transformations
    st.markdown("---")
    
    with st.expander("📖 See example transformations"):
        ex_col1, ex_col2 = st.columns(2)
        
        with ex_col1:
            st.markdown("#### Before")
            st.code("Fix the slow phenotype search", language=None)
            st.code("Add SNOMED CT support", language=None)
            st.code("Query timeouts for large cohorts", language=None)
        
        with ex_col2:
            st.markdown("#### After (Title + User Story)")
            st.markdown("""
            **Optimise Phenotype Search Performance**  
            *As a researcher, I want the phenotype search to return results within 2 seconds, so that I can efficiently explore available codelists without workflow interruption.*
            
            **Implement SNOMED CT Code Support**  
            *As a data analyst, I want to use SNOMED CT codes in phenotype definitions, so that I can work with primary care data alongside hospital records.*
            
            **Resolve Cohort Query Timeout Errors**  
            *As a researcher, I want large cohort queries to complete without timing out, so that I can analyse population-level datasets reliably.*
            """)
    
    # Footer
    st.markdown("""
    <div class="footer-minimal">
        <p>Built with Claude API & Streamlit | <a href="https://bhfdatasciencecentre.org" target="_blank">BHF Data Science Centre</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
