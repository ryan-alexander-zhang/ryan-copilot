# Diagram Templates

Use Mermaid unless the user asks for another diagram format.

Mark each diagram as one of:

- `Confirmed`: mostly derived from explicit public material
- `Mixed`: combines public evidence with bounded inference
- `Inferred`: reverse-engineered from behavior and public clues

## Workflow Flowchart

```mermaid
flowchart TD
    A[User enters product or workspace] --> B[Connect account or configure workspace]
    B --> C[System validates identity, access, and prerequisites]
    C --> D[Core business event occurs]
    D --> E[Product evaluates rules, policies, or workflow state]
    E --> F[Product triggers action or next step]
    F --> G[System persists state, audit trail, or ledger record]
    G --> H[Users receive status, notification, dashboard update, or report]
```

## Role Interaction Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Buyer
    actor Operator
    participant Product
    participant ExternalSystem

    Buyer->>Product: Configure account, policy, or workflow
    Product-->>Operator: Invite, assign, or request action
    Operator->>Product: Complete setup or submit business action
    ExternalSystem-->>Product: Send event, sync, or status change
    Product->>Product: Evaluate rules and update workflow state
    Product->>ExternalSystem: Trigger downstream action
    Product-->>Buyer: Show status, alert, or report
```

## C4 Context

```mermaid
C4Context
    title Inferred Product Context
    Person(primary_user, "Primary User", "Main operator or analyst")
    Person(secondary_user, "Secondary User", "Collaborator, approver, or customer")
    System(product, "Product", "Public-facing product being analyzed")
    System_Ext(ext_a, "External Platform", "Source or destination of business data")
    System_Ext(ext_b, "Identity/Payment/Messaging System", "Third-party dependency")

    Rel(primary_user, product, "Uses")
    Rel(secondary_user, product, "Interacts with")
    Rel(product, ext_a, "Reads or writes data")
    Rel(product, ext_b, "Delegates key external capability")
```

## C4 Container

```mermaid
C4Container
    title Inferred Product Containers
    Person(user, "User")
    System_Boundary(product_boundary, "Product") {
        Container(web, "Web App", "Web UI", "Dashboard and workflow interface")
        Container(api, "Backend/API", "Application service", "Handles product logic and integrations")
        Container(worker, "Async Worker", "Jobs/queues", "Runs scheduled and event-driven tasks")
        ContainerDb(db, "Operational Data Store", "Database", "Stores product state, entities, and reports")
    }
    System_Ext(ext, "External System", "Partner platform or infrastructure")

    Rel(user, web, "Uses")
    Rel(web, api, "Calls")
    Rel(api, db, "Reads and writes")
    Rel(api, worker, "Schedules jobs")
    Rel(worker, ext, "Syncs or triggers")
    Rel(api, ext, "Calls external APIs")
```

## C4 Component

```mermaid
C4Component
    title Inferred Core Components
    Container_Boundary(api_boundary, "Backend/API") {
        Component(auth, "Auth and Tenant Module", "Service", "Identity, roles, permissions, tenancy")
        Component(workflow, "Workflow Orchestrator", "Service", "State transitions, approvals, automation")
        Component(integrations, "Integration Layer", "Service", "APIs, webhooks, sync logic")
        Component(reporting, "Reporting and Audit Module", "Service", "Dashboards, exports, traceability")
    }
    ContainerDb(db, "Operational Data Store", "Database", "Entities, events, reports")
    System_Ext(ext, "External System", "Third-party platform")

    Rel(auth, workflow, "Authorizes actions for")
    Rel(workflow, integrations, "Invokes")
    Rel(workflow, reporting, "Emits status and outcomes to")
    Rel(auth, db, "Reads and writes")
    Rel(workflow, db, "Reads and writes")
    Rel(reporting, db, "Reads")
    Rel(integrations, ext, "Calls")
```

## Diagram Guidance

- Tailor actor names and system names to the actual product.
- Keep the workflow and sequence diagrams concrete and business-specific.
- Treat C4 diagrams as inferred unless official architecture documentation exists.
- Avoid naming vendors unless sources confirm them.
- If the public product is simple, a context diagram plus a compact container diagram may be enough; otherwise include all three C4 levels.
