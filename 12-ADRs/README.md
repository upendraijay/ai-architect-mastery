# Architecture Decision Records (ADRs)

## What is an ADR?

An **Architecture Decision Record (ADR)** is a short, immutable document that captures a single architectural decision, the context in which it was made, the decision drivers, the alternatives considered, the chosen solution, and the consequences.

The emphasis is on **single** and **immutable**:

- **Single** — each ADR should capture exactly one architectural decision.
- **Immutable** — an ADR records a decision at a point in time using the information available then. If the decision changes later, create a new ADR instead of modifying the old one.

During architecture design, the team evaluates multiple trade-offs and selects the best option. Once the decision is made, it is documented in an ADR, and implementation begins.

---

## Why ADRs Exist

ADRs exist so we remember **why** these decisions were made. They solve this problem by documenting the reasoning behind important architectural decisions.

---

## ADR Lifecycle

| Status | Meaning |
|---|---|
| **Proposed** | Under discussion |
| **Accepted** | Official architectural decision |
| **Rejected** | Considered but intentionally not chosen |
| **Superseded** | Replaced by a newer ADR |
| **Deprecated** | No longer applicable |

---

## ADR Structure

### Header

| Field | Example |
|---|---|
| **Title** | ADR-0007: Use PostgreSQL as the Primary Transactional Database |
| **Status** | Accepted |
| **Accepted Date** | 2026-08-08 |
| **Deciders** | Platform Team |
| **Supersedes** | ADR-0003 |

---

### 1. Context

Describe the situation **before** the decision was made. This section explains why a decision was needed, but does not justify or describe the selected solution.

Include relevant information such as:

- Business problem
- Functional requirements
- Quality attribute requirements
- Constraints
- Existing architecture
- Timeline
- Budget
- Team expertise

---

### 2. Decision Drivers

Decision drivers are the criteria used to evaluate and compare the available options. List the drivers in **priority order**, from most important to least important.

**Example:**

1. Availability
2. Operational simplicity
3. Cost
4. Horizontal scalability

The ordering is important because it reflects the trade-offs the team is willing to make.

---

### 3. Decision

State the decision clearly and concisely. Describe **what** has been decided, not why it was chosen.

**Example:**

> We will use PostgreSQL 16 on Amazon RDS Multi-AZ as the primary transactional database.

---

### 4. Alternatives Considered

Document the viable alternatives that were evaluated before making the decision. For each alternative, include:

- **What it offers** – A brief description of the approach or technology.
- **Why it was considered** – The strengths or benefits that made it a viable option.
- **Why it was not selected** – The key reasons it did not meet the decision drivers as well as the chosen solution.

---

### 5. Consequences

Every architectural decision has consequences. Document both the benefits and the trade-offs introduced by the decision.

**Positive** — Describe the advantages gained from the decision.

**Negative** — Describe the drawbacks, limitations, or risks introduced by the decision.
