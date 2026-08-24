from datetime import datetime


def execute_recovery(transaction, action):
    """
    Execute a simulated recovery action.

    No real payment is processed.
    """

    timestamp = datetime.now().isoformat()

    if action == "RETRY_PAYMENT":
        return {
            "status": "SUCCESS",
            "recovered_amount": transaction["amount"],
            "timestamp": timestamp,
            "message": "Simulated payment retry succeeded.",
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