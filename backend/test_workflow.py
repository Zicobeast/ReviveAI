from recovery_workflow import execute_recovery


transaction = {
    "transaction_id": "TXN-TEST-001",
    "amount": 12000,
    "failure_reason": "temporary_gateway_failure",
}


test_actions = [
    "RETRY_PAYMENT",
    "ESCALATE_TO_HUMAN",
    "STOP",
]


for action in test_actions:
    result = execute_recovery(transaction, action)

    print(f"Action: {action}")
    print(f"Status: {result['status']}")
    print(f"Recovered amount: {result['recovered_amount']}")
    print(f"Message: {result['message']}")
    print()