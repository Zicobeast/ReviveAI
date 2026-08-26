from ai_diagnosis import diagnose_transaction


transaction = {
    "transaction_id": "TXN-AI-001",
    "amount": 12000,
    "failure_reason": "temporary_gateway_failure",
    "gateway_status": "operational",
    "retry_count": 1,
}


diagnosis = diagnose_transaction(transaction)


print("AI Diagnosis")
print("------------")
print("Diagnosis:", diagnosis["diagnosis"])
print("Risk:", diagnosis["risk"])
print("Failure reason:", diagnosis["failure_reason"])