# Agile Work Item Converter

A Streamlit application that transforms rough work items into structured, actionable agile descriptions using Claude API.

## Features

- **Natural Language Input**: Accepts work items in any format - Jira titles, Slack messages, meeting notes, or rough ideas
- **Structured Output**: Generates complete agile descriptions including:
  - User story format
  - Acceptance criteria
  - Technical notes
  - Definition of done
  - Story point estimates
- **Team Context**: Optional context input for domain-specific terminology
- **Export**: Download generated descriptions as Markdown

## Installation

```bash
# Clone or download the files
cd agile_converter

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then:
1. Enter your Anthropic API key in the sidebar
2. (Optional) Add team/project context for better results
3. Paste your work item in the input box
4. Click "Generate"

## Example

**Input:**
```
Fix the slow dashboard
```

**Output:**
```markdown
## Title
Optimise Dashboard Load Time

## User Story
As a data analyst, I want the dashboard to load within 3 seconds, 
so that I can access insights without workflow interruption.

## Description
The main analytics dashboard currently experiences slow load times 
during peak usage. This impacts user productivity and workflow efficiency.
Focus on initial page load optimisation.

## Acceptance Criteria
- [ ] Dashboard loads in ≤3 seconds under normal conditions
- [ ] No regression in data accuracy or completeness
- [ ] Loading state displayed during data fetch
- [ ] Performance metrics logged to monitoring

## Technical Notes
- Profile current queries for bottlenecks
- Consider caching for frequently accessed data
- May require database index optimisation

## Definition of Done
- Code complete and reviewed
- Performance tests passing
- Deployed to staging and validated

## Suggested Story Points
5 - Requires investigation and optimisation work, but scope is defined.
```

## Configuration

### Environment Variables (Optional)

You can set the API key as an environment variable instead of entering it in the UI:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Then modify the app to read from environment:

```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY") or st.text_input(...)
```

## Customisation

### Modify the System Prompt

Edit the `SYSTEM_PROMPT` variable in `app.py` to:
- Add team-specific templates
- Include additional sections (e.g., data governance, security considerations)
- Change the story point scale
- Add healthcare-specific fields

### Add Team Presets

You could extend the sidebar to include preset contexts:

```python
presets = {
    "BHF DSC": "Healthcare data science team working with NHS datasets...",
    "Frontend": "React/TypeScript team following atomic design...",
}
```

## Deployment

### Streamlit Community Cloud

1. Push to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Add `ANTHROPIC_API_KEY` to secrets

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## License

MIT
