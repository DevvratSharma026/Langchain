from langchain.tools import tool

RUNBOOKS: dict[str, str] = {
    "auth failure": (
        "1. Verify credentials, OAuth client secret/certificate expiry, and security policy on the connection.\n"
        "2. Test the connection in OIC/integration console and re-save if needed.\n"
        "3. Re-run the failed job and confirm HTTP 200/201 responses."
    ),
    "stuck instance": (
        "1. Check if the payload/file size exceeds recommended batch/streaming limits.\n"
        "2. Inspect active threads/locks and abort or recover the hung instance safely if stalled.\n"
        "3. Split large files/batches or schedule off-peak runs, then re-trigger."
    ),
    "data truncation": (
        "1. Identify the source field length vs. target column/schema max length in the mapper.\n"
        "2. Coordinate with source/target owners to either truncate/trim safely or widen the target column.\n"
        "3. Re-process the failed record/batch and verify no data loss."
    ),
    "timeout": (
        "1. Check downstream endpoint health, latency, and network/firewall connectivity.\n"
        "2. Review connection/read timeout settings and retry policies.\n"
        "3. Re-run after the endpoint recovers or adjust timeout/batching thresholds."
    ),
}

INTEGRATION_STATUS: dict[str, dict[str, str | int]] = {
    "ERP_PO_SYNC": {
        "state": "DEGRADED",
        "last_success": "2026-11-20T08:15:00Z",
        "failures_24h": 14,
    },
    "HR_EMPLOYEE_FEED": {
        "state": "RUNNING",
        "last_success": "2026-11-21T02:10:00Z",
        "failures_24h": 1,
    },
    "INVOICE_TO_BANK": {
        "state": "ERROR",
        "last_success": "2026-11-22T04:30:00Z",
        "failures_24h": 6,
    },
    "CUSTOMER_SOAP_SYNC": {
        "state": "ERROR",
        "last_success": "2026-11-22T06:45:00Z",
        "failures_24h": 9,
    },
    "SHIPMENT_STATUS_PUSH": {
        "state": "HEALTHY",
        "last_success": "2026-11-22T05:50:00Z",
        "failures_24h": 0,
    },
}


@tool
def lookup_runbook(error_category: str) -> str:
    """Look up troubleshooting and fix steps for an integration error category.

    Valid error categories are:
    - auth failure
    - stuck instance
    - data truncation
    - timeout

    Args:
        error_category: One of the valid error category names (case-insensitive).

    Returns:
        Step-by-step remediation instructions, or a message stating no runbook was found.
    """
    normalized = error_category.strip().lower()
    if normalized not in RUNBOOKS:
        valid = ", ".join(RUNBOOKS.keys())
        return f"No runbook found for error category '{error_category}'. Valid categories: {valid}."
    return RUNBOOKS[normalized]


@tool
def get_integration_status(integration_name: str) -> str:
    """Fetch the current runtime state, last successful run timestamp, and 24-hour failure count for an integration.

    Args:
        integration_name: Exact integration identifier (e.g., ERP_PO_SYNC, HR_EMPLOYEE_FEED,
            INVOICE_TO_BANK, CUSTOMER_SOAP_SYNC, SHIPMENT_STATUS_PUSH).

    Returns:
        A formatted status summary for the integration, or 'unknown integration' if not found.
    """
    key = integration_name.strip().upper()
    status = INTEGRATION_STATUS.get(key)
    if status is None:
        return f"unknown integration: '{integration_name}'"

    return (
        f"Integration: {key} | "
        f"State: {status['state']} | "
        f"Last Success: {status['last_success']} | "
        f"Failures (last 24h): {status['failures_24h']}"
    )


@tool
def send_alert_email(recipient: str, subject: str, body: str) -> str:
    """Send an alert email notification to an on-call recipient or team distribution list.

    Args:
        recipient: Email address or distribution list to notify.
        subject: Concise alert subject line including ticket ID or integration name.
        body: Alert details including symptoms, status, and recommended next steps.

    Returns:
        Confirmation string indicating the alert email was sent.
    """
    print(f"[MOCK EMAIL] To: {recipient} | Subject: {subject}\n{body}\n")
    return f"sent alert email to {recipient} with subject '{subject}'"