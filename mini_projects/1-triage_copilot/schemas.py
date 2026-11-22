from typing import Literal
from pydantic import BaseModel, Field

StepOwner = Literal["support", "on-call", "business user", "partner team"]
SeverityLevel = Literal["low", "medium", "high", "critical"]
ErrorCategory = Literal[
    "auth failure",
    "stuck instance",
    "data truncation",
    "timeout", 
    "no_error_found",
    "unknown"
]

class NextStep(BaseModel):
    owner: StepOwner = Field(
        description="Who should perform this step: 'support', 'on-call', 'business user', 'partner team'"
    )
    action: str = Field(
        description='Concrete, actionable remediation or investigation step to take.'
    )

class Triage(BaseModel):
    ticket_id: str = Field(
        description="Identifier of the ticket being triaged (e.g., 'TKT-1001')."
    )
    integration: str = Field(
        description="Name of the affected integration (e.g., 'ERP_PO_SYNC')."
    )
    severity: SeverityLevel = Field(
        description="Overall incident severity: 'low', 'medium', 'high', or 'critical'."
    )
    category: ErrorCategory = Field(
        description=(
            "Classified error category: 'auth failure', 'stuck instance', "
            "'data truncation', 'timeout', 'no_error_found', or 'unknown'."
        )
    )
    suspected_cause: str = Field(
        description="Concise explanation of the most likely root cause based on the ticket text."
    )
    needs_alert: bool = Field(
        description="True if on-call escalation/alerting is warranted due to severity or impact, otherwise False."
    )
    next_steps: list[NextStep] = Field(
        description="Ordered list of concrete next steps with assigned owners."
    )