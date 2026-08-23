import pandas as pd


DATASET = "data/sample_revenue_events.csv"

AUTO_RECOVERY_LIMIT = 50000
MAX_RETRIES = 3


def expected_policy(row):
    if row["retry_count"] >= MAX_RETRIES:
        return "STOP"

    if row["amount"] > AUTO_RECOVERY_LIMIT:
        return "ESCALATE_TO_HUMAN"

    if (
        row["failure_reason"] == "temporary_gateway_failure"
        and row["gateway_status"] == "operational"
    ):
        return "RETRY_PAYMENT"

    if (
        row["failure_reason"] == "gateway_timeout"
        and row["gateway_status"] == "operational"
    ):
        return "RETRY_PAYMENT"

    if (
        row["failure_reason"] == "card_declined"
        and row["retry_count"] >= 2
    ):
        return "ESCALATE_TO_HUMAN"

    return "ESCALATE_TO_HUMAN"


def main():
    df = pd.read_csv(DATASET)

    errors = []

    for _, row in df.iterrows():
        expected = expected_policy(row)

        if row["expected_action"] != expected:
            errors.append(
                f"{row['transaction_id']}: "
                f"expected {expected}, "
                f"found {row['expected_action']}"
            )

    if errors:
        print("VALIDATION FAILED")

        for error in errors:
            print(error)

        raise SystemExit(1)

    print("VALIDATION PASSED")
    print(f"Checked {len(df)} records.")
    print("All expected actions match the policy.")


if __name__ == "__main__":
    main()