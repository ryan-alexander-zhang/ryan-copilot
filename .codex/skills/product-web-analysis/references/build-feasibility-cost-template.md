# Build Feasibility And Cost Report Template

Use this template for the third default output. This report is explicitly build-oriented and should stay separate from the two product-analysis reports.

## Build Feasibility And Cost Report

### 1. If Building a Similar Product

Cover:

- Suggested MVP scope
- Suggested modules
- Main build risks
- Cost considerations
- Early validation or success criteria when relevant

For cost considerations, include only the categories that materially matter, such as:

- Engineering and implementation cost
- Model, compute, storage, or media processing cost
- Third-party API or infrastructure cost
- Operations, support, or service delivery cost
- Sales, onboarding, or customer acquisition cost
- Compliance, legal, or security cost

### 2. Build Cost Research

Include this section by default in this report.

Split the section into:

- Confirmed current-product cost clues
- Confirmed vendor pricing
- Scenario-based build-cost estimates

Use these evidence levels:

- `High`: official source directly states the price, fee, or billing rule
- `Medium`: official source supports the pricing logic, but scenario mapping still requires analyst judgment
- `Low`: official source confirms the cost category exists, but does not support precise quantification
- `Do not quantify`: the item should be listed, but no defensible number should be given

For every important cost item, include:

- Cost item
- Vendor or cost type
- Whether the vendor is confirmed, a confirmed dependency, or only a candidate build option
- Official source
- Official URL
- Public pricing rule, fee rule, or billing rule
- Billing unit
- Evidence level
- Key uncertainty or assumption

Rules:

- Use official pricing, billing, fee, limits, quota, or legal pages whenever available.
- If pricing is not public, say `Contact sales / not publicly listed` rather than inventing a precise number.
- If the analyzed product does not confirm the vendor, do not present that vendor's pricing as the product's actual cost.
- Keep `Confirmed vendor pricing` separate from `Scenario-based build-cost estimates`.
- If evidence is too thin, keep the row and mark it `Do not quantify` rather than dropping the item.

### 3. Final Summary

End with a concise paragraph that states whether a similar product appears feasible to build, what the main build risks are, and which cost areas require the most diligence.
