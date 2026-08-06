# Resume Baseline

## Top 3 Projects

### **1. Enterprise AEM DAM Agentic Platform — IBM (Current)**

Designed and developed an enterprise-grade multi-agent platform for Adobe Experience Manager (AEM) Digital Asset Management using LangGraph. Built a capability-agnostic orchestration framework where a master orchestrator routes requests to specialized worker agents through a single structured `RoutingDecision` model. Implemented human-in-the-loop workflows using LangGraph's native `interrupt()` mechanism, shared checkpointing, and composite thread identifiers to enable scalable, stateful, and extensible agent execution.

---

### **2. Multi-Agent Contract Review System — Accolite (Insurance Client)**

Architected a LangGraph- and GPT-based multi-agent platform that validates insurance policy documents against mainframe records. Designed specialized review agents for policy validation, discrepancy detection, and compliance checks. Deployed the solution on AWS using Docker, reducing manual CSR review effort by approximately **90%** while improving review consistency and turnaround time.

---

### **3. Weaviate Row-Level Security Platform via MCP Server — Accolite**

Designed and implemented server-side, relationship-based access control for Weaviate using an MCP server. Enforced manager–subordinate inheritance and row-level security directly at the retrieval layer rather than in application code, ensuring secure, scalable, and centralized authorization for enterprise knowledge retrieval systems.

---

# Biggest Architectural Contribution

### **Capability-Agnostic Multi-Agent Orchestration Framework**

Designed a reusable orchestration architecture where the orchestrator remains completely independent of worker implementations. All routing decisions are driven through a single structured `RoutingDecision` model, while business capabilities are exposed as modular tools rather than hard-coded execution paths. This architecture enables new agents to be introduced without modifying orchestration logic, significantly improving extensibility, maintainability, and long-term scalability.

---

# Biggest Leadership Contribution

### **Established the Engineering Architecture Standard for the DAM Platform**

Defined the architectural vision and engineering principles for the enterprise DAM platform. Authored the platform design principles, drove architecture review discussions, incorporated cross-team feedback, and established the reference architecture adopted by the engineering team. Beyond implementation, this work created the technical foundation and development standards guiding future platform evolution.

---

# Largest Production System

### **Enterprise AEM DAM Agentic Platform on IBM Cloud/OpenShift**

Leading the design and implementation of a production-scale agentic AI platform deployed on IBM Cloud/OpenShift. The platform orchestrates multiple AI workers responsible for repository discovery, metadata intelligence, folder hierarchy generation, taxonomy mapping, governance, migration planning, and human-assisted workflows, providing a scalable foundation for enterprise digital asset management and migration automation.
