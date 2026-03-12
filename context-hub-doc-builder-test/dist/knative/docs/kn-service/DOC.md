---
name: kn-service
description: "Knative client CLI command reference for managing Knative services."
metadata:
  languages: "text"
  versions: "1.21.0"
  revision: 1
  updated-on: "2026-03-11"
  source: official
  tags: "cli,knative,service"
---

# kn service

## What This Covers

`kn service` is the top-level Knative client command group for managing Knative services in a cluster. Use it as the entry point before calling subcommands such as `create`, `update`, `describe`, `list`, or `delete`.

## Source Material

- `https://github.com/knative/client/blob/release-1.21/docs/cmd/kn_service.md`

## Quick Start

List the available subcommands for working with Knative services:

```bash
kn service
```

Show command help:

```bash
kn service --help
```

## Common Workflows

Use `kn service` as the namespace for service lifecycle operations:

- `kn service create` to create a service.
- `kn service update` to update a service.
- `kn service describe` to inspect a service.
- `kn service list` to list services.
- `kn service delete` to remove services.
- `kn service apply` to apply a service declaration.
- `kn service export` and `kn service import` to move service definitions.
- `kn service wait` to wait until a service is ready.

## Options

```text
-h, --help   help for service
```

## Inherited Options

The command inherits standard Knative client and Kubernetes context flags, including:

- `--as`
- `--as-group`
- `--as-uid`
- `--cluster`
- `--config`
- `--context`
- `--kubeconfig`
- `--log-http`

## Constraints

- Requires a working Kubernetes and Knative environment plus a valid kubeconfig context.
- Behavior depends on the selected cluster, kubeconfig, and impersonation flags.
- This page is only the command-group entry point. Detailed behavior lives in subcommand docs.

## Reference Files

- `references/examples.md` for common command invocations.
- `references/subcommands.md` for linked child commands.

## Reference Map

Use the main page for command discovery. Load the reference files when you need concrete invocations or the child-command list.
