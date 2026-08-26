from diagnosis_validator import validate_diagnosis


bad_diagnosis = {
    "diagnosis": "Retry immediately.",
    "risk": "EXTREME",
    "failure_reason": "temporary_gateway_failure",
    "gateway_status": "operational",
    "retry_count": 1,
    "amount": 12000,
}


try:
    validate_diagnosis(bad_diagnosis)
    print("TEST FAILED: invalid diagnosis was accepted.")

except ValueError as error:
    print("INVALID DIAGNOSIS REJECTED")
    print("Reason:", error)