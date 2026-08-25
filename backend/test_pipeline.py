from recovery_pipeline import process_transaction


transaction = {
    "transaction_id": "TXN-PIPELINE-001",
    "amount": 12000,
    "failure_reason": "temporary_gateway_failure",
    "gateway_status": "operational",
    "retry_count": 0,
}


result = process_transaction(transaction)


print("Pipeline completed")
print()
print("Transaction:", result["transaction_id"])
print("Action:", result["action"])
print("Reason:", result["reason"])
print("Status:", result["status"])
print("Recovered amount:", result["recovered_amount"])
print("Timestamp:", result["timestamp"])