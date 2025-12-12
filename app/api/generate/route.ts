import Anthropic from "@anthropic-ai/sdk";
import { NextResponse } from "next/server";

const SYSTEM_PROMPT = `You are an expert agile coach and product manager who transforms rough, unstructured work items into beautifully crafted, actionable agile descriptions. Your output should be clear, specific, and immediately usable by development teams.

For every work item, provide ALL of the following sections in this exact format:

## Title
A concise, action-oriented title (maximum 10 words) that clearly describes what needs to be done.

## User Story
Write in the format: "As a [type of user], I want [goal] so that [benefit]."
Be specific about the user persona and the value delivered.

## Description
Provide 2-3 sentences of context explaining:
- What problem this solves
- Why it matters to users or the business
- Any relevant background information

## Acceptance Criteria
List 3-5 specific, testable criteria as checkboxes:
- [ ] Criterion 1 - Must be measurable and verifiable
- [ ] Criterion 2 - Clear pass/fail condition
- [ ] Criterion 3 - Specific and actionable
(Add more if needed, but keep it focused)

## Technical Notes
Provide implementation hints and considerations:
- Key technical approaches to consider
- Potential dependencies or integrations
- Performance or security considerations
- Suggested architecture patterns

## Definition of Done
Checklist for completion:
- [ ] Code complete and reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product owner sign-off

## Story Points
Estimate using Fibonacci scale (1, 2, 3, 5, 8, 13).
Format: **[X] points** - Brief rationale for the estimate.

---

Guidelines:
- Be specific, not vague. Replace generic terms with concrete details.
- Focus on user value and business outcomes.
- Make acceptance criteria testable and unambiguous.
- Keep the scope reasonable - if it's too big, suggest breaking it down.
- Use technical language appropriately but keep it accessible.
- Consider edge cases and error scenarios in acceptance criteria.`;

export async function POST(request: Request) {
  try {
    const { workItem, teamContext } = await request.json();

    if (!workItem || typeof workItem !== "string") {
      return NextResponse.json(
        { error: "Work item is required" },
        { status: 400 }
      );
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;

    if (!apiKey) {
      return NextResponse.json(
        {
          error:
            "API key not configured. Please set ANTHROPIC_API_KEY in your environment variables.",
        },
        { status: 500 }
      );
    }

    const client = new Anthropic({ apiKey });

    // Build the user message
    let userMessage = `Please transform this rough work item into a structured agile description:\n\n"${workItem}"`;

    if (teamContext && typeof teamContext === "string" && teamContext.trim()) {
      userMessage += `\n\nTeam/Project Context:\n${teamContext}`;
    }

    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 2048,
      messages: [
        {
          role: "user",
          content: userMessage,
        },
      ],
      system: SYSTEM_PROMPT,
    });

    // Extract text content from response
    const textContent = response.content.find((block) => block.type === "text");

    if (!textContent || textContent.type !== "text") {
      throw new Error("No text content in response");
    }

    return NextResponse.json({ result: textContent.text });
  } catch (error) {
    console.error("Error generating description:", error);

    if (error instanceof Anthropic.AuthenticationError) {
      return NextResponse.json(
        { error: "Invalid API key. Please check your ANTHROPIC_API_KEY." },
        { status: 401 }
      );
    }

    if (error instanceof Anthropic.RateLimitError) {
      return NextResponse.json(
        { error: "Rate limit exceeded. Please try again in a moment." },
        { status: 429 }
      );
    }

    return NextResponse.json(
      { error: "Failed to generate description. Please try again." },
      { status: 500 }
    );
  }
}
