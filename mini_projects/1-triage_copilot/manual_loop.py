from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from config import get_model
from tickets import SAMPLE_TICKETS
from tools import get_integration_status, lookup_runbook, send_alert_email

MAX_ITERATIONS = 5

SYSTEM_PROMPT = """You are an Oracle Integration Cloud (OIC) support engineer triaging incoming incident tickets.

When investigating a ticket:
1. Always check the integration's current status using `get_integration_status`.
2. Look up remediation steps using `lookup_runbook` ONLY if the ticket points to one of these exact error categories: `auth failure`, `stuck instance`, `data truncation`, `timeout`. If none of those categories fit, do not guess a category.
3. Call `send_alert_email` to `oncall@example.com` ONLY when the issue is confirmed serious—such as an active outage/error state, authentication failure, stuck instance, exhausted retries/timeouts, or repeated failures. If the integration status is HEALTHY with 0 failures and there are no errors in monitoring, DO NOT send an alert email; instead suggest checking upstream/downstream producers, dashboards, or schedules.

Once you have enough information, provide a clear, concise triage summary and recommended action plan."""

TOOLS = [lookup_runbook, get_integration_status, send_alert_email]
TOOL_MAP = {t.name: t for t in TOOLS}
MODEL_WITH_TOOLS = get_model().bind_tools(TOOLS)


def triage_ticket(ticket: dict) -> AIMessage | None:
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    human_message = HumanMessage(
        content=(
            f"Ticket ID: {ticket['id']}\n"
            f"Integration: {ticket['integration']}\n"
            f"Description: {ticket['text']}"
        )
    )

    messages: list = [system_message, human_message]

    print(f"\n=== Triaging {ticket['id']} ({ticket['integration']}) ===")

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Step {step} ---")
        ai_message = MODEL_WITH_TOOLS.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            print("Final Answer:")
            print(ai_message.text)
            return ai_message

        for tool_call in ai_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]
            print(f"Calling tool: {tool_name} | Args: {tool_args}")

            selected_tool = TOOL_MAP.get(tool_name)
            if selected_tool is None:
                tool_result = ToolMessage(
                    content=f"Error: unknown tool '{tool_name}'. Available tools: {', '.join(TOOL_MAP.keys())}",
                    tool_call_id=tool_call_id,
                )
            else:
                tool_result = selected_tool.invoke(tool_call)

            content = tool_result.content if hasattr(tool_result, "content") else tool_result
            print(f"Tool result ({tool_name}): {content}")
            messages.append(tool_result)

    print(f"Reached max iterations ({MAX_ITERATIONS}) without a final response.")
    return None


if __name__ == "__main__":
    for sample_ticket in SAMPLE_TICKETS:
        triage_ticket(sample_ticket)