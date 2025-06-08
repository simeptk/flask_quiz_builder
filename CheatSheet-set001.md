# Google Cloud Professional Cloud Architect Exam Cheat Sheet

Remember, passing requires not just knowing *what* a service does, but *how* it fits into a solution to meet specific business and technical requirements, especially in case studies.

---

```markdown
**Purpose:** High-level overview of key GCP concepts and services aligned with the exam syllabus, focusing on use cases and architectural decisions.

**Disclaimer:** This is a study aid, not a substitute for hands-on experience and in-depth documentation review. The exam tests application of knowledge, not just memorization.

---

## 1. Designing and planning a cloud solution architecture (~24%)

**Core Concepts:** Resource Hierarchy, VPC Networking, Hybrid Connectivity, Compute Options, Storage Options, Database Options, Migration Strategies, HA/DR, Scalability, Cost Optimization, Load Balancing.

*   **Resource Hierarchy (Org -> Folders -> Projects):**
    *   **Purpose:** Organize resources, manage IAM policies and Organization Policies consistently.
    *   **Use Case:** Structure environments (prod, stage, dev) in separate projects under folders for isolation and policy inheritance. Apply a global network policy at the Organization level.

*   **VPC Network:**
    *   **Purpose:** Global private network for GCP resources. Subnets are regional.
    *   **Use Case:** Create a single, large VPC network for an organization (often via Shared VPC) to simplify networking and inter-service communication.

*   **Shared VPC:**
    *   **Purpose:** Allows multiple Service Projects to share a common Host Project VPC network.
    *   **Use Case:** Centralize network administration in a Host Project while allowing different teams/applications in Service Projects to deploy resources into that network.

*   **VPC Network Peering:**
    *   **Purpose:** Connect two separate VPC networks privately.
    *   **Use Case:** Connect VPCs from different organizations or projects that don't use Shared VPC, enabling private communication between them.

*   **Hybrid Connectivity (Cloud VPN, Cloud Interconnect):**
    *   **Purpose:** Connect on-premises networks to GCP VPCs.
    *   **Use Case:**
        *   **Cloud VPN (IPsec):** Secure connection over the public internet. Suitable for lower bandwidth, non-mission-critical connections.
        *   **Cloud Interconnect (Dedicated/Partner):** High-bandwidth, low-latency, dedicated connection. Suitable for mission-critical applications, large data transfers, hybrid cloud with high traffic.

*   **Compute Options:**
    *   **Compute Engine (CE):** Managed VMs.
        *   **Use Case:** Lift-and-shift legacy applications, custom OS requirements, specific hardware needs (GPUs, TPUs), stateful applications not easily containerized.
    *   **Google Kubernetes Engine (GKE):** Managed Kubernetes for containers.
        *   **Use Case:** Microservices, containerized applications needing orchestration, portability, scaling, self-healing, service discovery.
    *   **Cloud Run:** Serverless platform for containers.
        *   **Use Case:** Request-driven stateless containers, scales down to zero, ideal for web services, APIs, background jobs with variable traffic.
    *   **Cloud Functions:** Serverless Function as a Service (FaaS).
        *   **Use Case:** Event-driven workloads (responds to changes in storage, messages in Pub/Sub, HTTP requests), short-lived tasks, microservices broken down to minimal units.
    *   **App Engine (Standard/Flexible):** Managed application platform.
        *   **Use Case:** Web applications, APIs, scales automatically (Standard scales to zero, Flexible uses containers on VMs). Standard is more opinionated/restrictive, Flexible offers more control.

*   **Storage Options (Cloud Storage):**
    *   **Standard:** Hot data, frequent access, low latency. (Websites, mobile apps)
    *   **Nearline:** Cold data, <1 access/month. (Backups, DR)
    *   **Coldline:** Colder data, <1 access/quarter. (Archives, Long-term DR)
    *   **Archive:** Coldest data, <1 access/year. (Deep archives, Compliance)
    *   **Use Case:** Choose based on data access frequency to optimize cost vs. retrieval time/cost. Use Object Lifecycle Management to automate transitions.

*   **Block Storage (Persistent Disks):**
    *   **Standard PD:** Cost-effective, for boot disks or workloads with sequential reads/writes.
    *   **Balanced PD:** Balance of cost and performance, for most general applications.
    *   **SSD PD:** High performance, for databases, enterprise applications.
    *   **Extreme PD:** Highest performance, for extremely demanding databases.
    *   **Use Case:** Root disks for VMs, data volumes for databases or applications running on Compute Engine or GKE.

*   **File Storage (Cloud Filestore):**
    *   **Purpose:** Managed NFS file shares.
    *   **Use Case:** Applications requiring shared file system access (e.g., enterprise applications, media rendering, shared development environments).

*   **Database Options:**
    *   **Cloud SQL:** Managed Relational (MySQL, Postgre, SQL Server).
        *   **Use Case:** Traditional RDBMS workloads, lift-and-shift of existing relational databases, regional availability.
    *   **Cloud Spanner:** Managed Global Relational with strong consistency.
        *   **Use Case:** Mission-critical, globally distributed applications needing high availability (99.999%) and strong consistency worldwide (e.g., financial transactions, global gaming leaderboards).
    *   **Cloud Firestore:** Managed NoSQL Document (Serverless).
        *   **Use Case:** Mobile, web, serverless backends needing real-time sync, flexible schema, scales automatically.
    *   **Cloud Bigtable:** Managed NoSQL Wide-Column.
        *   **Use Case:** High-throughput, low-latency workloads with massive amounts of single-keyed data (e.g., time-series data, IoT data, operational/analytic data for large-scale applications).
    *   **BigQuery:** Managed Serverless Data Warehouse (OLAP).
        *   **Use Case:** Large-scale data analytics, business intelligence, running complex SQL queries over petabytes of data, batch and streaming analytics.

*   **Migration Strategies & Tools:**
    *   **Lift-and-Shift:** Migrate VMs as-is (Migrate to Virtual Machines).
    *   **Containerization:** Migrate VMs to containers (Migrate to Containers).
    *   **Replatforming:** Move to a managed service (e.g., self-hosted DB to Cloud SQL/Spanner, Kafka on VMs to Pub/Sub).
    *   **Refactoring/Re-architecting:** Rewrite for cloud-native (e.g., monolith to microservices on GKE/Cloud Run/Functions).
    *   **Data Migration:** Transfer Appliance (offline petabyte scale), Storage Transfer Service (online to Cloud Storage), Database Migration Service (DMS) (DB specific).
    *   **Use Case:** Choose strategy based on cost, time, complexity tolerance, and desired future state. Use Migration Center for assessment and planning.

*   **High Availability (HA) & Disaster Recovery (DR):**
    *   **HA:** Design within a region (multi-zone deployment for VMs/GKE, regional managed services like Cloud SQL HA).
    *   **DR:** Design across regions (multi-region deployments for Spanner/GCS, cross-region replication for Cloud SQL, DR patterns like Pilot Light, Warm Standby, Hot Standby).
    *   **RTO (Recovery Time Objective):** Max time to restore service after failure.
    *   **RPO (Recovery Point Objective):** Max acceptable data loss.
    *   **Use Case:** Select architecture and DR strategy based on required RTO/RPO for critical applications.

*   **Scalability & Elasticity:**
    *   **Vertical Scaling:** Increase resources of a single instance (Cloud SQL instance size).
    *   **Horizontal Scaling:** Add more instances (MIGs, GKE HPA, Cloud Run/Functions automatic scaling).
    *   **Elasticity:** Ability to automatically scale up/down based on load (MIGs autoscaling, GKE Cluster Autoscaler/HPA, Cloud Run/Functions).
    *   **Use Case:** Design for elasticity to handle variable load and optimize costs.

*   **Cost Optimization:**
    *   **Managed Services:** Reduce operational overhead.
    *   **Autoscaling/Serverless:** Pay only for resources used.
    *   **Right-sizing:** Choose appropriate machine types/sizes based on actual workload needs (use Cloud Monitoring/Recommendations).
    *   **Storage Class:** Match class to access frequency.
    *   **Preemptible/Spot VMs:** For fault-tolerant batch jobs.
    *   **Committed Use Discounts (CUDs):** For stable, predictable workloads.
    *   **Object Lifecycle Management:** Automate storage tiering.
    *   **Use Case:** Continuously monitor costs (Billing Reports), use recommendations, and apply appropriate services/configurations.

*   **Load Balancing:**
    *   **Global HTTP(S) Load Balancer:** Global external LB for web traffic, directs to closest backend, supports CDN. (Global web apps)
    *   **Regional External HTTP(S) LB:** Regional external LB for web traffic. (Regional web apps)
    *   **Internal HTTP(S) LB:** Regional internal LB for HTTP/S traffic within VPC. (Microservice communication)
    *   **Network Load Balancer (TCP/UDP):** Regional external passthrough LB for TCP/UDP traffic. (Non-HTTP/S protocols)
    *   **Internal TCP/UDP LB:** Regional internal passthrough LB for TCP/UDP within VPC. (Internal non-HTTP/S)
    *   **SSL Proxy/TCP Proxy LB:** Global external LBs for SSL/TCP traffic. (Specific protocol needs)
    *   **Use Case:** Choose based on traffic type (HTTP/S vs TCP/UDP), scope (Global vs Regional), and source (External vs Internal).

---

## 2. Managing and provisioning the solution infrastructure (~15%)

**Core Concepts:** Infrastructure as Code (IaC), Instance Templates, OS Patch Management, Shared VPC Configuration, Private Networking, Secrets Management.

*   **Infrastructure as Code (IaC):**
    *   **Tools:** Cloud Deployment Manager (native), Terraform (popular multi-cloud).
    *   **Purpose:** Automate provisioning and management of infrastructure declaratively.
    *   **Use Case:** Deploy consistent, repeatable environments (Dev, Stage, Prod), manage infrastructure state, version control infrastructure configurations.

*   **Instance Templates:**
    *   **Purpose:** Define machine type, boot disk, labels, metadata, startup scripts, etc., for creating identical Compute Engine VMs.
    *   **Use Case:** Used by Managed Instance Groups (MIGs) and individual instances for consistent VM creation.

*   **OS Patch Management:**
    *   **Purpose:** Automate patching of OS on Compute Engine VMs.
    *   **Use Case:** Ensure VMs are up-to-date with security patches and bug fixes across a fleet.

*   **Shared VPC Configuration:**
    *   **Purpose:** Set up host and service projects, manage `compute.networkUser` role.
    *   **Use Case:** Allow Service Projects to utilize the centralized network of the Host Project.

*   **Private Networking:**
    *   **Purpose:** Ensure communication happens over private IP space, not public internet.
    *   **Use Case:**
        *   **VPC Firewall Rules:** Control ingress/egress traffic based on tags, service accounts, IP ranges, protocols/ports.
        *   **Serverless VPC Access:** Allows serverless services (Functions, Run, App Engine) to connect to resources in a VPC network using internal IPs.
        *   **Private Google Access:** Allows VMs without external IPs to access Google APIs (like Cloud Storage, BigQuery) using internal IPs.

*   **Secrets Management (Secret Manager):**
    *   **Purpose:** Securely store, manage, and access sensitive data like API keys, passwords.
    *   **Use Case:** Retrieve database credentials or API keys in application code without storing them directly on VMs or in code repositories.

---

## 3. Analyzing and optimizing technical and business processes (~18%)

**Core Concepts:** Monitoring, Logging, Tracing, Profiling, Cost Analysis, Performance Tuning, Data Processing Services.

*   **Cloud Operations (formerly Stackdriver):** Integrated suite for observability.
    *   **Cloud Monitoring:** Collects metrics, creates dashboards, sets up alerting policies.
        *   **Use Case:** Monitor VM CPU utilization, database connections, request latency, create alerts when thresholds are crossed.
    *   **Cloud Logging:** Collects and stores logs from GCP services and applications.
        *   **Use Case:** Centralized log analysis for troubleshooting, create log-based metrics/alerts, export logs to BigQuery for analysis.
    *   **Cloud Trace:** Distributed tracing for request latency.
        *   **Use Case:** Identify performance bottlenecks across microservices in a request flow.
    *   **Cloud Profiler:** CPU and memory profiler.
        *   **Use Case:** Find resource-consuming functions in application code (running on CE, GKE, Cloud Run, Functions, App Engine).
    *   **Error Reporting:** Aggregates and analyzes application errors.
        *   **Use Case:** Get notified of application errors, view error frequency and details, link to relevant logs/traces.

*   **Cost Management:**
    *   **Billing Reports:** Analyze spending by service, project, SKU, label, region.
    *   **Pricing Calculator:** Estimate costs before deployment.
    *   **Cost Recommendations:** Suggestions for rightsizing VMs, deleting idle resources.
    *   **Use Case:** Track spending, identify cost drivers, forecast future costs, find optimization opportunities.

*   **Performance Optimization:**
    *   **Cloud CDN:** Cache content at edge locations. (Reduce latency for global users)
    *   **Load Balancing:** Distribute traffic efficiently.
    *   **Database Tuning:** Optimize queries, indexing, instance sizing, read replicas.
    *   **Autoscaling:** Match resources to demand.
    *   **Network Tier:** Choose Premium Tier for lower latency/global performance.
    *   **Use Case:** Improve application responsiveness, reduce load on backends, optimize resource usage.

*   **Data Processing Services:**
    *   **Dataflow:** Managed service for batch and streaming data processing (Apache Beam).
        *   **Use Case:** Complex ETL/ELT pipelines, real-time stream processing, large-scale batch transformations.
    *   **Dataproc:** Managed Apache Spark, Hadoop, Pig, Hive, Presto.
        *   **Use Case:** Lift-and-shift existing Hadoop/Spark jobs, large-scale batch processing using familiar frameworks.
    *   **Cloud Data Fusion:** Managed, visual ETL/ELT data integration.
        *   **Use Case:** Build and manage data pipelines with a GUI and pre-built connectors.
    *   **Pub/Sub:** Scalable messaging for streaming data and asynchronous tasks.
        *   **Use Case:** Decouple services, ingest high-velocity data streams, event-driven architectures.
    *   **BigQuery:** As mentioned, for large-scale analytics.

---

## 4. Designing for security and compliance (~18%)

**Core Concepts:** IAM, Resource Hierarchy Policies, Data Encryption (CMEK/CSEK), Secret Management, Network Security (Firewalls, VPC SC), Context-Aware Access, DLP, Security Command Center, SoD.

*   **IAM (Identity and Access Management):**
    *   **Purpose:** Who (principal) can do what (role) on which resource.
    *   **Principals:** Google Accounts, Service Accounts, Google Groups, Google Workspace/Cloud Identity domains.
    *   **Roles:** Primitive (Owner, Editor, Viewer), Predefined (service-specific), Custom.
    *   **Policy Hierarchy:** Policies inherited down the resource hierarchy (Org > Folder > Project > Resource).
    *   **Service Accounts:** Identity for applications/services. Grant roles *to* service accounts.
    *   **IAM Conditions:** Grant roles only under specific conditions (e.g., time of day, source IP, resource type).
    *   **Use Case:** Grant least privilege access, automate actions using service accounts, implement temporary access.

*   **Resource Hierarchy & Organization Policies:**
    *   **Purpose:** Enforce constraints on resource usage across the organization/folders/projects.
    *   **Use Case:** Restrict external IP creation, limit allowed VM images, enforce CMEK usage for certain services.

*   **Data Encryption:**
    *   **At Rest:** Google-managed (default), Customer-Managed Encryption Keys (CMEK in Cloud KMS), Customer-Supplied Encryption Keys (CSEK).
        *   **Use Case:** CMEK for organizational control over keys, compliance requirements. CSEK if you manage keys entirely yourself.
    *   **In Transit:** TLS/SSL (HTTPS Load Balancer, managed services).
        *   **Use Case:** Secure communication between users and applications, and between services.

*   **Cloud KMS (Key Management Service):**
    *   **Purpose:** Managed service for creating, managing, and using cryptographic keys.
    *   **Use Case:** Used with CMEK, direct encryption/decryption in applications, signing/verifying data. Includes Cloud HSM for FIPS 140-2 Level 3 requirements.

*   **VPC Service Controls:**
    *   **Purpose:** Create security perimeters around Google Cloud services to prevent data exfiltration.
    *   **Use Case:** Protect sensitive data in services like BigQuery, Cloud Storage, Cloud SQL from being moved to unauthorized projects or external networks, even if credentials are stolen.

*   **Identity-Aware Proxy (IAP) / Context-Aware Access:**
    *   **Purpose:** Control access to applications/VMs based on user identity and context (device, location, etc.) instead of just network origin. Part of BeyondCorp.
    *   **Use Case:** Secure access to internal web applications or VMs for remote employees without using a VPN.

*   **Data Loss Prevention (DLP) API:**
    *   **Purpose:** Discover, classify, and de-identify sensitive data (PII, credit card numbers, etc.).
    *   **Use Case:** Scan Cloud Storage buckets or BigQuery tables for sensitive data, mask or tokenize data before analysis.

*   **Security Command Center (SCC):**
    *   **Purpose:** Centralized security and data risk platform. Identifies vulnerabilities, threats, compliance findings.
    *   **Use Case:** Get an overview of your security posture, detect misconfigurations (e.g., public buckets, open ports), monitor compliance.

*   **Separation of Duties (SoD):**
    *   **Purpose:** Ensure no single individual has excessive permissions that could lead to fraud or error.
    *   **Use Case:** Assign different IAM roles to different users for critical tasks (e.g., one user can create KMS keys, another can use them).

---

## 5. Managing implementation (~11%)

**Core Concepts:** CI/CD, Developer Tools, API Management, Application Best Practices.

*   **CI/CD Pipeline:**
    *   **Cloud Source Repositories:** Managed Git repository.
    *   **Cloud Build:** Managed CI service (build, test, containerize).
    *   **Artifact Registry:** Managed repository for container images and other artifacts (replaces Container Registry).
    *   **Cloud Deploy:** Managed continuous delivery to GKE, Cloud Run, App Engine.
    *   **Use Case:** Automate the process of building, testing, and deploying applications from source code to production environments.

*   **Developer Tools:**
    *   **Cloud Shell:** Web-based terminal with Cloud SDK pre-installed. (Quick command-line access)
    *   **gcloud CLI:** Primary command-line tool for managing GCP resources.
    *   **gsutil CLI:** Command-line tool for managing Cloud Storage.
    *   **bq CLI:** Command-line tool for BigQuery.
    *   **Cloud SDK:** Libraries and tools for interacting with GCP APIs programmatically (Java, Python, Node.js, etc.).
    *   **Emulators:** Local emulators for services like Cloud Storage, Pub/Sub, Firestore/Datastore for offline development and testing.

*   **API Management:**
    *   **Cloud Endpoints:** Develop, deploy, manage APIs on GCP infrastructure. (Simple API gateway)
    *   **Apigee:** Full-lifecycle API management platform. (Advanced API gateway, developer portal, analytics, security)
    *   **Service Directory:** Managed service registry. (Discovering services by name)
    *   **Use Case:** Expose application functionality as APIs, secure APIs, manage API versions, onboard developers.

*   **Application Development Best Practices:**
    *   **Microservices:** Break down large applications into smaller, independent services. (Improved scalability, resilience, independent deployment)
    *   **APIs:** Define clear interfaces for service communication.
    *   **Resilience:** Implement patterns like retries (with exponential backoff), circuit breakers to handle transient failures between services.
    *   **Observability:** Build applications that are easy to monitor, log, trace, and debug.

---

## 6. Ensuring solution and operations reliability (~14%)

**Core Concepts:** Cloud Operations Suite, Deployment Strategies, Health Checks, DR Patterns, SRE Concepts, Debugging Tools.

*   **Cloud Operations Suite:** (See Section 3 - Monitoring, Logging, Alerting are key for reliability)
    *   **Use Case:** Proactively identify issues (alerts), diagnose root causes (logs, traces, profiling), understand system health (dashboards).

*   **Deployment Strategies:**
    *   **Rolling Update:** Gradually replace old version instances with new ones. (Minimizes downtime, allows rollback)
    *   **Blue/Green Deployment:** Deploy new version alongside old, switch traffic instantly. (Fast rollback)
    *   **Canary Deployment:** Release new version to a small subset of users, monitor, then roll out wider. (Reduce risk by testing in production)
    *   **Use Case:** Choose strategy based on risk tolerance and rollback requirements.

*   **Health Checks:**
    *   **Purpose:** Determine if an application instance/pod is healthy and able to serve traffic.
    *   **Use Case:** Used by Load Balancers and Managed Instance Groups to direct traffic away from unhealthy instances and trigger auto-healing (restarting/replacing instances). GKE uses Readiness and Liveness probes.

*   **Disaster Recovery (DR) Patterns:** (See Section 1 - RTO/RPO)
    *   **Backup and Restore:** Simplest, highest RTO/RPO. (Cold data, non-critical)
    *   **Pilot Light:** Minimal resources running in DR region, data replicated. (Lower RTO/RPO than backup/restore)
    *   **Warm Standby:** Scaled-down replica running in DR region, data replicated. (Even lower RTO/RPO)
    *   **Hot Standby (Active/Active):** Full application running in multiple regions, traffic managed globally. (Lowest RTO/RPO, highest cost/complexity)

*   **SRE Concepts:**
    *   **SLOs (Service Level Objectives):** Target values for service reliability (e.g., 99.9% availability, <100ms latency).
    *   **Error Budgets:** The amount of acceptable downtime/errors based on the SLO.
    *   **Monitoring:** Measure SLIs (Service Level Indicators) like latency, throughput, error rate, availability.
    *   **Chaos Engineering:** Experimentation on a system to build confidence in its resilience by injecting failures.
    *   **Use Case:** Drive operational practices, balance reliability vs. innovation, proactively test system resilience.

*   **Troubleshooting Tools:**
    *   **Cloud Debugger:** Inspect the state of a running application in production without stopping it.
    *   **Cloud Profiler/Trace:** Identify performance bottlenecks.
    *   **Cloud Logging/Error Reporting:** Analyze logs and errors.

---

**General Exam Tips:**

*   **Read Carefully:** Pay close attention to keywords in the questions and case studies (e.g., "minimize downtime," "global," "real-time," "cost-effective," "highly available," "compliance," "serverless").
*   **Scenario-Based Thinking:** For case study questions, refer back to the business and technical requirements. The "best" solution directly addresses the constraints and goals in the scenario.
*   **Trade-offs:** Understand the pros and cons of different services (e.g., managed vs. self-managed, cost vs. performance vs. complexity).
*   **Eliminate Incorrect Options:** Often, you can eliminate options that clearly don't meet a key requirement.
*   **Focus on Managed Services:** Google Cloud generally favors its managed services over running everything on Compute Engine VMs.
*   **IAM and Networking are Crucial:** Expect many questions on how to secure and connect resources.
*   **Practice:** Use the GCP Free Tier, Qwiklabs, and the official practice exams.

Good luck with your studies and the exam!
```