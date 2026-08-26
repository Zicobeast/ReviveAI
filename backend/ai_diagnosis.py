def diagnose_transaction(transaction):
    """
    Analyze a failed transaction and return a structured diagnosis.
    """

    failure_reason = transaction["failure_reason"]
    gateway_status = transaction["gateway_status"]
    retry_count = transaction["retry_count"]
    amount = transaction["amount"]

    if failure_reason == "temporary_gateway_failure":
        diagnosis = "Likely transient gateway issue."
        risk = "LOW"

    elif failure_reason == "gateway_timeout":
        diagnosis = "Payment gateway timed out and may recover on retry."
        risk = "MEDIUM"

    elif failure_reason == "card_declined":
        diagnosis = "Payment method was declined."
        risk = "MEDIUM"

    elif failure_reason == "insufficient_funds":
        diagnosis = "Customer may not have sufficient funds."
        risk = "HIGH"

    elif failure_reason == "expired_card":
        diagnosis = "Customer payment method appears to be expired."
        risk = "HIGH"

    else:
        diagnosis = "Failure reason requires further investigation."
        risk = "HIGH"

    return {
        "diagnosis": diagnosis,
        "risk": risk,
        "failure_reason": failure_reason,
        "gateway_status": gateway_status,
        "retry_count": retry_count,
        "amount": amount,
    }