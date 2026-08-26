import random
from datetime import datetime

RNG = random.Random(42)


def execute_recovery(transaction, action):
    """
    Execute a simulated recovery action.
    """

    timestamp = datetime.now().isoformat()

    if action == "RETRY_PAYMENT":
        failure_reason = transaction["failure_reason"]

        if failure_reason == "temporary_gateway_failure":
            success_probability = 0.80
        elif failure_reason == "gateway_timeout":
            success_probability = 0.70
        else:
            success_probability = 0.50

        success = RNG.random() < success_probability

        if success:
            return {
                "status": "SUCCESS",
                "recovered_amount": transaction["amount"],
                "timestamp": timestamp,
                "message": "Simulated payment retry succeeded.",
            }

        return {
            "status": "FAILED",
            "recovered_amount": 0,
            "timestamp": timestamp,
            "message": "Simulated payment retry failed.",
        }

    if action == "ESCALATE_TO_HUMAN":
        return {
            "status": "ESCALATED",
            "recovered_amount": 0,
            "timestamp": timestamp,
            "message": "Transaction escalated for human review.",
        }

    if action == "STOP":
        return {
            "status": "STOPPED",
            "recovered_amount": 0,
            "timestamp": timestamp,
            "message": "Recovery workflow stopped by policy.",
        }

    return {
        "status": "REJECTED",
        "recovered_amount": 0,
        "timestamp": timestamp,
        "message": "Unknown recovery action.",
    }