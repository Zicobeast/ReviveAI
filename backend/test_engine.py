from recovery_engine import decide_recovery


test_cases = [
    {
        "name": "Normal temporary failure",
        "transaction": {
            "amount": 12000,
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "retry_count": 0,
        },
        "expected": "RETRY_PAYMENT",
    },
    {
        "name": "Retry limit reached",
        "transaction": {
            "amount": 12000,
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "retry_count": 3,
        },
        "expected": "STOP",
    },
    {
        "name": "High value transaction",
        "transaction": {
            "amount": 80000,
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "retry_count": 0,
        },
        "expected": "ESCALATE_TO_HUMAN",
    },
    {
        "name": "Repeated card decline",
        "transaction": {
            "amount": 8000,
            "failure_reason": "card_declined",
            "gateway_status": "operational",
            "retry_count": 2,
        },
        "expected": "ESCALATE_TO_HUMAN",
    },
    {
        "name": "High value with retry limit",
        "transaction": {
            "amount": 80000,
            "failure_reason": "temporary_gateway_failure",
            "gateway_status": "operational",
            "retry_count": 3,
        },
        "expected": "STOP",
    },
]


for test in test_cases:
    action, reason = decide_recovery(test["transaction"])

    result = "PASS" if action == test["expected"] else "FAIL"

    print(f"{result}: {test['name']}")
    print(f"  Expected: {test['expected']}")
    print(f"  Actual:   {action}")
    print(f"  Reason:   {reason}")
    print()