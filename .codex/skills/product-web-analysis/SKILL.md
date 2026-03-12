---
name: product-web-analysis
description: Analyze a product from a user-provided product name or URL using web search and official public sources, then produce a structured product intelligence report in the user's requested language. Use when Codex needs product analysis, website analysis, product research, competitor analysis, product teardown, reverse analysis of a SaaS or tool, or an explanation of what a product does, who it serves, use cases, requirements, pain points, dependencies, business model clues, or likely technical architecture. Trigger on requests such as analyze this product, analyze this website, explain this product, summarize this SaaS, infer the architecture, compare these products, or Chinese requests like 分析这个产品、分析这个网站、产品分析、竞品分析、产品拆解、技术架构推断、产品调研、逆向分析这个产品、根据产品名称或URL生成报告. Generate reports with flowcharts, sequence diagrams, and C4 diagrams while clearly separating confirmed facts from reasoned inference.
---

# Product Web Analysis

## Overview

Use this skill to research a public product on the web and turn scattered evidence into a structured report. Accept either a product name or a product URL, adapt the report language to the user's request, and keep a hard boundary between confirmed facts and inference.

This skill is primarily for understanding and analyzing an existing product as it appears in public. It is not primarily a product design, implementation planning, or PRD-writing workflow.

Typical Chinese triggers include `分析这个产品`, `分析这个网站`, `做一个产品分析`, `做竞品分析`, `拆解这个 SaaS`, `推断技术架构`, and `根据这个 URL 做产品调研`.

Read [references/report-template.md](references/report-template.md) when you need the full report structure. Read [references/diagram-templates.md](references/diagram-templates.md) when generating Mermaid diagrams.

## Inputs

Collect these inputs from the user request or infer reasonable defaults:

- Product identifier: product name, URL, or both
- Analysis objective: general analysis, competitor comparison, architecture inference, PRD-style decomposition, investor-style summary, and so on
- Preferred language for the final report
- Depth: `basic`, `detailed`, or `expert`
- Audience: `beginner`, `pm`, `founder`, `engineer`, `architect`, or `investor`
- Whether to compare multiple products

If the user does not specify language, answer in the language used by the user.

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

## Output rules

- Write the final report in the user's requested language.
- Keep section titles and diagram labels in that same language unless the user asks to preserve English technical terms.
- Include direct source links.
- Call out uncertainty instead of smoothing it over.
- Explain jargon when the requested audience is non-technical.
- Always include a standalone glossary or terminology section near the top of the report, even for non-technical audiences.
- Keep the glossary generic to the analyzed product's domain. Do not reuse terms from previous products unless they actually apply here.
- Keep the report centered on understanding the product as-is: what it does, who it serves, how it works, what constraints shape it, and what is likely true about its business and technical design.
- Do not let product analysis sections drift into implementation advice, backlog design, system design prescriptions, or pseudo-PRD content.
- Treat build-oriented content as a separate, explicitly bounded section. It should stay short unless the user explicitly asks for a builder-focused or implementation-focused analysis.
- Prefer analyzing realistic user alternatives over a shallow list of named competitors.
- Include business model, competitive positioning, growth/distribution, and moat analysis when public evidence supports it.
- Include data, security, and compliance analysis when they materially affect the product.
- Always include a standalone diagram section unless the user explicitly opts out.
- Keep the diagram section internally ordered as: workflow, sequence, then C4.
- Prefer fewer, tighter diagrams over speculative completeness.
- For comparison tasks, apply the same structure to each product before comparing overlaps and differences.

## Minimum report contents

Include, at minimum:

- Product summary
- One-sentence product definition
- Key terminology or glossary
- What the product actually does
- Target users and roles
- Application scenarios
- Current alternatives or substitutes
- Implemented requirements
- Pain points solved
- Business model and monetization clues
- Competitive positioning and differentiation
- Growth or distribution clues
- Dependencies: business, external product/infrastructure, technical
- Key risks and constraints
- Data, security, and compliance considerations
- Moat and copyability
- Likely technical solution
- Confirmed facts vs reasoned inference
- Build-a-similar-product notes
- A standalone diagram section containing workflow, sequence, and C4 diagrams

## Boundary between analysis and build guidance

Use this distinction consistently:

- `Product analysis`: what the product appears to do, how it is positioned, how users likely adopt it, what dependencies and risks shape it, what business and technical properties are visible from public evidence.
- `Build guidance`: what someone should build, in what order, with which scope, modules, or implementation choices.

When the user asks for general product analysis, keep the main report in `Product analysis`. Only include a short build-oriented section at the end. If the user explicitly asks for a reverse-engineering or builder-focused deliverable, you may expand the build-oriented section while still separating evidence from prescription.

In the build-oriented section, include cost considerations when relevant. Distinguish clearly between:

- The analyzed product's apparent business cost structure
- The likely build and operating costs someone would face when creating a similar product

Use [references/report-template.md](references/report-template.md) when the user wants a full reusable structure.
