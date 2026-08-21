# ReviveAI — System Architecture

## 1. Architecture Overview

ReviveAI uses a layered architecture consisting of a React frontend, FastAPI backend, recovery engine, AI analysis layer, deterministic safety guardrails, recovery simulator, audit logging, and persistent data storage.

The system is designed so that AI can provide contextual reasoning without having unrestricted authority over financial recovery actions.

## 2. High-Level Flow

Revenue Event
     ↓
FastAPI Backend
     ↓
Risk Detection
     ↓
Safety / Eligibility Checks
     ↓
AI Root-Cause Analysis
     ↓
Bounded Recovery Recommendation
     ↓
Deterministic Policy Validation
     ↓
Recovery Simulator
     ↓
Recovery Result
     ↓
Metrics + Audit Trail


The React frontend communicates with the FastAPI backend through HTTP APIs using structured JSON.

## 3. Frontend

The frontend will be implemented using React.

Its responsibilities include:

* Displaying revenue-recovery KPIs
* Displaying transaction/recovery cases
* Showing individual transaction details
* Displaying AI recommendations
* Showing recovery results
* Displaying the audit trail
* Presenting evaluation results

The frontend does not make financial recovery decisions.

## 4. Backend

The backend will use Python and FastAPI.

Its responsibilities include:

* API request handling
* Input validation
* Transaction processing
* Risk detection
* Recovery policy enforcement
* AI orchestration
* Recovery simulation
* Metrics calculation
* Audit logging
* Error handling

Business rules should remain separated from HTTP/API handling where practical.

## 5. Recovery Engine

The recovery engine contains deterministic business logic.

It determines whether an action is permitted based on rules such as:

* Failure reason
* Previous retry count
* Transaction amount
* Recovery eligibility
* Previous recovery outcomes
* Stopping conditions
* Escalation requirements

The recovery engine must not rely on the LLM for safety-critical enforcement.

## 6. AI Analysis Layer

The AI layer provides contextual reasoning where an LLM adds useful value.

It may:

* Interpret failure context
* Identify a likely root cause
* Recommend an allowed recovery action
* Explain its recommendation
* Generate a recovery message where appropriate

The AI output must follow a structured schema.

The AI is not allowed to invent arbitrary actions or directly execute financial operations.

## 7. Guardrails

Deterministic guardrails are placed between AI recommendations and recovery execution.

The guardrail layer validates:

* Whether the transaction is eligible
* Whether the requested action is allowed
* Retry limits
* Transaction-value limits
* Stopping rules
* Escalation requirements
* Required fields in the AI response

If an AI response is invalid or unsafe, the system must reject it and use a safe fallback such as `ESCALATE_TO_HUMAN` or `STOP`.

## 8. Allowed Actions

The MVP supports five recovery actions:


* RETRY_PAYMENT
* SEND_REMINDER
* OFFER_GRACE_PERIOD
* ESCALATE_TO_HUMAN
* STOP


The backend maintains the authoritative list of allowed actions.

## 9. Recovery Simulator

The simulator represents payment-recovery outcomes without connecting to real payment systems.

It uses synthetic ground-truth data to model:

* Successful recovery
* Failed recovery
* Repeated failure
* Retry-limit reached
* Human escalation

The simulator records the actual outcome used for evaluation and dashboard metrics.

## 10. Audit Layer

The audit logger records meaningful events throughout the recovery workflow.

An audit event should include:

* Timestamp
* Transaction ID
* Event type
* Decision
* Reason
* Action
* Result

This allows a reviewer to understand how and why a recovery decision occurred.

## 11. Data Layer

The initial implementation will use synthetic data and SQLite where persistence is required.

The data layer will store information necessary for:

* Revenue events
* Recovery decisions
* Recovery attempts
* Results
* Audit events

The architecture should allow migration to PostgreSQL later if the application needs to support larger workloads.

## 12. Security and Financial Safety

ReviveAI is a prototype and must not execute real financial transactions.

No real payment credentials or merchant payment accounts will be connected.

All recovery actions occur through the simulator.

The system must also prevent unrestricted AI control over financial operations through deterministic validation and bounded action policies.

## 13. Evaluation Flow

The evaluation system processes a complete synthetic batch.


Synthetic Dataset
       |
ReviveAI Recovery Pipeline
       |
Predicted Decisions
       |
Ground Truth Comparison
       |
Decision Metrics
       +
Business Metrics
       +
Safety Metrics


Metrics must be calculated programmatically from actual results.

## 14. Design Principle

The central architectural principle is:

***Use AI for contextual reasoning and deterministic software for deterministic, safety-critical decisions***.

This separation allows ReviveAI to benefit from AI reasoning while keeping financial recovery actions constrained, auditable, and testable.
