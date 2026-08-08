# ADR-0001: Use PostgreSQL as the Primary Transactional Database

- **Status:** Accepted
- **Date:** 2026-08-08
- **Deciders:** Architecture Team

---

## Context

The application requires a primary database to manage users, orders, payments, and inventory. These operations involve multiple related entities and require **ACID transactions**, **strong consistency**, and **complex relational queries**. The engineering team has extensive SQL experience, and the system is expected to grow while maintaining data correctness.

---

## Decision Drivers

1. Strong transactional consistency
2. ACID transaction support
3. Support for joins and complex SQL queries
4. Team expertise and operational simplicity
5. Scalability for future growth

---

## Decision

Use **PostgreSQL** as the primary transactional database for the application.

---

## Alternatives Considered

### PostgreSQL

**What it offers**

- Full ACID transaction support
- Strong consistency
- Rich SQL support with joins
- Mature ecosystem and tooling
- Reliable backup, replication, and indexing capabilities

**Why it was selected**

It best satisfies the application's transactional requirements, relational data model, and the team's existing expertise.

---

### MongoDB

**What it offers**

- Flexible schema
- Easy horizontal scaling
- High performance for document-based workloads
- Rapid development for evolving data models

**Why it was not selected**

Although MongoDB provides excellent flexibility and scalability, the application relies heavily on relational data, transactions, and complex queries involving multiple entities. PostgreSQL is a better fit for these requirements.

---

## Consequences

### Positive

- Strong transactional consistency
- Reliable processing of orders and payments
- Excellent SQL support for reporting and analytics
- Mature ecosystem with extensive tooling and community support

### Negative

- Horizontal scaling is more complex than document databases
- Schema changes require database migrations

### Neutral

- Database schema changes must be managed through migration scripts.
- The team must maintain PostgreSQL operational knowledge.

---

## Revisit Triggers

Reconsider this decision if:

- The application becomes primarily document-oriented.
- Horizontal write scalability becomes the primary requirement.
- The data model no longer requires joins or ACID transactions.
- Business requirements favor schema flexibility over relational consistency.
