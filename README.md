# Security Compliance as Code

`security-compliance-as-code` evaluates AWS and Terraform security configuration against executable controls and produces evidence-based compliance reports.

> **Compliance does not guarantee security.** A passing report is a point-in-time signal, not a security certification or substitute for threat modeling, testing, or operational judgment.

## Workflow

Infrastructure -> Collectors -> Security Checks -> Control Mapping -> Evidence -> Compliance Engine -> Risk Evaluation -> Reports

The offline reference implementation accepts a normalized JSON snapshot. Production collectors can adapt AWS APIs, Terraform plan JSON, Checkov, and Prowler output into the same shape without changing controls or reporting.

## Quick start

```bash
python -m pip install -e '.[dev]'
pytest
python -m src.cli --config examples/partial.json --controls controls --format markdown --output reports/example.md
```

Exit code is non-zero when a control fails or errors, making the CLI suitable for a security gate. Reports are available as JSON, CSV, Markdown, and HTML.

## Frameworks and mappings

Controls demonstrate CIS AWS Foundations, NIST CSF, PCI DSS, and ISO/IEC 27001. Mappings identify related outcomes only; they do not claim equivalence, audit coverage, or certification. See [docs/mapping-methodology.md](docs/mapping-methodology.md).

## Repository guide

- [Architecture](docs/architecture.md)
- [Control model](docs/control-model.md)
- [Evidence and risk](docs/evidence-and-risk.md)
- [Workflow and CI/CD](docs/workflow.md)
- [Exception process](docs/exception-process.md)
- [Testing and limitations](docs/testing-and-limitations.md)
- [Security policy](SECURITY.md)

## Integrations

Checkov can validate Terraform plans and Prowler can collect AWS posture evidence in CI. Their output should be normalized into the collector contract before evaluation. The included workflow demonstrates the stages without requiring AWS credentials for pull requests.
