---
name: product-web-analysis
description: Analyze a product from a user-provided product name or URL using web search and official public sources, then produce structured reports in the user's requested language. Use when Codex needs product analysis, website analysis, product research, competitor analysis, product teardown, reverse analysis of a SaaS or tool, or an MVP build assessment for a similar product, including scope, dependencies, compliance, cost, and technical architecture suggestions. Trigger on requests such as analyze this product, analyze this website, explain this product, summarize this SaaS, infer the architecture, compare these products, assess whether it is worth building, estimate MVP cost or feasibility, or Chinese requests like 分析这个产品、分析这个网站、产品分析、竞品分析、产品拆解、技术架构推断、产品调研、逆向分析这个产品、根据产品名称或URL生成报告、评估能不能做、做MVP拆解、估算开发成本. Generate reports with flowcharts, sequence diagrams, and C4 diagrams while clearly separating confirmed facts from reasoned inference.
---

# Product Web Analysis

## Overview

Use this skill to research a public product on the web and turn scattered evidence into a structured report. Accept either a product name or a product URL, adapt the report language to the user's request, and keep a hard boundary between confirmed facts and inference.

This skill is primarily for understanding and analyzing an existing
product as it appears in public. The first two reports stay analytical.
The third report is the only build-oriented output and should stay
focused on an early MVP rather than a full PRD.

Typical Chinese triggers include `分析这个产品`, `分析这个网站`, `做一个产品分析`, `做竞品分析`, `拆解这个 SaaS`, `推断技术架构`, and `根据这个 URL 做产品调研`.

Read these templates when you need the full output structure:

- [references/product-understanding-template.md](references/product-understanding-template.md)
- [references/market-strategy-template.md](references/market-strategy-template.md)
- [references/build-mvp-template.md](references/build-mvp-template.md)
- [references/diagram-templates.md](references/diagram-templates.md)

## Inputs

Collect these inputs from the user request or infer reasonable defaults:

- Product identifier: product name, URL, or both
- Analysis objective: general analysis, competitor comparison, architecture inference, PRD-style decomposition, investor-style summary, and so on
- Preferred language for the final report
- Depth: `basic`, `detailed`, or `expert`
- Audience: `beginner`, `pm`, `founder`, `engineer`, `architect`, or `investor`
- Whether to compare multiple products

If the user does not specify language, answer in the language used by the user.

## Cost Research Trigger

Switch into evidence-backed cost research mode when the user asks for any of the following:

- Whether it is worth building a similar product
- Development, operating, or vendor cost analysis
- API pricing, infrastructure pricing, or external dependency fees
- Unit economics or cost structure validation
- Official links, official pricing pages, billing pages, or legal fee pages
- High-confidence cost analysis with precise source attribution

In this mode, cost-related claims must be treated as a separate evidence-gathering task rather than lightweight commentary.

## Default Deliverables

By default, produce three separate reports rather than one monolithic report:

1. `Product Understanding`
2. `Market And Strategy`
3. `Build MVP`

All three are default outputs. Do not collapse them into one long report unless the user explicitly asks for a single-file format.

## Build MVP Deliverable

Use [references/build-mvp-template.md](references/build-mvp-template.md)
for the third report.

The `Build MVP` report should answer one bounded question: if someone
wants to launch a credible early version of a similar product, what is
the smallest useful scope, what are the main blockers, what dependencies
and compliance constraints matter, what will likely cost money, and what
technical architecture is appropriate now.

By default, organize the `Build MVP` report into these seven sections:

1. MVP goals and boundaries
2. Core challenges analysis
3. MVP core flow
4. Compliance and qualification analysis
5. Dependency research and interface inventory
6. Cost analysis
7. Technical architecture recommendation

Keep this report simple, staged, and actionable. Avoid turning it into a
full backlog or enterprise target-state architecture.

## Workflow

### 1. Normalize the target

- If the user gives a URL, open that site first and confirm the product name.
- If the user gives only a product name, use web search to identify the official site before deeper analysis.
- If multiple products share the same name, disambiguate by company, domain, tagline, or URL before continuing.

### 2. Gather evidence with web search

- Use web search for the product name, official site, docs, pricing, blog, help center, integrations, legal/compliance pages, and public product demos when relevant.
- Prioritize official sources first: homepage, product pages, docs, help center, pricing, changelog, blog, terms, privacy, trust/compliance pages.
- Use third-party sources only to fill gaps or corroborate unclear claims.
- Keep source URLs for every major conclusion.

### 3. Reconstruct the product from business reality

Work in this order:

1. Identify product category and target users.
2. Build a product-specific glossary of the key domain terms needed to understand the product.
3. Extract positioning from the site's own language and compress it into a one-sentence product definition.
4. Reconstruct the real workflow the product supports or replaces.
5. Identify application scenarios, operating context, and the current alternatives users would realistically use instead.
6. Derive requirements, pain points, dependencies, business model clues, distribution clues, and likely business constraints.
7. Infer the likely technical solution only after the business workflow is clear.

Do not stop at marketing copy. Explain the concrete workflow, main actors, data flow, and operating sequence.

The glossary must stay product-appropriate and domain-specific without hard-coding examples from unrelated products. Define terms in plain language first, then explain what each term means in this product's context.
The glossary may include both business terms and essential external proper nouns when they are necessary to understand the report, such as important platforms, protocols, infrastructure layers, or third-party service providers. Do not turn the glossary into a full dependency inventory.

### 4. Separate evidence from inference

Classify important conclusions into:

- `Confirmed facts`: directly supported by the cited public sources
- `Reasoned inference`: inferred from observable behavior, wording, integrations, workflows, and common implementation patterns

For each non-trivial inference, include a confidence label:

- `High`: explicit or nearly explicit in source material
- `Medium`: strongly implied by public evidence
- `Low`: plausible but speculative

Never claim a specific vendor, architecture, or internal implementation detail without evidence.

### 5. Analyze the technical solution carefully

Infer likely modules, data flows, and architecture patterns only to the degree justified by public behavior. Good candidates include:

- Web app, admin console, mobile app, public API
- Identity and tenant management
- Integrations, sync jobs, webhooks, queues, schedulers
- Workflow orchestration or state machines
- Billing, invoicing, ledger, reporting, reconciliation
- Search, analytics, notifications, audit, compliance

State implementation uncertainty explicitly. Treat diagrams as inferred unless the public sources clearly document the architecture.

### 6. Analyze product risks and constraints

Include a standalone section on the main risks and constraints involved in operating or building the product. Focus on the risks that materially affect viability, defensibility, implementation complexity, or go-to-market execution.

Good categories to consider include:

- Business or market risk
- Operational risk
- Technical risk
- Compliance or legal risk
- Platform or ecosystem dependency risk
- Go-to-market risk

Choose only the categories that are relevant to the product. Do not force a generic checklist if the evidence does not support it.

### 7. Analyze business model, competition, and moat

Include bounded analysis of the product's business position where public evidence allows. Good questions include:

- Who appears to pay
- What value the user is likely paying for
- What the realistic substitutes or alternatives are
- Where the product appears differentiated
- What growth or distribution mechanisms are visible
- What might count as a moat, and what appears easy to copy

Keep this analytical rather than advisory. Describe what appears true about the product; do not turn it into startup strategy unless the user explicitly asks for that.

### 8. Analyze data, security, and compliance posture

When relevant, include a standalone section covering:

- What kinds of data the product likely handles
- What permission or tenancy boundaries likely matter
- What security, privacy, or compliance expectations shape the product

This section is especially important for B2B software, AI products, fintech, health, legal, and workflow systems that touch sensitive data.

### 9. Produce diagrams

Unless the user explicitly opts out, include:

- A detailed workflow flowchart
- A detailed role interaction sequence diagram
- Detailed C4 diagrams for the inferred technical solution

Place all diagrams together in one standalone report section rather than scattering them across the document.

Within that section, keep a stable order:

1. Workflow flowchart
2. Role interaction sequence diagram
3. C4 diagrams

Diagram discipline:

- The workflow diagram should describe the concrete business or user workflow, not a vague marketing funnel.
- The sequence diagram should reflect real actor or system interactions implied by public evidence.
- The C4 diagrams should stay explicitly bounded by evidence and should usually be labeled as inferred unless official architecture documentation exists.
- Do not invent hidden services, vendors, microservices, databases, or internal components unless the public evidence materially supports them.
- If the evidence is thin, simplify the diagrams rather than compensating with speculation.

Use Mermaid by default. Prefer:

- `flowchart` for product workflow
- `sequenceDiagram` for actor and system interactions
- `C4Context`, `C4Container`, and `C4Component` when the product is technically rich enough

Label diagram sections as `Confirmed`, `Mixed`, or `Inferred` when needed. Use [references/diagram-templates.md](references/diagram-templates.md) for templates.

### 10. Run evidence-backed cost research when triggered

When cost research mode is active:

1. List the major external capabilities a similar product would likely require, such as payments, KYC, model inference, OCR, messaging, storage, media processing, data providers, or sales-assisted onboarding.
2. For each capability, determine whether the analyzed product publicly confirms a specific vendor or only implies a capability category.
3. Search official sources first:
   - Official pricing pages
   - Official API pricing or usage pricing docs
   - Official billing, limits, quota, or fee docs
   - Official legal or fee disclosures
   - Official sales/contact pages if pricing is not public
4. Record the direct source URL for every non-trivial cost claim.
5. Separate output into:
   - `Confirmed current-product cost clues`
   - `Confirmed vendor pricing`
   - `Scenario-based build-cost estimates`
6. If official pricing is unavailable, state that clearly and do not invent precise numbers.

Place this material inside the `Cost Analysis` section of the `Build MVP`
report rather than as a separate standalone report.

Use these evidence levels in cost research:

- `High`: official page directly states the pricing, fee, or billing rule
- `Medium`: official source supports the pricing logic, but the analyst must map it to the scenario
- `Low`: official source confirms the cost category exists, but not enough to quantify precisely
- `Do not quantify`: evidence is insufficient for a defensible number

Evidence discipline for cost research:

- Do not guess vendor pricing from memory or industry averages.
- Do not treat a possible vendor as a confirmed vendor.
- Do not present old or third-party pricing as current official pricing.
- If the vendor is unconfirmed, present it only as a candidate option in the build-cost model.
- If the evidence is too thin, mark the item as `Do not quantify`.
- Prefer saying `candidate build option` or `confirmed dependency` over collapsing both into one label.

## Output rules

- Write the final reports in the user's requested language.
- Keep section titles and diagram labels in that same language unless the user asks to preserve English technical terms.
- Include direct source links.
- Call out uncertainty instead of smoothing it over.
- Explain jargon when the requested audience is non-technical.
- Always include a standalone glossary or terminology section near the top of the report, even for non-technical audiences.
- Keep the glossary generic to the analyzed product's domain. Do not reuse terms from previous products unless they actually apply here.
- Keep the product-analysis reports centered on understanding the product as-is: what it does, who it serves, how it works, what constraints shape it, and what is likely true about its business and technical design.
- Do not let product-analysis reports drift into implementation advice, backlog design, system design prescriptions, or pseudo-PRD content.
- Keep build-oriented content in the dedicated `Build MVP` report.
- Structure the `Build MVP` report with the seven required sections from
  the Build MVP template.
- In the `Build MVP` report, explicitly answer which features trigger
  regulation, what qualifications or licenses may be needed, which items
  can be covered by third parties, which interfaces are required by the
  MVP flow, and why the recommended architecture fits an early MVP.
- If compliance, licensing, dependency, or vendor details cannot be
  confirmed, label them as `推测` or `待验证项` when writing in Chinese, or
  use an equivalent localized uncertainty label in other languages.
- Prefer analyzing realistic user alternatives over a shallow list of named competitors.
- Include business model, competitive positioning, growth/distribution, and moat analysis when public evidence supports it.
- Include data, security, and compliance analysis when they materially affect the product.
- In cost research mode, every non-trivial cost claim must include a direct official source URL whenever one exists.
- In cost research mode, distinguish:
  - the analyzed product's apparent business cost structure
  - official third-party pricing facts
  - build-cost estimates based on explicit assumptions
- If official pricing is unavailable, say so clearly instead of inferring a precise number.
- In cost research mode, use the evidence levels `High`, `Medium`, `Low`, and `Do not quantify` consistently.
- In cost research mode, if a cost item lacks a defensible number, output the item, source, and uncertainty anyway instead of omitting it.
- Always include a standalone diagram section unless the user explicitly opts out.
- Keep the diagram section internally ordered as: workflow, sequence, then C4.
- Prefer fewer, tighter diagrams over speculative completeness.
- For comparison tasks, apply the same structure to each product before comparing overlaps and differences.
- Default to separate outputs when different chapter groups serve different decision types.

## Minimum deliverables

Include, at minimum:

- A `Product Understanding` report
- A `Market And Strategy` report
- A `Build MVP` report

The first two are product-analysis outputs.
The third is the MVP-build-oriented output.

## Boundary between analysis and build guidance

Use this distinction consistently:

- `Product analysis`: what the product appears to do, how it is positioned, how users likely adopt it, what dependencies and risks shape it, what business and technical properties are visible from public evidence.
- `Build guidance`: what someone should build, in what order, with which scope, modules, or implementation choices.

When the user asks for general product analysis, still produce all three
default reports, but keep the first two as product analysis and the
third as the build-oriented `Build MVP` output.

In the build-oriented report, distinguish clearly between:

- The analyzed product's apparent business cost structure
- The likely build and operating costs someone would face when creating a similar product

Use the three reference templates when the user wants full reusable structures.
