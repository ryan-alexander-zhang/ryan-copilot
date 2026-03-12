# Product Web Analysis Report Template

Use this template when the user asks for a detailed or reusable report.

Important boundary:

- Sections 1 through 11 are for analyzing the product as it exists.
- Section 12 is the only build-oriented section by default.
- Section 13 is the fixed diagram section.
- Section 14 is the final summary.
- Do not let earlier sections drift into recommendations, implementation plans, or pseudo-PRDs unless the user explicitly asks for that style of output.

## Product Analysis Report

### 1. Product Summary

- Product name
- Product URL
- Category
- Primary audience
- Secondary audience
- Core value proposition
- Analysis confidence

### 2. Key Terminology

For each important term, explain:

- Term
- Plain-language meaning
- What it means in this product's context
- Whether it is an industry-standard term or a product-specific term

Choose only the terms necessary to understand the product. Keep this section domain-appropriate rather than reusing fixed example terms.
This section may include both business terms and essential external proper nouns, such as important platforms, protocols, infrastructure layers, or third-party providers, when they are required for the reader to understand the rest of the report.
Do not expand this section into a complete list of vendors or dependencies.

### 3. What the Product Actually Does

- Plain-language explanation
- Core workflow in ordered steps
- Main actors and roles

### 4. Target Users and Roles

- Buyer
- Operator
- End beneficiary

### 5. Application Scenarios

For each scenario, explain:

- Who uses it
- When they use it
- What problem it solves
- Why the product fits that scenario

### 6. Implemented Requirements

Split requirements into:

- Business requirements
- Functional requirements
- Operational requirements
- Risk or compliance requirements

### 7. Pain Points Solved

Explain:

- What the workflow looked like before the product
- What friction or risk existed
- What the product removes or improves
- What new value it creates

### 8. Dependencies

Split dependencies into:

- Business dependencies
- External integrations or infrastructure dependencies
- Internal technical dependencies

### 9. Key Risks and Constraints

Cover only the risk categories that materially apply to the product:

- Business or market risks
- Operational risks
- Technical risks
- Compliance or legal risks
- Platform or ecosystem dependency risks
- Go-to-market risks

For each important risk, explain:

- What the risk is
- Why it matters for this product
- Whether it appears to be core, moderate, or secondary

### 10. Likely Technical Solution

Cover:

- Likely architecture style
- Likely core modules
- Likely data and workflow design
- Key technical challenges

### 11. Confirmed Facts vs Reasoned Inference

Split into:

- Confirmed facts
- Reasoned inference

Add confidence labels where helpful.

### 12. If Building a Similar Product

Cover:

- Suggested MVP scope
- Suggested modules
- Main risks

Keep this section clearly separate from product analysis. It should summarize implications for someone building a similar product, not rewrite the full report as implementation advice.

### 13. Product Diagrams

Include these in this order:

- Workflow diagram
- Sequence diagram
- C4 diagrams

Rules:

- Keep all diagrams in this one section rather than scattering them across the report.
- Label diagrams as `Confirmed`, `Mixed`, or `Inferred` when needed.
- Keep diagrams concrete and product-specific.
- If the public evidence is thin, simplify the diagrams instead of inventing unsupported internals.

### 14. Final Summary

End with a concise paragraph that states what the product is, who it serves, what core workflow it handles, and what is most likely true about its technical approach.

## Adaptation Notes

- For `basic` depth, keep the glossary short but still include it as a standalone section.
- For `basic` depth, compress sections 6 through 13.
- For `expert` depth, expand sections 6 through 11 and include more explicit assumptions.
- For beginner audiences, define jargon inline.
- For technical audiences, add more detail on state transitions, jobs, APIs, permissions, integration boundaries, and operational risks.
