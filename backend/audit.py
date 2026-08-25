import csv
from pathlib import Path


AUDIT_FILE = Path("data/recovery_audit.csv")


def record_audit(transaction, action, reason, result):
    """
    Record a recovery decision and its outcome.
    """

    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = AUDIT_FILE.exists()

    with AUDIT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "transaction_id",
                "action",
                "reason",
                "status",
                "recovered_amount",
                "timestamp",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "transaction_id": transaction["transaction_id"],
                "action": action,
                "reason": reason,
                "status": result["status"],
                "recovered_amount": result["recovered_amount"],
                "timestamp": result["timestamp"],
            }
        )