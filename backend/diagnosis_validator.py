ALLOWED_RISKS = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


def validate_diagnosis(diagnosis):
    """
    Validate the structure and allowed values of an AI diagnosis.
    """

    required_fields = {
        "diagnosis",
        "risk",
        "failure_reason",
        "gateway_status",
        "retry_count",
        "amount",
    }

    missing_fields = required_fields - diagnosis.keys()

    if missing_fields:
        raise ValueError(
            f"Missing diagnosis fields: {missing_fields}"
        )

    if diagnosis["risk"] not in ALLOWED_RISKS:
        raise ValueError(
            f"Invalid risk level: {diagnosis['risk']}"
        )

    if not isinstance(diagnosis["retry_count"], int):
        raise ValueError(
            "retry_count must be an integer."
        )

    if diagnosis["amount"] < 0:
        raise ValueError(
            "amount cannot be negative."
        )

    return True