import csv
import pandas as pd

from .recovery_pipeline import process_transaction


DATASET = "data/revenue_events.csv"
AUDIT_FILE = "data/recovery_audit.csv"


def reset_audit_log():
    """Create a fresh audit log for this batch run."""

    with open(AUDIT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "transaction_id",
            "action",
            "reason",
            "status",
            "recovered_amount",
            "timestamp",
        ])


def main():
    reset_audit_log()

    df = pd.read_csv(DATASET)

    results = []

    for _, row in df.iterrows():
        transaction = row.to_dict()

        result = process_transaction(transaction)

        results.append(result)

    results_df = pd.DataFrame(results)

    audit_df = pd.read_csv(AUDIT_FILE)

    print("BATCH PROCESSING COMPLETED")
    print()
    print("Transactions processed:", len(results_df))
    print("Audit records:", len(audit_df))
    print()

    print("Workflow outcomes:")
    print(
        "SUCCESS:",
        (results_df["status"] == "SUCCESS").sum(),
    )
    print(
        "ESCALATED:",
        (results_df["status"] == "ESCALATED").sum(),
    )
    print(
        "STOPPED:",
        (results_df["status"] == "STOPPED").sum(),
    )
    print(
        "FAILED:",
        (results_df["status"] == "FAILED").sum(),
    )

    print()

    recovered_revenue = results_df["recovered_amount"].sum()

    print("Recovered revenue: ₹", recovered_revenue)

    if len(audit_df) == len(results_df):
        print("AUDIT VALIDATION PASSED")
    else:
        print("AUDIT VALIDATION FAILED")


if __name__ == "__main__":
    main()