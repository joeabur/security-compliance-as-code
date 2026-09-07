# Architecture

The platform separates collection from evaluation. Collectors normalize AWS APIs, Terraform plan JSON, Checkov findings, and Prowler findings into a configuration snapshot. Pure checks evaluate that snapshot. YAML controls provide framework metadata and mapping references. The engine attaches evidence to every result, calculates framework scores, and renders reports.

The boundary is intentional: adding a collector or a framework does not require changing existing checks. Live AWS access should be an explicitly configured integration, never a test prerequisite.
