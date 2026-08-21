# ReviveAI — Product Requirements

## 1. Product Overview

ReviveAI is an AI-assisted revenue recovery platform designed to help merchants recover revenue from failed payments.

The system processes revenue-loss events, identifies whether a case is eligible for recovery, analyzes the likely cause of the failure, recommends a bounded recovery action, simulates the recovery attempt, records the outcome, and measures the resulting recovered revenue.

The MVP focuses exclusively on failed-payment recovery.

## 2. Problem

Businesses can lose revenue when customer payments fail because of temporary gateway failures, payment-method problems, repeated failures, or other payment issues.

Simple retry rules may waste recovery attempts or repeatedly target cases that should instead be escalated to a human.

ReviveAI aims to make recovery decisions more contextual while keeping financial actions constrained by deterministic safety rules.

## 3. Target User

The primary user is a merchant, revenue operations team, or payment operations team that needs visibility into failed payments and a controlled way to recover eligible revenue.

## 4. MVP(Minimum Viable Product) Goal

The MVP must demonstrate the complete recovery workflow:

Failed payment -> risk detection -> safety checks -> root-cause analysis -> recovery decision -> bounded action -> simulated result -> metrics -> audit trail.

The product must measure results across a complete synthetic batch rather than relying on selected successful examples.

## 5. Allowed Recovery Actions

ReviveAI supports the following bounded actions:

- `RETRY_PAYMENT`
- `SEND_REMINDER`
- `OFFER_GRACE_PERIOD`
- `ESCALATE_TO_HUMAN`
- `STOP`

The AI may recommend only one of these actions.

The backend must validate the recommendation against deterministic recovery policies before any action is executed.

## 6. AI Responsibilities

AI is used for tasks where contextual reasoning provides value:

- Interpreting payment-failure context
- Identifying a likely root cause
- Recommending an allowed recovery action
- Providing an explanation for the recommendation
- Generating a recovery message when appropriate

AI is not responsible for:

- Financial calculations
- Retry limits
- Safety policies
- Eligibility enforcement
- Stopping rules
- Ground-truth evaluation
- KPI calculations
- Database integrity
- Executing arbitrary financial actions

## 7. Safety Principles

ReviveAI is a financial-recovery prototype, so automated actions must be bounded.

The system must enforce:

- Maximum retry attempts
- Eligibility rules
- Transaction-value limits
- Cooldowns where required
- Stopping conditions
- Human escalation
- Allowed-action validation
- Safe fallback when AI output is invalid or unavailable

If the AI produces an invalid or unsafe recommendation, the system must reject it and use a deterministic fallback such as `ESCALATE_TO_HUMAN` or `STOP`.

## 8. Recovery Simulator

The MVP will not connect to real payment providers or execute real financial transactions.

Instead, ReviveAI will use a deterministic simulator based on synthetic ground-truth data.

The simulator must support:

- Successful recovery
- Failed recovery
- Repeated failure
- Retry-limit reached
- Human escalation

All recovery metrics must be calculated from actual simulator results.

## 9. Synthetic Dataset

The project will use synthetic revenue-event data.

The initial dataset target is approximately 500–1,000 records.

Each record should contain enough information to evaluate recovery decisions and outcomes, including transaction details, failure context, previous attempts, customer context, expected action, recoverability, and actual recovery outcome.

The dataset must be reproducible using a fixed random seed.

The dataset is synthetic and must not be represented as real merchant data.

## 10. Dashboard Requirements

The dashboard must provide visibility into:

- Revenue at risk
- Potentially recoverable revenue
- Revenue recovered
- Recovery rate
- Recovery attempts
- Successful recoveries
- Escalated cases
- Unresolved cases

Metrics must be calculated dynamically from processed records.

## 11. Transaction Explorer

Users must be able to inspect individual recovery cases.

A transaction detail view should display:

- Transaction ID
- Customer
- Amount
- Failure/problem
- Risk information
- Likely root cause
- AI recommendation
- Action taken
- Recovery result
- Amount recovered
- Relevant audit events

## 12. Audit Trail

Meaningful recovery events must be recorded with:

- Timestamp
- Transaction
- Event
- Decision
- Reason
- Action
- Result

The audit trail must allow a reviewer to understand why a recovery decision occurred.

## 13. Evaluation

The system will be evaluated on a complete synthetic batch.

Evaluation should include appropriate decision metrics such as:

- Precision
- Recall
- F1 where applicable
- False positives
- False negatives

Business metrics should include:

- Revenue at risk
- Potentially recoverable revenue
- Revenue recovered
- Recovery rate
- Recovery attempts
- Escalation rate
- Unresolved amount

Safety evaluation should include:

- Invalid AI actions
- Actions blocked by guardrails
- Retry-limit violations
- Unsafe automatic recovery attempts

No evaluation metric may be manually hardcoded.

## 14. Testing Requirements

The project must include automated tests covering:

- Dataset validation
- Recovery policies
- Retry limits
- High-value transactions
- Repeated failures
- Human escalation
- AI schema validation
- Invalid AI responses
- API validation
- Error handling
- Metric calculations

## 15. Explicit Non-Goals

The MVP will not:

- Process real payments
- Access real merchant payment accounts
- Execute real financial transactions
- Send real customer communications
- Implement every revenue-loss scenario
- Use machine learning merely for the purpose of adding an ML component
- Give an LLM unrestricted authority over financial actions

## 16. Success Criteria

The MVP is successful if it can process a complete synthetic batch and demonstrate:

1. Revenue-risk detection
2. Safe recovery eligibility decisions
3. AI-assisted contextual reasoning
4. Bounded recovery actions
5. Deterministic safety enforcement
6. Simulated recovery outcomes
7. Measured recovered revenue
8. Human escalation
9. Complete auditability
10. Automated evaluation and testing

The final product should demonstrate that AI can improve revenue-recovery decisions without giving an AI model unrestricted control over financial operations.
