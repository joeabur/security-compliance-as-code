# Compliance Workflow

GitHub Actions runs lint, unit tests, Terraform formatting and validation, security checks, compliance evaluation, mapping review, report publication, and a security gate. Checkov is appropriate for Terraform static analysis; Prowler is appropriate for AWS posture collection. Their findings should be normalized before entering the engine.

Pull requests can use offline fixtures. Protected deployments should use short-lived cloud credentials, least privilege, artifact retention controls, and explicit environment approvals.
