SAMPLE_TICKETS = [
    {
        "id": "TKT-1001",
        "integration": "ERP_PO_SYNC",
        "text": (
            "HTTP 401 Unauthorized calling the ERP Cloud purchaseOrders REST resource. "
            "Connection ERP_PROD_CONN security policy failed. Last successful run 2 days ago."
        ),
    },
    {
        "id": "TKT-1002",
        "integration": "HR_EMPLOYEE_FEED",
        "text": (
            "Scheduled integration stuck in RUNNING for 6 hours (expected 10 min). "
            "FTP adapter reading employees_20261120.csv (480 MB)."
        ),
    },
    {
        "id": "TKT-1003",
        "integration": "INVOICE_TO_BANK",
        "text": (
            "ORA-12899: value too large for column REFERENCE_NO (actual 42, max 30). "
            "Mapper failed on invoice INV-77821."
        ),
    },
    {
        "id": "TKT-1004",
        "integration": "CUSTOMER_SOAP_SYNC",
        "text": (
            "Connection timeout after 60000 ms invoking partner SOAP endpoint "
            "CustomerService. Retries exhausted (3/3)."
        ),
    },
    {
        "id": "TKT-1005",
        "integration": "SHIPMENT_STATUS_PUSH",
        "text": (
            "Business user says shipments haven't updated on the dashboard since morning. "
            "No errors visible in OIC monitoring."
        ),
    },
]