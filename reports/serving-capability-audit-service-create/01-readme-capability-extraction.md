# README Capability Extraction

## Scope Note

This document follows Stage 1 strictly from the repository root README only. The later code audit is intentionally narrowed to the `Service create` chain, but the capability list below reflects the repository-level claims that the README makes.

## Project Positioning

Knative Serving builds on Kubernetes to deploy and serve applications and functions as serverless containers, with an emphasis on easy startup and production-scale serving behavior.

## Core Capability List

| Capability | README evidence | Boundary | Initial confidence |
| --- | --- | --- | --- |
| Rapid deployment of serverless containers | README says Knative Serving supports "deploying and serving of applications and functions as serverless containers" and provides "Rapid deployment of serverless containers". | What it is: declarative deployment and serving primitives for serverless workloads on Kubernetes. What it is not: image build, source-to-image, or CI/CD automation. | high |
| Automatic scaling up and down to zero | README explicitly lists "Automatic scaling up and down to zero". | What it is: workload scaling behavior managed by Serving. What it is not: a generic Kubernetes autoscaler for arbitrary workloads outside Serving's model. | high |
| Routing and network programming | README explicitly lists "Routing and network programming". | What it is: request-routing primitives and networking integration for exposed services. What it is not: a full service mesh or arbitrary ingress controller replacement by itself. | medium |
| Point-in-time snapshots of deployed code and configurations | README explicitly lists "Point-in-time snapshots of deployed code and configurations". | What it is: immutable deployment snapshots captured as part of Serving's rollout model. What it is not: source control versioning or full backup/restore tooling. | medium |

## Scoped Audit Target

The user-requested audit target is the normalized capability:

`Knative Service creation to Configuration, Revision, and Route materialization`

This scoped target is justified by combining three README claims:

- `Rapid deployment of serverless containers`
- `Routing and network programming`
- `Point-in-time snapshots of deployed code and configurations`

`Automatic scaling up and down to zero` remains a documented repository capability, but it is not part of the primary `create` control-plane path being audited here.

## Boundary For The Scoped Target

- What it is:
  - How a newly created Knative `Service` object is admitted, defaulted, validated, reconciled, and expanded into child resources that make the service reachable.
  - How immutable snapshot semantics appear during create through `Configuration` and `Revision` resources.
  - How initial traffic routing intent is materialized through `Route`.
- What it is not:
  - Runtime request execution inside queue-proxy or user containers after the service is already ready.
  - Autoscaler steady-state behavior after the first create completes.
  - Cluster installation, CRD generation, or operator lifecycle management.

## Initial Hypothesis For Later Verification

Based on README inference, the `Service create` path likely relies on a top-level Serving API object that fans out into immutable revision state and networking state. Confidence for this hypothesis is `medium` because the README does not name concrete modules, APIs, or controllers.
