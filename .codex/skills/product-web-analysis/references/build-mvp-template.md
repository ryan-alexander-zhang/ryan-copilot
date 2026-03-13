# Build MVP Report Template

Use this template for the third default output. This report is
explicitly MVP-oriented and should stay separate from the two
product-analysis reports.

The default question is: if someone wants to build a similar product
now, what is the smallest credible MVP, what makes it hard, what
compliance and dependencies matter, what does it cost, and what
architecture is suitable for an early team.

## Build MVP Report

### Global Rules

- Keep `Confirmed facts` separate from `Reasoned inference`.
- If a regulatory conclusion, license requirement, dependency detail, or
  vendor detail cannot be confirmed, label it as `推测` or `待验证项`.
- Prefer simple, shippable MVP recommendations. Avoid overdesign unless
  the product's risk profile clearly demands it.
- Tie scope, dependencies, costs, and architecture back to the MVP core
  flow rather than listing generic best practices.
- When cost research mode is active, include direct official links for
  every non-trivial pricing claim whenever they exist.

### 1. MVP Goals And Boundaries

Cover:

- The user problem the MVP must solve
- The primary target user or buyer
- The single end-to-end workflow that must work
- MVP success criteria
- Explicit boundaries and non-goals
- Key assumptions and prerequisites

Use a MoSCoW-style feature list. For each feature, fill in:

- `Priority`: `Must`, `Should`, `Could`, or `Won't (for MVP)`
- `Feature or capability`
- `User value`
- `Why now or later`
- `Notes, risks, or assumptions`

Rules:

- `Must` items should be the minimum required to complete one
  closed-loop workflow.
- `Should` items materially improve viability but can be delayed if needed.
- `Could` items are useful but non-critical.
- `Won't (for MVP)` items should be deferred explicitly rather than left
  ambiguous.

### 2. Core Challenges Analysis

Identify the 3-7 product-specific difficulties most likely to decide
whether the MVP works.

For each challenge, explain:

- Why it is core to this product rather than a generic startup problem
- Whether it is mainly a product, engineering, operations, compliance,
  or go-to-market issue
- What failure looks like if the team gets it wrong
- How the MVP should handle it at first launch

Suggested fields per challenge:

- `Core challenge`
- `Why it is hard here`
- `Impact area`
- `MVP handling strategy`
- `Confidence`

### 3. MVP Core Flow

Describe the one main end-to-end flow the MVP must support.

Include:

- Primary actors
- Trigger or entry point
- Step-by-step flow
- Key decisions or state transitions
- Failure handling and manual fallback
- Success outcome

When useful, add a Mermaid `flowchart` for this single core flow.

### 4. Compliance And Qualification Analysis

Analyze the product from these six angles:

1. Business compliance
2. Required qualifications, registrations, permits, licenses, or filings
3. Data and privacy
4. Content and transaction regulation
5. Regional differences
6. Risk grading

For each angle, explicitly answer:

- Which features trigger regulatory requirements
- What qualifications, filings, permits, licenses, or registrations may
  be needed
- Whether third-party providers can cover all or part of the requirement
- Which countries or regions differ materially
- Which features are safe for the MVP and which should be deferred
- Whether the conclusion is confirmed, `推测`, or a `待验证项`

Recommended fields per compliance dimension:

- `Dimension`
- `Triggering features`
- `Likely requirement`
- `Third-party coverage`
- `Major regional differences`
- `MVP recommendation`
- `Status`

Add a separate risk-grading table:

- `Feature or module`
- `Risk level`
- `Why`
- `MVP advice`

Use `Low`, `Medium`, or `High` for risk level.

### 5. Dependency Research And Interface Inventory

Do not make this section brief. Expand it into a detailed interface
inventory that covers all external interfaces required by the MVP core
flow and the internal module boundaries needed to support that flow.

Produce this section in two views:

1. `Flow view`
2. `Module view`

For the `Flow view`, group interfaces by concrete workflow stages such
as:

- Agency or business onboarding
- Creator or end-user onboarding
- KYC / KYB / verification
- Bank linking or account verification
- Funding source activation
- Authorization or mandate setup
- Debit or collection
- Payout or disbursement
- Reconciliation and event handling
- Notifications and messaging
- Invoicing or billing
- Cross-border or optional regional flows

For the `Module view`, group interfaces by internal product or system
modules such as:

- Identity and tenant management
- Split configuration or billing rules
- Ledger and transaction state
- Workflow orchestration
- Payments and payout orchestration
- Notifications
- Reporting and exports
- Compliance and risk controls
- Support or ops console

For every external interface, include:

- Vendor
- Product or API family
- Exact endpoint name, operation name, or the narrowest official guide
- Purpose
- When it is called in the workflow
- Key inputs
- Key outputs or webhook callbacks
- Whether it is synchronous, asynchronous, or both
- Integration difficulty
- Backup option
- Whether it is a confirmed dependency, candidate build option, or
  `推测`
- Official documentation URL
- Documentation freshness note, such as `URL verified on YYYY-MM-DD`

For every internal interface or module boundary, include:

- Module name
- Internal API, command, event, or job boundary
- Upstream trigger
- Downstream dependency
- Why it is required for the MVP
- Whether it is public, internal-only, or admin-only

Rules:

- Prefer official APIs and documented integration points.
- Use web search to verify official documentation URLs on the analysis
  date.
- Prefer endpoint-level or guide-level official docs over generic vendor
  homepages.
- If exact interfaces are not public, infer from common industry
  practice and label the item as `推测`.
- If no public docs exist for a confirmed integration, say `No public
  API docs found as of YYYY-MM-DD` instead of pretending the docs are
  public.
- Separate must-have interfaces from deferrable interfaces when that
  makes the tradeoff clearer.
- If versioning or changelog pages materially affect freshness, cite
  them alongside the interface docs or mention them in the freshness
  note.

### 6. Cost Analysis

Start with a five-dimension summary and assign each dimension a level of
`Low`, `Medium`, or `High`.

Required dimensions:

- Development cost
- Infrastructure and DevOps cost
- Third-party vendor cost
- Compliance cost
- Business operations cost

Recommended fields per cost dimension:

- `Cost dimension`
- `Level`
- `Why`
- `Main drivers`
- `MVP control strategy`

If cost research mode is active, add these three subsections:

1. `Confirmed current-product cost clues`
2. `Confirmed vendor pricing`
3. `Scenario-based build-cost estimates`

Use these evidence levels:

- `High`: official source directly states the pricing, fee, or billing rule
- `Medium`: official source supports the pricing logic, but scenario
  mapping still requires analyst judgment
- `Low`: official source confirms the cost category exists, but does not
  support precise quantification
- `Do not quantify`: the item should be listed, but no defensible
  number should be given

For every important cost item, include:

- Cost item
- Vendor or cost type
- Whether the vendor is confirmed, a confirmed dependency, or only a
  candidate build option
- Official source
- Official URL
- Public pricing, fee, or billing rule
- Billing unit
- Evidence level
- Key uncertainty or assumption

Rules:

- Use official pricing, billing, fee, limits, quota, or legal pages
  whenever available.
- If pricing is not public, say `Contact sales / not publicly listed`
  rather than inventing a precise number.
- If the analyzed product does not confirm the vendor, do not present
  that vendor's pricing as the product's actual cost.
- Keep `Confirmed vendor pricing` separate from `Scenario-based build-cost estimates`.
- If evidence is too thin, keep the row and mark it `Do not quantify`
  rather than dropping the item.

### 7. Technical Architecture Recommendation

Recommend an MVP-appropriate architecture and explain why it is the
right fit for an early stage team.

Cover at least:

- Client shape
- Server architecture
- Database
- Cache
- Object storage
- Message queue
- Login and authentication
- Logging and monitoring
- Third-party integration pattern

Recommended fields per layer:

- `Layer`
- `Recommendation`
- `Why it fits MVP`
- `Upgrade signal`

Architecture rules:

- Prefer a modular monolith plus managed services unless the product's
  constraints clearly require something more complex.
- Avoid adding infrastructure only because it is fashionable. If a
  component is not needed yet, say `Not needed initially`.
- Explain how the architecture supports the MVP core flow, compliance
  posture, team size, and likely traffic shape.

### Final Summary

End with a concise paragraph that states:

- Whether a similar MVP appears feasible to launch
- What the main blockers are
- Which features should ship first
- Which high-risk features should be delayed
- Which dependencies or compliance questions need validation before
  implementation starts
