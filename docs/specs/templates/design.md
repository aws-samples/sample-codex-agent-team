# Design: <Title>

> Architecture, repository structure, and infrastructure design for `<slug>`. Keep Security Considerations for production-impacting or AWS-heavy work.

## Architecture Overview

High-level description, components, and request/data flow. Link or include diagrams when useful.

## Repository / Module Structure

```text
<tree of dirs and key files this work will create or touch>
```

## Components

### <Component Name>

- Responsibility: <what it owns>
- Interface: <public API / events / inputs and outputs>
- Dependencies: <upstream/downstream>

## Data Model

Entities, schemas, storage choices, retention, and data classification.

## Infrastructure Design

AWS services, IaC approach, environments, deploy/rollback strategy, and outputs consumed by application code or other stacks.

## Security Considerations

Reconcile against `aws-security-guidelines` when AWS or production data is involved.

- Authentication and authorization
- Least-privilege IAM
- Encryption at rest
- Encryption in transit
- Secrets management
- Network exposure
- Logging and audit
- Data classification and tagging
- Threat model notes

## Tradeoffs And Alternatives

What was considered and rejected, with reasoning.

## Open Design Questions

- [ ] <question>
