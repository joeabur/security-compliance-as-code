"""Pure checks over normalized AWS/Terraform configuration snapshots."""

from __future__ import annotations

from typing import Any


def _check(value: bool, passed: str, failed: str) -> tuple[bool, str]:
    return value, passed if value else failed


def check_mfa(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("iam", {}).get("root_mfa_enabled")),
        "Root MFA is enabled",
        "MFA not detected for root account",
    )


def check_root_activity(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        not config.get("iam", {}).get("root_activity", False),
        "No root account activity detected",
        "Root account activity was detected",
    )


def check_iam_wildcards(config: dict[str, Any]) -> tuple[bool, str]:
    wildcard_count = config.get("iam", {}).get("wildcard_policies", 0)
    return _check(
        wildcard_count == 0,
        "No IAM wildcard permissions detected",
        f"{wildcard_count} IAM wildcard permission policies detected",
    )


def check_s3_public_access(config: dict[str, Any]) -> tuple[bool, str]:
    public_buckets = config.get("s3", {}).get("public_buckets", [])
    return _check(
        not public_buckets,
        "All S3 buckets deny public access",
        f"Public S3 buckets detected: {', '.join(public_buckets)}",
    )


def check_encryption(config: dict[str, Any]) -> tuple[bool, str]:
    unencrypted = config.get("storage", {}).get("unencrypted_resources", [])
    return _check(
        not unencrypted,
        "Storage encryption is enabled",
        f"Unencrypted resources detected: {', '.join(unencrypted)}",
    )


def check_cloudtrail(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("logging", {}).get("cloudtrail_enabled")),
        "CloudTrail is enabled",
        "CloudTrail is not enabled",
    )


def check_logging(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("logging", {}).get("centralized_logging")),
        "Centralized logging is configured",
        "Centralized logging is not configured",
    )


def check_security_group_exposure(config: dict[str, Any]) -> tuple[bool, str]:
    exposed = config.get("network", {}).get("publicly_exposed_ports", [])
    return _check(
        not exposed,
        "No unrestricted security group ingress detected",
        f"Unrestricted ingress detected on ports: {exposed}",
    )


def check_password_policy(config: dict[str, Any]) -> tuple[bool, str]:
    policy = config.get("iam", {}).get("password_policy", {})
    valid = policy.get("minimum_length", 0) >= 14 and policy.get("require_symbols", False)
    return _check(
        valid, "IAM password policy meets baseline", "IAM password policy does not meet baseline"
    )


def check_key_management(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("storage", {}).get("customer_managed_keys")),
        "Customer-managed key controls are present",
        "Customer-managed key controls are not present",
    )


def check_backup(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("resilience", {}).get("backup_enabled")),
        "Backups are enabled",
        "Backups are not enabled",
    )


def check_monitoring(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("monitoring", {}).get("alerts_enabled")),
        "Security monitoring alerts are enabled",
        "Security monitoring alerts are not enabled",
    )


def check_vulnerability_management(config: dict[str, Any]) -> tuple[bool, str]:
    return _check(
        bool(config.get("vulnerability_management", {}).get("scanning_enabled")),
        "Vulnerability scanning is enabled",
        "Vulnerability scanning is not enabled",
    )


CHECKS = {
    name.removeprefix("check_"): value
    for name, value in globals().items()
    if name.startswith("check_")
}
