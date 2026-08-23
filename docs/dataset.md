# ReviveAI Dataset and Recovery Policy v1

## Purpose

The dataset represents synthetic failed-payment events that ReviveAI will process for revenue recovery.

One record represents one failed payment event.

The dataset is synthetic and does not represent real merchant or customer data.

The dataset will be used for development, recovery simulation, and batch evaluation.

## Dataset Fields

### Identifiers

transaction_id

Unique identifier for the payment event.

customer_id

Unique identifier for the customer associated with the payment.

### Transaction Information

amount

Transaction amount in INR.

currency

Currency of the transaction. The initial dataset uses INR.

timestamp

Time at which the payment failure occurred.

### Payment Information

payment_method

Allowed values:

* credit_card
* debit_card
* upi
* net_banking

payment_status

The initial dataset contains failed payments, so the value is failed.

failure_reason

Allowed values:

* temporary_gateway_failure
* gateway_timeout
* card_declined
* insufficient_funds
* expired_card
* invalid_payment_method

gateway_status

Allowed values:

* operational
* degraded
* down

### Customer Context

previous_failures

Number of previous failed payments associated with the customer.

previous_successes

Number of previous successful payments associated with the customer.

customer_tenure_days

Number of days since the customer started using the service.

### Recovery Context

retry_count

Number of automated recovery retries already attempted for the transaction.

### Ground Truth and Outcome

recoverable

Whether the transaction is considered eligible for recovery according to the dataset policy.

expected_action

The recovery action that the policy considers appropriate.

Allowed values:

* RETRY_PAYMENT
* SEND_REMINDER
* OFFER_GRACE_PERIOD
* ESCALATE_TO_HUMAN
* STOP

actual_recovery

Whether the simulated recovery ultimately recovered the payment.

recovered_amount

The amount actually recovered by the simulator.

These fields are used for evaluation and must not be provided to the recovery decision logic before it makes its decision.

## Recovery Policy v1

The initial policy is designed for the synthetic MVP environment.

The policy parameters are configurable and are not intended to represent universal production financial rules.

### Policy Parameters

AUTO_RECOVERY_LIMIT = 50000 INR

MAX_RETRIES = 3

### Rule Priority

Rules are evaluated in the following order:

1. Stopping conditions
2. High-value restrictions
3. Failure-specific recovery rules
4. Safe fallback

### Rule 1: Retry Limit

If retry_count is greater than or equal to MAX_RETRIES:

Action:

STOP

Reason:

The maximum number of automated recovery attempts has been reached.

### Rule 2: High-Value Transaction

If amount is greater than AUTO_RECOVERY_LIMIT:

Action:

ESCALATE_TO_HUMAN

Reason:

High-value transactions require additional review in the MVP policy.

This rule does not mean that transactions above this amount are impossible to recover. It means that the MVP does not automatically recover them.

### Rule 3: Temporary Gateway Failure

If:

* failure_reason is temporary_gateway_failure
* gateway_status is operational
* retry_count is less than MAX_RETRIES
* amount is less than or equal to AUTO_RECOVERY_LIMIT

Action:

RETRY_PAYMENT

Reason:

The failure appears temporary, the gateway is operational, and the transaction is within the automatic recovery limit.

### Rule 4: Gateway Timeout

If:

* failure_reason is gateway_timeout
* gateway_status is operational
* retry_count is less than MAX_RETRIES
* amount is less than or equal to AUTO_RECOVERY_LIMIT

Action:

RETRY_PAYMENT

Reason:

The timeout may be temporary and another controlled attempt may succeed.

### Rule 5: Repeated Card Decline

If:

* failure_reason is card_declined
* retry_count is greater than or equal to 2

Action:

ESCALATE_TO_HUMAN

Reason:

Repeated card declines should not be retried indefinitely.

### Rule 6: Other Payment Failures

For failures where automatic recovery is not clearly justified:

Action:

ESCALATE_TO_HUMAN

Reason:

The system does not have sufficient justification for automatic recovery.

## Policy Examples

### Example 1

Amount: 12000 INR

Failure: temporary_gateway_failure

Gateway: operational

Retry count: 0

Expected action:

RETRY_PAYMENT

### Example 2

Amount: 12000 INR

Failure: temporary_gateway_failure

Gateway: operational

Retry count: 3

Expected action:

STOP

### Example 3

Amount: 80000 INR

Failure: temporary_gateway_failure

Gateway: operational

Retry count: 0

Expected action:

ESCALATE_TO_HUMAN

### Example 4

Amount: 8000 INR

Failure: card_declined

Gateway: operational

Retry count: 2

Expected action:

ESCALATE_TO_HUMAN

## Ground Truth

Ground truth is generated using deterministic policy rules.

The LLM is not used to create the ground truth.

The purpose of ground truth is to provide a reference against which ReviveAI decisions can be evaluated.

The recovery system should receive the transaction context but should not receive expected_action, recoverable, actual_recovery, or recovered_amount while making its decision.

## Synthetic Data Generation

The dataset will be generated using Python.

A fixed random seed will be used so that the dataset can be reproduced.

The initial development process will generate a small sample first.

The sample will be inspected for:

* Valid field values
* Realistic transaction amounts
* Reasonable failure distributions
* Correct ground truth
* Correct policy behavior
* Useful edge cases

After validation, the generator will be used to create the larger evaluation dataset.

## Important Limitations

This policy is an MVP policy for a synthetic environment.

The AUTO_RECOVERY_LIMIT and MAX_RETRIES values are configurable assumptions.

A production system would require merchant-specific policies, historical data, risk controls, compliance review, payment-provider requirements, and monitoring before automatic financial actions could be enabled.

The simulator does not execute real financial transactions.
