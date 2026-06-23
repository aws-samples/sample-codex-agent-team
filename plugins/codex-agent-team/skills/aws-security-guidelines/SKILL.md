---
name: aws-security-guidelines
description: Service-specific AWS security requirements and verification checklists for Codex. Use when creating, configuring, reviewing, or planning AWS resources, AWS IaC, deployment handoffs, production readiness, data security controls, or security reviews for services such as S3, Lambda, DynamoDB, RDS, EBS, API Gateway, Aurora DSQL, Amplify, IAM, KMS, Secrets Manager, CloudTrail, and CloudWatch.
---

# AWS Security Guidelines

Use these service-specific security requirements for AWS work. Apply them when creating, configuring, planning, or reviewing AWS resources.

## Operating Rules

- Treat unknown AWS environments as production until proven otherwise.
- Prefer read-only verification commands (`list`, `describe`, `get`, `plan`, `diff`, dry-run) before any mutating operation.
- Do not run mutating AWS, CDK, Terraform, or deployment commands unless the user explicitly requests or approves them.
- When proposing mutating commands, state the expected impact and verification command.
- Never inline secrets in code, docs, config, tests, prompts, or command examples.
- Convert any durable security notes from this skill into repo-local `.codex/specs/<slug>/` artifacts when a spec workflow is in play.

## Data Security Implementation Order

Implement data security controls in phased priority order.

### Phase 1: Blocks Task Completion

1. Encryption at rest: `aws <service> describe-<resource> --<id> <value> | jq '.EncryptionConfiguration'`
   - Expect an AWS Key Management Service (AWS KMS) key ARN.
2. TLS enforcement for Amazon S3:
   - Add a DENY policy to reject non-TLS requests.
   - `Principal: "*"` in a DENY statement is an AWS-recommended pattern to enforce TLS for all callers. This differs from ALLOW policies with wildcards, which grant overly broad permissions.
   - Policy pattern:
     ```json
     {
       "Effect": "Deny",
       "Principal": "*",
       "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
       "Resource": ["arn:aws:s3:::<your-bucket>/*", "arn:aws:s3:::<your-bucket>"],
       "Condition": {"Bool": {"aws:SecureTransport": "false"}}
     }
     ```
   - Verify with `aws s3api get-bucket-policy`.
3. Block Public Access:
   - Configure with `aws s3api put-public-access-block --bucket <name> --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true`.
   - Verify with `aws s3api get-public-access-block`.

### Phase 2: Required For Review PASS

4. Access logging:
   - Configure with `aws s3api put-bucket-logging --bucket <name> --bucket-logging-status file://logging.json`.
   - Verify with `aws s3api get-bucket-logging`.
5. Data classification tags:
   - Configure with `aws s3api put-bucket-tagging --bucket <name> --tagging 'TagSet=[{Key=data-classification,Value=confidential}]'`.
   - Verify with `aws s3api get-bucket-tagging`.

### Phase 3: Production Requirement

6. Versioning:
   - Configure with `aws s3api put-bucket-versioning --bucket <name> --versioning-configuration Status=Enabled`.
   - Verify with `aws s3api get-bucket-versioning`.
   - Expect `Status=Enabled` for `data-classification=confidential|internal`.
7. MFA Delete:
   - Configure with `aws s3api put-bucket-versioning --bucket <name> --versioning-configuration Status=Enabled,MFADelete=Enabled --mfa "<device-arn> <code>"`.
   - Verify with `aws s3api get-bucket-versioning`.
   - Expect `MFADelete=Enabled` for `data-classification=confidential`.
8. BYOK documentation:
   - Create `.codex/specs/<slug>/kms-key-usage.md` documenting key ARNs, rotation schedule, and access policies.
   - Flag the item for security review in `review.md`.

## Data Security Verification Checklist

For infrastructure handling sensitive data, verify:

1. Encryption at rest: `aws <service> describe-<resource> | jq '.EncryptionConfiguration'`
   - Expect an AWS KMS key ARN.
2. Encryption in transit:
   - Verify TLS 1.2+ enforcement via service configuration or bucket policies.
3. Key management:
   - Verify AWS KMS key usage is documented in `.codex/specs/<slug>/kms-key-usage.md`.
4. Data classification:
   - `aws <service> get-<resource>-tagging | jq '.TagSet[] | select(.Key=="data-classification")'`
   - Expect a tag to be present.
5. Access logging:
   - `aws <service> get-<resource>-logging`
   - Expect logging enabled.

## Amazon Simple Storage Service (Amazon S3)

- Encryption at rest using AWS KMS keys: Critical if missing.
- Encryption in transit via `aws:SecureTransport` bucket policy condition: Critical if missing.
- Block Public Access enabled: Critical if missing, unless public access is explicitly documented and justified.
- Bucket policies enforce TLS/HTTPS using `aws:SecureTransport` condition and deny when false: Critical if missing.
- Versioning enabled for buckets containing critical data: Warning if missing.
- MFA Delete configured for buckets with sensitive data: Warning if missing.
- Access logging enabled to an audit bucket: Warning if missing.
- Data classification tags present: Warning if missing.
- BYOK customer-managed AWS KMS key usage documented and flagged for security review: Warning if not documented.
- Key management strategy documented, including key rotation and access policies: Warning if missing.

## AWS Lambda

- Execution role permissions:
  - Apply least-privilege IAM policies.
  - Give each function its own execution role. Never share roles across functions.
  - Verify with `aws iam simulate-principal-policy --policy-source-arn <role-arn> --action-names <actions>`.
  - Expect `Deny` for unused actions.
- Environment variable encryption:
  - Use AWS KMS encryption for environment variables containing sensitive data.
  - Verify with `aws lambda get-function-configuration --function-name <name> | jq '.KMSKeyArn'`.
  - Expect an AWS KMS key ARN for functions with sensitive environment variables.
- VPC configuration:
  - Place functions in an Amazon VPC when accessing private resources such as Amazon RDS, ElastiCache, or internal APIs.
  - Configure security groups to restrict outbound traffic.
  - Verify with `aws lambda get-function-configuration --function-name <name> | jq '.VpcConfig'`.
- Resource-based policies:
  - Restrict invoke permissions to specific principals.
  - Verify with `aws lambda get-policy --function-name <name>`.
  - Expect no wildcard principals.
- Reserved concurrency:
  - Set reserved concurrency to prevent runaway invocations from exhausting account limits.

## Amazon DynamoDB

- Encryption at rest:
  - Use AWS KMS keys, not default AWS owned keys, for tables containing sensitive data.
  - Verify with `aws dynamodb describe-table --table-name <name> | jq '.Table.SSEDescription'`.
  - Expect `SSEType=KMS` with `KMSMasterKeyArn`.
- Point-in-time recovery:
  - Enable PITR for all tables.
  - Verify with `aws dynamodb describe-continuous-backups --table-name <name> | jq '.ContinuousBackupsDescription.PointInTimeRecoveryDescription'`.
  - Expect `PointInTimeRecoveryStatus=ENABLED`.
- IAM policies for table access:
  - Use fine-grained IAM conditions such as `dynamodb:LeadingKeys` and `dynamodb:Attributes` to restrict row and attribute-level access.
  - Never grant `dynamodb:*` on production tables.
- Data classification tags:
  - Apply data classification tags.
  - Verify with `aws dynamodb list-tags-of-resource --resource-arn <arn> | jq '.Tags[] | select(.Key=="data-classification")'`.
- Encryption in transit:
  - Use HTTPS endpoints only. This is the AWS SDK default, but verify custom clients.

## Amazon Relational Database Service (Amazon RDS)

- Encryption at rest:
  - Enable at creation with AWS KMS keys. It cannot be enabled after creation.
  - Verify with `aws rds describe-db-instances --db-instance-identifier <name> | jq '.DBInstances[0].StorageEncrypted, .DBInstances[0].KmsKeyId'`.
  - Expect `true` with a KMS key ARN.
- Encryption in transit:
  - Enforce SSL/TLS connections via parameter groups, such as `rds.force_ssl=1` for PostgreSQL or `require_secure_transport=ON` for MySQL.
  - Verify with `aws rds describe-db-parameters --db-parameter-group-name <name> | jq '.Parameters[] | select(.ParameterName=="rds.force_ssl")'`.
- Authentication:
  - Use IAM database authentication where supported.
  - For password auth, store credentials in AWS Secrets Manager with automatic rotation.
  - Verify with `aws rds describe-db-instances --db-instance-identifier <name> | jq '.DBInstances[0].IAMDatabaseAuthenticationEnabled'`.
- Network isolation:
  - Place databases in private subnets with no public accessibility.
  - Verify with `aws rds describe-db-instances --db-instance-identifier <name> | jq '.DBInstances[0].PubliclyAccessible'`.
  - Expect `false`.
- Automated backups:
  - Enable backups with an appropriate retention period.
  - Verify with `aws rds describe-db-instances --db-instance-identifier <name> | jq '.DBInstances[0].BackupRetentionPeriod'`.
  - Expect at least `7`.
- Data classification tags:
  - Apply tags.
  - Verify with `aws rds list-tags-for-resource --resource-name <arn> | jq '.TagList[] | select(.Key=="data-classification")'`.

## Amazon Elastic Block Store (Amazon EBS)

- Encryption at rest:
  - Enable default encryption in the account or per-volume with AWS KMS keys.
  - Verify with `aws ec2 describe-volumes --volume-ids <id> | jq '.Volumes[0].Encrypted, .Volumes[0].KmsKeyId'`.
  - Expect `true` with a KMS key ARN.
- Snapshots:
  - Encrypt all snapshots.
  - Verify with `aws ec2 describe-snapshots --snapshot-ids <id> | jq '.Snapshots[0].Encrypted'`.
- Data classification tags:
  - Apply tags.
  - Verify with `aws ec2 describe-volumes --volume-ids <id> | jq '.Volumes[0].Tags[] | select(.Key=="data-classification")'`.

## Amazon API Gateway

- Authorization:
  - Configure appropriate authorizers, such as IAM, Cognito, or Lambda, for all routes.
  - Critical if missing. Do not leave endpoints open or unauthenticated unless explicitly documented.
- Throttling:
  - Set rate limiting and burst limits on all stages and methods.
  - Verify with `aws apigateway get-method-response` or `aws apigatewayv2 get-stage`.
- WAF integration:
  - Attach AWS WAF web ACL for public-facing APIs.
  - Warning if missing.
- Mutual TLS:
  - Enable mTLS for API-to-API communication when handling sensitive data.
  - Warning if missing.
- Access logging:
  - Enable access logging to CloudWatch Logs or Kinesis Data Firehose.
  - Verify with `aws apigateway get-stage --rest-api-id <id> --stage-name <stage> | jq '.accessLogSettings'`.
  - Expect a destination ARN.
  - Warning if missing.
- Resource policies:
  - Restrict API access by source IP or VPC endpoint for private APIs.
  - Verify with `aws apigateway get-rest-api --rest-api-id <id> | jq '.policy'`.
- Request validation:
  - Enable request validators for body, query string, and path parameters.
  - Warning if missing.

## Aurora DSQL

- IAM authentication:
  - Use IAM database authentication. Never store database passwords.
  - Generate auth tokens via `aws dsql generate-db-connect-auth-token`.
  - Verify IAM policies grant `dsql:DbConnectAdmin` only to required principals.
  - Critical if password-based auth is used.
- Encryption at rest:
  - Aurora DSQL encrypts data at rest by default using AWS-managed keys.
  - For sensitive data, verify encryption configuration.
- Encryption in transit:
  - All DSQL connections use TLS by default.
  - Verify application connection strings use `sslmode=verify-full`.
  - Critical if TLS is disabled.
- Network isolation:
  - Use VPC endpoints for DSQL access from within VPCs.
  - Verify with `aws ec2 describe-vpc-endpoints --filters Name=service-name,Values=dsql`.
  - Warning if VPC workloads access DSQL over the public internet.
- Fine-grained access:
  - Use PostgreSQL `GRANT` and `REVOKE` for table and column-level access control.
  - Never grant `superuser` to application roles.
- Multi-tenant isolation:
  - For multi-tenant schemas, enforce row-level security policies.
  - Verify with a read-only query: `SELECT * FROM pg_policies`.
  - Expect row-level security policies for tenant tables.
- Audit logging:
  - Enable query logging for compliance.
  - Verify audit trail configuration.

## AWS Amplify Gen 2

- Authentication:
  - Use Amplify Auth backed by Amazon Cognito.
  - Configure MFA, password policies, and account recovery.
  - Verify Cognito user pool settings.
  - Critical if auth is unenforced on protected routes.
- Authorization rules:
  - Define per-model authorization rules in the Amplify data schema with `@auth` directives.
  - Verify owner-based and group-based access.
  - Critical if models are publicly readable or writable without explicit justification.
- API keys:
  - Never expose Amplify API keys in client-side code for production.
  - Use IAM or Cognito-based auth for production APIs.
- Storage:
  - Configure S3 storage access levels such as guest, authenticated, and owner appropriately.
  - Verify bucket policies.
  - Warning if overly permissive.
- Environment separation:
  - Use separate Amplify sandbox and production environments.
  - Never deploy development configurations to production.

## General Requirements

- Store all secrets in AWS Secrets Manager or AWS Systems Manager Parameter Store. Do not inline them in code or IaC.
- Tag all resources with `service`, `environment`, `owner`, `cost-center`, and `data-classification`.
- Document key management strategy in `design.md`, including rotation policies.
- Apply data classification tags (`data-classification: public|internal|confidential`) to all resources handling data.
- Enable access logging for data operations: CloudTrail, S3 access logs, database audit logs, and service-specific logs.
