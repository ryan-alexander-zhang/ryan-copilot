---
name: product-web-analysis
description: >-
  Analyze a product from a user-provided product name or URL using web
  search and official public sources, then produce three structured
  reports in the user's requested language: Product Understanding,
  Market And Strategy, and Build MVP. Use when Codex needs product
  analysis, website analysis, product research, competitor analysis,
  product teardown, reverse analysis of a SaaS or tool, or an MVP build
  assessment for a similar product, including scope, dependencies,
  compliance, cost, and technical architecture suggestions. Trigger on
  requests such as analyze this product, analyze this website, explain
  this product, summarize this SaaS, infer the architecture, compare
  these products, assess whether it is worth building, estimate MVP cost
  or feasibility, or Chinese requests like 分析这个产品、分析这个网站、产品分析、竞品分析、产品拆解、技术架构推断、产品调研、逆向分析这个产品、根据产品名称或URL生成报告、评估能不能做、做MVP拆解、估算开发成本.
  Generate reports with flowcharts, sequence diagrams, and C4 diagrams
  while clearly separating confirmed facts from reasoned inference.
---

# Product Web Analysis

## Overview

Use this skill to research a public product on the web and turn
scattered evidence into three structured reports. Accept either a
product name or a product URL, adapt the report language to the user's
request, and keep a hard boundary between confirmed facts and
inference.

This skill is primarily for understanding and analyzing an existing
product as it appears in public. The first two reports stay analytical.
The third report is the only build-oriented output and should stay
focused on an early MVP rather than a full PRD.

Typical Chinese triggers include `分析这个产品`, `分析这个网站`, `做一个产品分析`,
`做竞品分析`, `拆解这个 SaaS`, `推断技术架构`, and `根据这个 URL 做产品调研`.

Read these templates when you need the full output structure:

- [references/product-understanding-template.md](references/product-understanding-template.md)
- [references/market-strategy-template.md](references/market-strategy-template.md)
- [references/build-mvp-template.md](references/build-mvp-template.md)
- [references/diagram-templates.md](references/diagram-templates.md)

## Minimal Inputs

This skill should normally be called with only the smallest necessary
inputs. Do not expose a large parameter surface unless the user clearly
needs it.

Required:

- Product identifier: product name, URL, or both

Optional:

- Preferred language for the final report
- Comparison targets when the user explicitly wants competitor comparison
- Output format override when the user explicitly wants a single-file
  report instead of the default three-report output
- Output path override when the user explicitly wants a different
  directory; otherwise use the default file output path described below

If the user does not specify language, answer in the language used by the user.

Do not ask the user to choose an analysis objective, audience, evidence
mode, diagram mode, or terminology mode. Those are internal defaults.

## Internal Defaults

Unless the user explicitly overrides them, use these defaults:

- Deliverables: always produce `Product Understanding`, `Market And
  Strategy`, and `Build MVP`
- Output format: three separate reports
- File output: mandatory
- Default output directory: relative to the current working directory,
  `reports/{project-name}/`
- Default report filenames:
  - `01-product-understanding.md`
  - `02-market-and-strategy.md`
  - `03-build-mvp.md`
- Source policy: official sources first, third-party sources only to fill
  gaps or corroborate
- Cost research: enabled by default for the `Build MVP` report
- Diagrams: enabled by default
- Evidence model: always separate `Confirmed facts` from `Reasoned
  inference`
- Uncertainty labels: always mark uncertain items as `推测` or `待验证项`
  in Chinese, or equivalent labels in the output language
- Writing stance: neutral, analytical, and fact-first rather than tuned
  to a role-based audience
- Depth: default to a solid `detailed` level; only compress or expand if
  the user explicitly asks for a shorter or deeper version
- English technical terms: preserve when they improve precision; do not
  expose this as a user-facing parameter

`{project-name}` normalization rules:

- Prefer the confirmed official product name from the analyzed site.
- Convert the name to a filesystem-safe slug suitable for a directory
  name.
- If the official name cannot be confirmed, derive the slug from the
  provided domain or product identifier.
- Do not ask the user to choose a directory name unless ambiguity blocks
  reasonable normalization.

Mandatory file-output rule:

- Writing the deliverables to files is required, not optional.
- Do not treat chat-only output as sufficient completion.
- Even when summarizing results in chat, write the report files first and
  then reference their paths in the response.
- If the user explicitly asks for a single-file report, still write it to
  disk under `reports/{project-name}/`, using a single Markdown file
  instead of the three default files.

## Cost Research Default

Evidence-backed cost research is on by default for the `Build MVP`
report.

Strengthen the cost-research pass when the user asks for any of the
following:

- Whether it is worth building a similar product
- Development, operating, or vendor cost analysis
- API pricing, infrastructure pricing, or external dependency fees
- Unit economics or cost structure validation
- Official links, official pricing pages, billing pages, or legal fee pages
- High-confidence cost analysis with precise source attribution

In this mode, cost-related claims must be treated as a separate
evidence-gathering task rather than lightweight commentary.

## Default Deliverables

By default, produce three separate reports rather than one monolithic
report:

1. `Product Understanding`
2. `Market And Strategy`
3. `Build MVP`

All three are default outputs. Do not collapse them into one long report
unless the user explicitly asks for a single-file format.

Default file layout:

- `reports/{project-name}/01-product-understanding.md`
- `reports/{project-name}/02-market-and-strategy.md`
- `reports/{project-name}/03-build-mvp.md`

These files are mandatory deliverables by default.

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

Special requirement for section 5:

- Do not stop at a short or generic bullet list.
- Expand `Dependency research and interface inventory` into a detailed
  inventory organized in at least two views:
  1. end-to-end flow view
  2. module view
- In the flow view, group interfaces by concrete workflow stages such as
  onboarding, KYC, bank linking, authorization, debit, payout,
  reconciliation, notifications, invoicing, and cross-border handling
  when relevant.
- In the module view, group interfaces by product or system modules such
  as identity, tenant management, split rules, ledger, workflow,
  reporting, notifications, compliance, and ops tooling.
- For every external interface, include the exact vendor, product or API
  family, specific endpoint or narrowest official guide, call timing,
  key inputs, key outputs or webhook callbacks, backup option, and
  whether the dependency is confirmed or inferred.
- Verify documentation URLs with live web search on the analysis date.
  Prefer endpoint-level or guide-level official docs over generic
  homepages.
- When a vendor publishes versioning or changelog docs that materially
  affect interface freshness, include them or cite them in that section.
- If no public API docs exist, state that explicitly as of the analysis
  date instead of pretending the interface is documented.

## Workflow

### 1. Normalize the target

- If the user gives a URL, open that site first and confirm the product name.
- If the user gives only a product name, use web search to identify the official site before deeper analysis.
- If multiple products share the same name, disambiguate by company, domain, tagline, or URL before continuing.
- Normalize the output directory name from the confirmed product name and
  prepare `reports/{project-name}/` in the current working directory
  unless the user explicitly requested a different location.

### 2. Gather evidence with web search

- Use web search for the product name, official site, docs, pricing, blog, help center, integrations, legal/compliance pages, and public product demos when relevant.
- Prioritize official sources first: homepage, product pages, docs, help center, pricing, changelog, blog, terms, privacy, trust/compliance pages.
- Use third-party sources only to fill gaps or corroborate unclear claims.
- Keep source URLs for every major conclusion.
- For `Build MVP` section 5, run a dedicated documentation pass using web
  search to verify current official API or integration docs for each
  major external interface included in the MVP flow.

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

### 11. Write the reports to files

- Writing files is mandatory for this skill.
- By default, write three Markdown files under
  `reports/{project-name}/`:
  - `01-product-understanding.md`
  - `02-market-and-strategy.md`
  - `03-build-mvp.md`
- If the user explicitly requested a single-file output, still write it
  under `reports/{project-name}/` as one Markdown file.
- After writing the files, return a concise chat response that points to
  the generated file paths and optionally summarizes the key findings.

## Output rules

- Write the final reports in the user's requested language.
- Always write the final reports to local Markdown files before sending
  the chat response.
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
- In the `Build MVP` report, make the `Dependency research and interface
  inventory` section detailed rather than brief, and include concrete
  official documentation URLs for each major external interface verified
  via web search on the analysis date.
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
- In the default case, the required file outputs are:
  - `reports/{project-name}/01-product-understanding.md`
  - `reports/{project-name}/02-market-and-strategy.md`
  - `reports/{project-name}/03-build-mvp.md`
- In the final chat response, include the written file paths rather than
  only pasting the full report into chat.

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
