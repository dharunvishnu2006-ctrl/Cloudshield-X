from src.models import Alert
from src.logging_setup import get_logger

logger = get_logger("summarise")


def build_context(alerts: list[Alert]) -> dict:
    if not alerts:
        return {}

    ips = [a.ip for a in alerts]
    counts = [a.count for a in alerts]
    severities = [a.severity for a in alerts]
    reasons = [a.reason for a in alerts]

    context = {
        "ip_addresses": ips,
        "fail_counts": counts,
        "severities": severities,
        "reasons": reasons,
        "total_alerts": len(alerts),
        "highest_severity": max(
            severities, key=lambda s: ["low", "medium", "high", "critical"].index(s)
        ),
    }

    logger.info(f"Context built for {len(alerts)} alerts")
    return context


def build_prompt(context: dict) -> str:
    if not context:
        return ""

    prompt = f"""You are a security analyst assistant.
Summarise this incident in exactly 3 sentences.
Use ONLY the data provided. Do NOT invent any IP addresses,
counts or details not in the input.
Write "not available" for anything missing.
No speculation.

Data:
- IP addresses: {context['ip_addresses']}
- Fail counts: {context['fail_counts']}
- Severities: {context['severities']}
- Reasons: {context['reasons']}
- Total alerts: {context['total_alerts']}
- Highest severity: {context['highest_severity']}

3-sentence summary, then 1 recommended action:"""

    return prompt


def verify_summary(summary: str, context: dict) -> bool:
    if not context:
        return False

    for ip in context.get("ip_addresses", []):
        if ip not in summary:
            logger.warning(f"IP {ip} missing from summary!")
            return False

    for count in context.get("fail_counts", []):
        if str(count) not in summary:
            logger.warning(f"Count {count} missing!")
            return False

    return True


def summarise(alerts: list[Alert]) -> dict:
    if not alerts:
        return {
            "verified": False,
            "summary": "No alerts to summarise.",
            "raw_alerts": [],
        }

    context = build_context(alerts)
    prompt = build_prompt(context)

    logger.info(f"Prompt built: {len(prompt)} chars")

    try:
        import anthropic

        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        summary_text = message.content[0].text
        logger.info(f"LLM response: {summary_text[:100]}")

    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        summary_text = "not available"

    verified = verify_summary(summary_text, context)

    if not verified:
        logger.warning("Summary UNVERIFIED — showing raw alerts")

    return {
        "verified": verified,
        "summary": summary_text if verified else "UNVERIFIED",
        "raw_alerts": [
            {"ip": a.ip, "count": a.count, "severity": a.severity} for a in alerts
        ],
    }
