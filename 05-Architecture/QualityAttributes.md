# Quality Attributes

## Functional vs Non-Functional Requirements

Functional requirements define **what** the system should do, while non-functional requirements define **how well** the system should perform.

- **Functional Requirements:** User Login, Search Products, Place Order, Process Payment.
- **Non-Functional Requirements:** Scalability, Availability, Reliability, Performance, Security.

Non-Functional Requirements (NFRs) are also known as **Quality Attributes** because they describe the quality characteristics of the system.

---

## 1. Availability

Availability is the ability of a system to remain accessible to users when they need it. It is typically measured as **percentage uptime** over a year.

| Availability | Downtime / Year | Downtime / Month |
|---|---|---|
| 99% | 3.65 days | 7.2 hours |
| 99.9% | 8.76 hours | 43.8 minutes |

**Why is it important?**

If the system is unavailable, users cannot access the application, leading to poor user experience, lost revenue, and reduced customer trust.

**How do we achieve it?**

- Use a load balancer with health checks to route traffic only to healthy instances.
- Eliminate single points of failure, such as a single application server or database.
- Deploy across multiple Availability Zones (AZs) or regions.
- Configure automatic failover so that healthy instances take over when failures occur.

**Example**

Amazon can continue accepting orders even if one application server fails because the load balancer automatically detects the unhealthy server and routes traffic to healthy instances without affecting users.

---

## 2. Reliability

Reliability is the ability of a system to consistently produce the **correct business outcome**.

It is commonly measured using the **Business Error Rate** — the percentage of requests that result in an incorrect business outcome, such as duplicate orders, lost payments, incorrect inventory updates, or inconsistent data. Business errors are detected by monitoring and performing reconciliation in the system.

**Why is it important?**

Users trust a system only if it consistently produces the correct results.

**How do we achieve it?**

- Perform periodic reconciliation.
- Monitor business invariants and generate alerts when they are violated.
- Implement comprehensive automated testing.

**Example**

A customer pays ₹5,000 for an order. A network timeout occurs after the payment is processed, causing the client to retry the request.

A reliable system uses an **idempotency key** to recognize the retry and ensures that the payment is processed only once and exactly one order is created. If the system detects two orders for the same payment, or a payment without an order, it records a business invariant violation and raises an alert for investigation.

---

## 3. Scalability

Scalability is the ability of a system to handle increased workload by adding computing resources while maintaining acceptable performance.

> **Important:** *Elasticity* is an automated form of scalability. A system must first be scalable before it can be elastic. **Scalability** is the architectural capability to handle increased load by adding resources, while **elasticity** is the operational capability to automatically add and remove those resources based on demand.

**Why is it important?**

As the business grows, the application should continue to perform well.

**How do we achieve it?**

- **Vertical Scaling (Scale Up)** – Increase the CPU, RAM, or storage of an existing server.
- **Horizontal Scaling (Scale Out)** – Add more servers or instances behind a load balancer.
- Database sharding.
- Microservices.

**Example**

During a festival sale, an e-commerce application scales from 100 servers to 500 servers to handle increased traffic.

---

## 4. Modifiability & Maintainability

Modifiability and maintainability is the ability of a system to be maintained and modified easily without significantly affecting other parts of the system.

**Why is it important?**

Software systems continuously evolve due to changing business requirements, new integrations, and bug fixes. A well-designed system reduces development effort and enables teams to deliver changes quickly and safely.

**How do we achieve it?**

- Modular architecture
- Loose coupling
- Clean, readable code
- Appropriate design patterns
- Good documentation
- Comprehensive automated testing

**Example**

If a bug is later discovered in the payment logic, it can be fixed within the Payment Service without affecting the Product, Order, or Inventory services.

---

## 5. Security

Security is the ability of a system to protect its data, services, and resources from unauthorized access, modification, and disclosure.

**Why is it important?**

Applications often process sensitive customer data. Weak security can lead to data breaches and loss of customer trust.

**How do we achieve it?**

- **Authentication** (verify identity)
- **Authorization** (control access using least privilege)
- **Encryption** (data at rest and in transit)
- Input validation
- Security monitoring, logging, and auditing
- Regular vulnerability scanning and patching

**Example**

A customer logs into an e-commerce application. The system authenticates the user, authorizes access only to their own orders, encrypts communication using HTTPS, and prevents SQL injection through input validation.

---

## 6. Performance

Performance is how efficiently a system handles work. It is measured using two key metrics:

- **Latency** – The time taken to complete a single request.
- **Throughput** – The number of requests the system can process in a given period (for example, requests per second).

**Why is it important?**

Fast applications provide a better user experience, improve customer satisfaction, and support higher business volume. Poor performance can lead to user frustration, abandoned transactions, and reduced system capacity.

**How do we achieve it?**

- Caching
- Efficient database queries and indexing
- Asynchronous processing
- Connection pooling
- Content Delivery Networks (CDNs)
- Load balancing
- Optimized algorithms and data structures

**Example**

In an e-commerce application:

- A customer searches for a product, and the search results are displayed in **150 ms** (latency).
- During a flash sale, the application processes **20,000 search requests per second** (throughput).

---

## 7. Resilience

Resilience is the ability of a system to continue operating, or recover quickly, when failures occur.

**Why is it important?**

Failures are inevitable in distributed systems.

**How do we achieve it?**

- Retry mechanisms
- Circuit breakers
- Timeouts
- Message queues
- Graceful degradation
- Failover

**Example**

If the Notification Service is unavailable, the order is still placed successfully, and the notification is sent later when the service recovers.

---

## 8. Observability

Observability is the ability to understand the internal state of a system by analyzing its outputs.

**Why is it important?**

It helps engineers quickly detect, diagnose, and resolve production issues.

**How do we achieve it?**

- Logging
- Metrics
- Distributed tracing
- Dashboards
- Alerts

**Example**

If payment requests suddenly fail, dashboards, logs, and traces help identify whether the problem is in the Payment Service, database, or external payment gateway.

---

## 9. Cost

Cost refers to the infrastructure, licensing, development, and operational expenses of the system.

**Why is it important?**

Architects must balance technical excellence with business budgets.

**How do we achieve it?**

- Right-size infrastructure
- Auto-scaling
- Serverless where appropriate
- Managed cloud services
- Optimize resource utilization

**Example**

Use auto-scaling so extra servers run only during peak shopping hours, reducing cloud costs.
