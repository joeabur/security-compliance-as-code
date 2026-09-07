# Control Model

Each YAML control contains control ID, framework, requirement, description, severity, executable check, recommendation, owner, remediation, references, and related mappings. Runtime results add status, evidence, and optional exception metadata.

Supported statuses are `PASS`, `FAIL`, `PARTIAL`, `NOT_APPLICABLE`, and `ERROR`. An unknown check is an `ERROR`, not a pass. A framework score counts only applicable controls and is a signal for prioritization, not an assurance statement.
