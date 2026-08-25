import csv
from pathlib import Path

from audit import record_audit


AUDIT_FILE = Path("data/recovery_audit.csv")


transaction = {
    "transaction_id": "TXN-AUDIT-001",
}

result = {
    "status": "SUCCESS",
    "recovered_amount": 12000,
    "timestamp": "2026-08-26T04:00:00",
}

record_audit(
    transaction,
    "RETRY_PAYMENT",
    "Temporary gateway failure with an operational gateway.",
    result,
)


with AUDIT_FILE.open("r", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))


assert len(rows) == 1
assert rows[0]["transaction_id"] == "TXN-AUDIT-001"
assert rows[0]["action"] == "RETRY_PAYMENT"
assert rows[0]["status"] == "SUCCESS"
assert int(rows[0]["recovered_amount"]) == 12000

print("AUDIT VALIDATION PASSED")