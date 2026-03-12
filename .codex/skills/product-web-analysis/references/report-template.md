# Product Web Analysis Report Template

Use this template when the user asks for a detailed or reusable report.

Important boundary:

- Sections 1 through 17 are for analyzing the product as it exists.
- Section 18 is the only build-oriented section by default.
- Section 19 is the fixed diagram section.
- Section 20 is the final summary.
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

### 2. One-Sentence Product Definition

Summarize the product in one sentence:

- Who it serves
- In what scenario
- What problem it solves
- How it delivers value

### 3. Key Terminology

For each important term, explain:

- Term
- Plain-language meaning
- What it means in this product's context
- Whether it is an industry-standard term or a product-specific term

Choose only the terms necessary to understand the product. Keep this section domain-appropriate rather than reusing fixed example terms.
This section may include both business terms and essential external proper nouns, such as important platforms, protocols, infrastructure layers, or third-party providers, when they are required for the reader to understand the rest of the report.
Do not expand this section into a complete list of vendors or dependencies.

### 4. What the Product Actually Does

- Plain-language explanation
- Core workflow in ordered steps
- Main actors and roles

### 5. Target Users and Roles

- Buyer
- Operator
- End beneficiary

### 6. Application Scenarios

For each scenario, explain:

- Who uses it
- When they use it
- What problem it solves
- Why the product fits that scenario

### 7. Current Alternatives and Substitutes

Cover:

- What users likely did before adopting this product
- The realistic alternatives, including manual workflows, internal tools, adjacent platforms, or direct competitors
- Why users might still choose those alternatives

### 8. Implemented Requirements

Split requirements into:

- Business requirements
- Functional requirements
- Operational requirements
- Risk or compliance requirements

### 9. Pain Points Solved

Explain:

- What the workflow looked like before the product
- What friction or risk existed
- What the product removes or improves
- What new value it creates

### 10. Business Model and Monetization Clues

Cover:

- Who appears to pay
- What they are likely paying for
- Pricing or packaging clues if public
- Likely cost drivers if they are visible

### 11. Competitive Positioning and Differentiation

Cover:

- Direct competitors when relevant
- Indirect substitutes
- Why a user might choose this product instead
- What appears differentiated in product, workflow, audience, pricing, ecosystem, or data

### 12. Growth and Distribution Clues

Cover:

- Likely acquisition channels
- Product-led, sales-led, partner-led, or content-led signals
- Referral, sharing, collaboration, template, or ecosystem loops if visible

### 13. Moat and Copyability

Cover:

- What might count as the product's moat
- What appears easy to replicate
- What appears difficult to replicate because of data, workflow depth, distribution, trust, integrations, or execution

### 14. Dependencies

Split dependencies into:

- Business dependencies
- External integrations or infrastructure dependencies
- Internal technical dependencies

### 15. Key Risks and Constraints

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

### 16. Data, Security, and Compliance Considerations

Cover when relevant:

- What kinds of data the product likely handles
- What permission, tenant, or access boundaries likely matter
- What security, privacy, or compliance expectations are implied

### 17. Likely Technical Solution

Cover:

- Likely architecture style
- Likely core modules
- Likely data and workflow design
- Key technical challenges

### 18. Confirmed Facts vs Reasoned Inference

Split into:

- Confirmed facts
- Reasoned inference

Add confidence labels where helpful.

### 19. If Building a Similar Product

Cover:

- Suggested MVP scope
- Suggested modules
- Main risks
- Cost considerations
- Early validation or success criteria when relevant

Keep this section clearly separate from product analysis. It should summarize implications for someone building a similar product, not rewrite the full report as implementation advice.

For cost considerations, include only the cost categories that materially matter, such as:

- Engineering and implementation cost
- Model, compute, storage, or media processing cost
- Third-party API or infrastructure cost
- Operations, support, or service delivery cost
- Sales, onboarding, or customer acquisition cost
- Compliance, legal, or security cost

### 20. Product Diagrams

Include these in this order:

- Workflow diagram
- Sequence diagram
- C4 diagrams

Rules:

- Keep all diagrams in this one section rather than scattering them across the report.
- Label diagrams as `Confirmed`, `Mixed`, or `Inferred` when needed.
- Keep diagrams concrete and product-specific.
- If the public evidence is thin, simplify the diagrams instead of inventing unsupported internals.

### 21. Final Summary

End with a concise paragraph that states what the product is, who it serves, what core workflow it handles, and what is most likely true about its technical approach.

## Adaptation Notes

- For `basic` depth, keep the glossary short but still include it as a standalone section.
- For `basic` depth, compress sections 6 through 20.
- For `expert` depth, expand sections 6 through 18 and include more explicit assumptions.
- For beginner audiences, define jargon inline.
- For technical audiences, add more detail on state transitions, jobs, APIs, permissions, integration boundaries, and operational risks.
