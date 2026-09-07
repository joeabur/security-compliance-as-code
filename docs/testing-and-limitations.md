# Testing and Limitations

Fixtures cover compliant, partially compliant, and non-compliant environments. Unit tests exercise every executable check and report format. Terraform validation is part of CI.

The sample collector is offline and does not authenticate to AWS. Real deployments need authenticated collectors, asset discovery, control scoping, evidence retention, drift handling, false-positive review, and independent audit validation. The sample controls are illustrative and do not constitute a complete CIS, NIST, PCI DSS, or ISO 27001 implementation.
