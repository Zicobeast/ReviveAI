import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


SEED = 42
SAMPLE_SIZE = 20

AUTO_RECOVERY_LIMIT = 50000
MAX_RETRIES = 3

OUTPUT_FILE = Path(__file__).parent / "sample_revenue_events.csv"


FAILURE_REASONS = [
    "temporary_gateway_failure",
    "gateway_timeout",
    "card_declined",
    "insufficient_funds",
    "expired_card",
    "invalid_payment_method",
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "upi",
    "net_banking",
]

GATEWAY_STATUSES = [
    "operational",
    "degraded",
    "down",
]


def determine_ground_truth(record):
    """
    Apply the deterministic recovery policy.

    This function creates the ground truth.
    The AI will NOT be used here.
    """

    amount = record["amount"]
    failure_reason = record["failure_reason"]
    gateway_status = record["gateway_status"]
    retry_count = record["retry_count"]

    # Rule 1: Stop when retry limit is reached.
    if retry_count >= MAX_RETRIES:
        return False, "STOP"

    # Rule 2: High-value transactions require human review.
    if amount > AUTO_RECOVERY_LIMIT:
        return False, "ESCALATE_TO_HUMAN"

    # Rule 3: Temporary gateway failures can be retried.
    if (
        failure_reason == "temporary_gateway_failure"
        and gateway_status == "operational"
    ):
        return True, "RETRY_PAYMENT"

    # Rule 4: Gateway timeouts can be retried.
    if (
        failure_reason == "gateway_timeout"
        and gateway_status == "operational"
    ):
        return True, "RETRY_PAYMENT"

    # Rule 5: Repeated card declines require human review.
    if (
        failure_reason == "card_declined"
        and retry_count >= 2
    ):
        return False, "ESCALATE_TO_HUMAN"

    # Rule 6: Safe fallback.
    return False, "ESCALATE_TO_HUMAN"


def simulate_recovery(record, expected_action, rng):
    """
    Simulate the outcome of the recovery action.

    This is only a prototype simulation.
    No real payment is processed.
    """

    if expected_action != "RETRY_PAYMENT":
        return False, 0

    success_probability = {
        "temporary_gateway_failure": 0.80,
        "gateway_timeout": 0.70,
    }.get(record["failure_reason"], 0.20)

    recovered = rng.random() < success_probability

    if recovered:
        return True, record["amount"]

    return False, 0

def create_policy_cases(start_time, rng):
    cases = [
        {
            "transaction_id": "TXN-POLICY-001",
            "customer_id": "CUST-POLICY-001",
            "amount": 12000,
            "currency": "INR",
            "payment_method": "upi",
            "payment_status": "failed",
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "previous_failures": 0,
            "previous_successes": 5,
            "customer_tenure_days": 300,
            "retry_count": 0,
            "timestamp": start_time.isoformat(),
        },
        {
            "transaction_id": "TXN-POLICY-002",
            "customer_id": "CUST-POLICY-002",
            "amount": 12000,
            "currency": "INR",
            "payment_method": "credit_card",
            "payment_status": "failed",
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "previous_failures": 1,
            "previous_successes": 8,
            "customer_tenure_days": 500,
            "retry_count": 3,
            "timestamp": (start_time + timedelta(minutes=1)).isoformat(),
        },
        {
            "transaction_id": "TXN-POLICY-003",
            "customer_id": "CUST-POLICY-003",
            "amount": 80000,
            "currency": "INR",
            "payment_method": "net_banking",
            "payment_status": "failed",
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "previous_failures": 0,
            "previous_successes": 10,
            "customer_tenure_days": 700,
            "retry_count": 0,
            "timestamp": (start_time + timedelta(minutes=2)).isoformat(),
        },
        {
            "transaction_id": "TXN-POLICY-004",
            "customer_id": "CUST-POLICY-004",
            "amount": 8000,
            "currency": "INR",
            "payment_method": "credit_card",
            "payment_status": "failed",
            "failure_reason": "card_declined",
            "gateway_status": "operational",
            "previous_failures": 2,
            "previous_successes": 4,
            "customer_tenure_days": 200,
            "retry_count": 2,
            "timestamp": (start_time + timedelta(minutes=3)).isoformat(),
        },
        {
            "transaction_id": "TXN-POLICY-005",
            "customer_id": "CUST-POLICY-005",
            "amount": 80000,
            "currency": "INR",
            "payment_method": "upi",
            "payment_status": "failed",
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "previous_failures": 3,
            "previous_successes": 6,
            "customer_tenure_days": 900,
            "retry_count": 3,
            "timestamp": (start_time + timedelta(minutes=4)).isoformat(),
        },
    ]

    for case in cases:
        recoverable, expected_action = determine_ground_truth(case)

        actual_recovery, recovered_amount = simulate_recovery(
            case,
            expected_action,
            rng,
        )

        case["recoverable"] = recoverable
        case["expected_action"] = expected_action
        case["actual_recovery"] = actual_recovery
        case["recovered_amount"] = recovered_amount

    return cases


def generate_record(index, rng, start_time):
    amount = round(
        rng.choices(
            population=[500, 2500, 7500, 15000, 30000, 75000, 150000],
            weights=[20, 25, 20, 15, 10, 7, 3],
            k=1,
        )[0],
        2,
    )

    failure_reason = rng.choice(FAILURE_REASONS)
    payment_method = rng.choice(PAYMENT_METHODS)
    gateway_status = rng.choice(GATEWAY_STATUSES)

    retry_count = rng.randint(0, 5)
    previous_failures = rng.randint(0, 5)
    previous_successes = rng.randint(0, 20)
    customer_tenure_days = rng.randint(1, 2000)

    timestamp = start_time + timedelta(
        minutes=rng.randint(0, 60 * 24 * 30)
    )

    record = {
        "transaction_id": f"TXN-{index:05d}",
        "customer_id": f"CUST-{rng.randint(1, 500):04d}",
        "amount": amount,
        "currency": "INR",
        "payment_method": payment_method,
        "payment_status": "failed",
        "failure_reason": failure_reason,
        "gateway_status": gateway_status,
        "previous_failures": previous_failures,
        "previous_successes": previous_successes,
        "customer_tenure_days": customer_tenure_days,
        "retry_count": retry_count,
        "timestamp": timestamp.isoformat(),
    }

    recoverable, expected_action = determine_ground_truth(record)

    actual_recovery, recovered_amount = simulate_recovery(
        record,
        expected_action,
        rng,
    )

    record["recoverable"] = recoverable
    record["expected_action"] = expected_action
    record["actual_recovery"] = actual_recovery
    record["recovered_amount"] = recovered_amount

    return record


def main():
    rng = random.Random(SEED)

    start_time = datetime(2026, 1, 1, 0, 0, 0)

    fieldnames = [
        "transaction_id",
        "customer_id",
        "amount",
        "currency",
        "payment_method",
        "payment_status",
        "failure_reason",
        "gateway_status",
        "previous_failures",
        "previous_successes",
        "customer_tenure_days",
        "retry_count",
        "timestamp",
        "recoverable",
        "expected_action",
        "actual_recovery",
        "recovered_amount",
    ]

    policy_cases = create_policy_cases(start_time,rng)

    random_cases = [
        generate_record(i, rng, start_time)
        for i in range(1, SAMPLE_SIZE - len(policy_cases) + 1)
    ]

    records = policy_cases + random_cases

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()