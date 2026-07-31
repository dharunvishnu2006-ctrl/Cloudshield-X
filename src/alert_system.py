def raise_alerts(suspicious: dict) -> list:
    """Print a warning per suspicious IP; return the messages."""
    if not suspicious:
        print("All clear")
        return []
    messages = []
    for ip, count in suspicious.items():
        msg = f"ALERT: {ip} had {count} failed logins"
        print(msg)
        messages.append(msg)
    return messages
