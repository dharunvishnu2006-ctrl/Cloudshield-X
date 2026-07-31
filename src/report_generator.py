import pandas as pd


def generate_report(suspicious: dict, out="data/security_report.csv") -> str:
    """Write a CSV: columns = IP, Failed_Attempts, Risk."""
    rows = []
    for ip, count in suspicious.items():
        risk = "HIGH" if count >= 5 else "MEDIUM"
        rows.append((ip, count, risk))

    df = pd.DataFrame(rows, columns=["IP", "Failed_Attempts", "Risk"])
    df.to_csv(out, index=False)
    return out
