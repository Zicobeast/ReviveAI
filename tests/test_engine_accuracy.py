import pandas as pd

from backend.recovery_engine import decide_recovery


DATASET = "data/revenue_events.csv"


def main():
    df = pd.read_csv(DATASET)

    correct = 0
    total = len(df)

    mismatches = []

    for _, row in df.iterrows():

        transaction = {
            "amount": row["amount"],
            "failure_reason": row["failure_reason"],
            "gateway_status": row["gateway_status"],
            "retry_count": row["retry_count"],
        }

        predicted_action, reason = decide_recovery(transaction)

        expected_action = row["expected_action"]

        if predicted_action == expected_action:
            correct += 1
        else:
            mismatches.append(
                {
                    "transaction_id": row["transaction_id"],
                    "expected": expected_action,
                    "predicted": predicted_action,
                    "reason": reason,
                }
            )

    accuracy = (correct / total) * 100

    print(f"Total transactions: {total}")
    print(f"Correct decisions: {correct}")
    print(f"Incorrect decisions: {len(mismatches)}")
    print(f"Decision accuracy: {accuracy:.2f}%")

    if mismatches:
        print("\nFirst mismatches:")

        for mismatch in mismatches[:10]:
            print(mismatch)
    else:
        print("\nAll decisions match the ground truth.")


if __name__ == "__main__":
    main()