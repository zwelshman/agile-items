"""
Agile Work Item Converter
Transforms rough work items into structured agile descriptions using Claude API.
"""

import streamlit as st
import anthropic
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Agile Work Item Converter",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header styling */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    
    h2, h3 {
        font-weight: 600 !important;
        color: #1a1a2e !important;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4361ee !important;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15) !important;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.35) !important;
    }
    
    /* Output container */
    .output-container {
        background: #fafafa;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e8e8e8;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4361ee;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 0.5rem;
    }
    
    /* Code blocks */
    code {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .badge-success {
        background: #d4edda;
        color: #155724;
    }
    
    .badge-info {
        background: #e7f1ff;
        color: #004085;
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


def get_agile_description(
    work_item: str,
    context: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """Generate an agile description from a work item using Claude API."""
    
    if not api_key:
        return "❌ Please provide an Anthropic API key in the sidebar."
    
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
        return "❌ Invalid API key. Please check your Anthropic API key."
    except anthropic.RateLimitError:
        return "❌ Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Your Anthropic API key for Claude access"
        )
        
        st.markdown("---")
        
        st.markdown("### 📝 Team Context (Optional)")
        team_context = st.text_area(
            "Provide context about your team, project, or domain",
            placeholder="e.g., We're a healthcare data science team working with NHS datasets. Our stack is Python/PySpark/Databricks. We use 2-week sprints.",
            height=120,
            help="This helps generate more relevant and domain-specific descriptions"
        )
        
        st.markdown("---")
        
        st.markdown("### 📖 Quick Guide")
        st.markdown("""
        **Input Examples:**
        - "Fix the slow dashboard"
        - "Add export to CSV"
        - "Users can't login with SSO"
        - "Need better error messages"
        
        **Output Includes:**
        - User story format
        - Acceptance criteria
        - Technical notes
        - Story point estimate
        """)
        
        st.markdown("---")
        st.caption("Built with Claude API & Streamlit")
    
    # Main content
    st.markdown("# 📋 Agile Work Item Converter")
    st.markdown("Transform rough work items into structured, actionable agile descriptions.")
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input")
        work_item = st.text_area(
            "Enter your work item",
            placeholder="Paste a rough work item, Jira title, Slack message, or meeting note...\n\nExamples:\n- 'Fix the slow dashboard'\n- 'Add phenotype search to the toolkit'\n- 'Users complaining about timeout errors'",
            height=250,
            label_visibility="collapsed"
        )
        
        # Action buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
        
        with btn_col1:
            generate_btn = st.button("🚀 Generate", use_container_width=True)
        
        with btn_col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.rerun()
    
    with col2:
        st.markdown("### Output")
        
        # Output container
        output_placeholder = st.empty()
        
        if generate_btn and work_item:
            with st.spinner("Generating agile description..."):
                result = get_agile_description(
                    work_item=work_item,
                    context=team_context if team_context else None,
                    api_key=api_key
                )
                
                # Store in session state
                st.session_state['last_output'] = result
        
        # Display output
        if 'last_output' in st.session_state:
            output_placeholder.markdown(st.session_state['last_output'])
            
            # Copy button (download as markdown)
            st.download_button(
                label="📥 Download as Markdown",
                data=st.session_state['last_output'],
                file_name="agile_description.md",
                mime="text/markdown"
            )
        else:
            output_placeholder.markdown(
                """<div style="
                    background: #f8f9fa; 
                    border: 2px dashed #dee2e6; 
                    border-radius: 12px; 
                    padding: 3rem; 
                    text-align: center;
                    color: #6c757d;
                    height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                ">
                    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Your agile description will appear here</p>
                    <p style="font-size: 0.9rem;">Enter a work item and click Generate</p>
                </div>""",
                unsafe_allow_html=True
            )
    
    # Example section
    st.markdown("---")
    
    with st.expander("💡 See example transformations"):
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            st.markdown("#### Before")
            st.code("Fix the slow dashboard", language=None)
            st.code("Add export feature", language=None)
            st.code("Login broken for some users", language=None)
        
        with example_col2:
            st.markdown("#### After (Title + User Story)")
            st.markdown("""
            **Optimise Dashboard Load Time**  
            *As a data analyst, I want the dashboard to load within 3 seconds, so that I can access insights without workflow interruption.*
            
            **Implement Data Export to CSV**  
            *As a researcher, I want to export query results to CSV, so that I can analyse data in external tools.*
            
            **Fix SSO Authentication Failures**  
            *As a user, I want SSO login to work reliably, so that I can access the system without manual intervention.*
            """)


if __name__ == "__main__":
    main()
