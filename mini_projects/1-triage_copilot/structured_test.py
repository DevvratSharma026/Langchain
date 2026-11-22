import time
from langchain_core.messages import HumanMessage, SystemMessage
from config import get_model
from schemas import Triage
from tickets import SAMPLE_TICKETS

SYSTEM_PROMPT = """You are an Oracle Integration Cloud (OIC) support engineer triaging incoming incident tickets from ticket text alone.

Classify each ticket accurately into a `Triage` object:
- Map clear failure clues to the matching category (`auth failure`, `stuck instance`, `data truncation`, `timeout`), use `no_error_found` when no errors are reported and behavior is unclear/healthy-looking, or `unknown` if the issue doesn't fit cleanly.
- Set `needs_alert` to True for serious issues (auth failures, stuck instances, data truncation/mapper errors, exhausted timeouts/retries) and False when no error is found or impact is minor/unclear.
- Provide concrete `next_steps` assigned to the right `owner` (`support`, `on-call`, `business user`, or `partner team`)."""


def format_ticket_prompt(ticket: dict) -> str:
    """Format a ticket dictionary consistently for model prompts."""
    return (
        f"Ticket ID: {ticket['id']}\n"
        f"Integration: {ticket['integration']}\n"
        f"Description: {ticket['text']}"
    )


def triage_structured(ticket: dict, structured_model=None, include_raw: bool = True):
    """Triage a single ticket into a validated `Triage` model."""
    model = structured_model or get_model().with_structured_output(
        Triage, include_raw=include_raw
    )
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=format_ticket_prompt(ticket)),
    ]
    return model.invoke(messages)


def run_all_tickets(sleep_seconds: float = 2.0) -> list[Triage]:
    """Run all sample tickets and print a summary table."""
    structured_model = get_model().with_structured_output(Triage)
    results: list[Triage] = []

    print(f"{'ID':<10} | {'Severity':<8} | {'Category':<16} | {'Needs Alert'}")
    print("-" * 56)

    for idx, ticket in enumerate(SAMPLE_TICKETS):
        triage: Triage = structured_model.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=format_ticket_prompt(ticket)),
            ]
        )
        results.append(triage)
        print(
            f"{triage.ticket_id:<10} | {triage.severity:<8} | "
            f"{triage.category:<16} | {str(triage.needs_alert)}"
        )

        if idx < len(SAMPLE_TICKETS) - 1 and sleep_seconds > 0:
            time.sleep(sleep_seconds)

    return results


if __name__ == "__main__":
    run_all_tickets(sleep_seconds=2.0)