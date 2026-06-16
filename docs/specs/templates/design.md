# Design: <Title>

> Architecture, module layout, integration contracts, and operational design for `<slug>`.

## Architecture Overview

Describe components and how requests, data, or control flow through them.

```text
<ASCII diagram or link to diagram>
```

## Repository / Module Structure

```text
<tree of directories and key files this work will create or touch>
```

## Components

### <Component Name>

- Responsibility:
- Interface:
- Dependencies:

## Data Model

Describe entities, schemas, storage choices, retention, and sensitivity.

## Infrastructure Design

Describe environments, deploy path, rollback path, config, outputs, and operational dependencies.

For smoke, staging, or deployment checks, include:

- Target classification and non-production preflight.
- Required environment variables or parameters.
- Retry count, timeout, delay, and abort criteria.
- Evidence to capture, such as command output, target classification, artifact identifier, and final PASS or FAIL.

## Security Considerations

- Authentication and authorization:
- Secrets management:
- Data protection:
- Network exposure:
- Logging and audit:
- Non-production target guardrails for smoke or deploy checks:
- Threat model notes:

## Trade-offs & Alternatives

Document what was considered and rejected.

## Open Design Questions

- [ ] <question>
