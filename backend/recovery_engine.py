AUTO_RECOVERY_LIMIT = 50000
MAX_RETRIES = 3


def decide_recovery(transaction):
    """
    Decide the safest recovery action for a failed payment.
    Returns:
        action: recovery action
        reason: explanation for the decision
    """

    amount = transaction["amount"]
    failure_reason = transaction["failure_reason"]
    gateway_status = transaction["gateway_status"]
    retry_count = transaction["retry_count"]

    # Rule 1: Stop after the maximum number of retries.
    if retry_count >= MAX_RETRIES:
        return (
            "STOP",
            "Maximum retry limit has been reached."
        )

    # Rule 2: High-value transactions require human review.
    if amount > AUTO_RECOVERY_LIMIT:
        return (
            "ESCALATE_TO_HUMAN",
            "Transaction exceeds the automatic recovery limit."
        )

    # Rule 3: Temporary gateway failure.
    if (
        failure_reason == "temporary_gateway_failure"
        and gateway_status == "operational"
    ):
        return (
            "RETRY_PAYMENT",
            "Temporary gateway failure with an operational gateway."
        )

    # Rule 4: Gateway timeout.
    if (
        failure_reason == "gateway_timeout"
        and gateway_status == "operational"
    ):
        return (
            "RETRY_PAYMENT",
            "Gateway timeout may be recoverable with another attempt."
        )

    # Rule 5: Repeated card decline.
    if (
        failure_reason == "card_declined"
        and retry_count >= 2
    ):
        return (
            "ESCALATE_TO_HUMAN",
            "Repeated card decline requires human review."
        )

    # Rule 6: Safe fallback.
    return (
        "ESCALATE_TO_HUMAN",
        "Automatic recovery is not justified for this failure."
    )