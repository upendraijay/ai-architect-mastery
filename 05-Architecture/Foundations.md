# Architecture Foundations

## Software Architecture

Software architecture is the blueprint of a software system. It defines the logical components of the system and how they interact with each other.

### Example: E-Commerce Application

The architecture identifies the major components — User Service, Product Service, Order Service, Inventory Service, Payment Service, Notification Service — and defines how these services communicate.

Order placement flow:

1. The customer places an order.
2. The request reaches the **Order Service**.
3. The **Order Service** asks the **Inventory Service** to validate that the product is available.
4. If the product is available, the **Order Service** requests the **Payment Service** to process the payment.
5. If the payment is successful, the **Inventory Service** confirms the order and updates (decrements) the stock.
6. The **Notification Service** sends an email or SMS confirmation to the customer.

### Purpose of Software Architecture

The purpose of software architecture is to organize the system in a way that makes it easier to develop, maintain, and scale.

---

## Responsibilities of a Software Architect

### 1. Understand Business Requirements

Before designing the system, the architect first understands the business problem.

Questions include:

- What problem are we solving?
- What are the business goals?
- Who are the users?

**Example:** If the business expects **10 million users** and **100,000 orders per hour**, the architecture will be very different from a system expected to support only a few thousand users.

---

### 2. Ensure Non-Functional Requirements

The architect ensures that the system satisfies important quality attributes.

- **Scalability** – Can the system handle increasing users and traffic?
- **Security** – Is customer data protected through authentication, authorization, and encryption?
- **Performance** – Does the system meet the required response time and throughput?

---

### 3. Design the System Architecture

The architect identifies the major components of the system, assigns clear responsibilities to each component, and defines how they communicate.

---

### 4. Make Technical Trade-offs

Every architectural decision involves trade-offs. There is rarely a single "best" solution.

| Decision | Trade-off |
|---|---|
| **Monolith vs Microservices** | Monoliths are simpler to develop and deploy initially, while microservices offer better scalability and independent deployments but increase operational complexity. |
| **Performance vs Cost** | Adding more servers improves performance but increases infrastructure costs. |
| **Simplicity vs Flexibility** | A simple design is easier to build and maintain, while a more flexible design can better accommodate future requirements but adds complexity. |

The architect evaluates these trade-offs and chooses the solution that best aligns with the business goals, budget, and long-term vision.

---

## Software Architecture vs System Design vs Solution Architecture

| Aspect | Software Architecture | System Design | Solution Architecture |
|---|---|---|---|
| **Definition** | Defines the high-level structure of a software application, its components, and their interactions. | Designs how a specific system or feature is implemented in detail. | Designs a complete business solution by integrating multiple applications, technologies, and business processes. |
| **Focus** | Application structure. | Technical implementation. | End-to-end business solution. |
| **Key Questions** | What are the major components? How do they interact? | How should this feature be built? | How do different systems work together to solve a business problem? |
| **Main Deliverables** | Architecture diagrams, technology choices, architectural decisions. | APIs, database design, caching strategy, algorithms. | Solution architecture diagrams, integration design, data flows, technology stack. |
| **Primary Goal** | Build a maintainable, scalable, and modular application. | Build an efficient, reliable, and scalable system. | Deliver a complete business solution. |
