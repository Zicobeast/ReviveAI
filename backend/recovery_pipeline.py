from recovery_engine import decide_recovery
from recovery_workflow import execute_recovery
from audit import record_audit


def process_transaction(transaction):
    """
    Process one failed transaction through the complete
    recovery decision and execution pipeline.
    """

    action, reason = decide_recovery(transaction)

    result = execute_recovery(
        transaction,
        action,
    )

    record_audit(
        transaction,
        action,
        reason,
        result,
    )

    return {
        "transaction_id": transaction["transaction_id"],
        "action": action,
        "reason": reason,
        "status": result["status"],
        "recovered_amount": result["recovered_amount"],
        "timestamp": result["timestamp"],
    }