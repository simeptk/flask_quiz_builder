# Google Professional Cloud Architect Exam - Sample Case Studies Questions

**Prepared by:** Your Name/Team (Simulated Persona: GCP Cloud Architect preparing for the exam)

**Date:** [Insert Date]

**Purpose:** This document provides sample questions based on the official Google Cloud Professional Cloud Architect exam case studies. These questions are designed to test your ability to apply Google Cloud concepts to realistic business and technical scenarios. This section contains only the questions for self-assessment.

**Disclaimer:** These are sample questions created for study purposes based on publicly available case study information and common exam topics. They are not actual exam questions. Always consult the official Google Cloud documentation, hands-on labs, and recommended training resources.

---

## Case Study: EHR Healthcare - Questions

**Company Overview:** EHR Healthcare provides electronic health record software as a service. They are experiencing rapid growth and need to scale, improve DR, implement continuous deployment, reduce latency, maintain compliance, and decrease admin costs. Their existing environment is in colocation facilities with web/containerized apps on Kubernetes, data in MySQL, MS SQL Server, Redis, MongoDB, and legacy on-prem integrations.

1.  EHR Healthcare needs to achieve a minimum 99.9% availability for their customer-facing applications running on Kubernetes. They are currently in colocation and migrating to Google Cloud.

    Which Google Cloud architecture should they implement to meet this availability requirement for their containerized applications?

    a) Deploy the Kubernetes cluster in a single zone within a region.
    b) Deploy the Kubernetes cluster across multiple zones within a single region.
    c) Deploy the Kubernetes cluster across multiple regions.
    d) Deploy the Kubernetes cluster on Compute Engine VMs in a single zone.

2.  EHR Healthcare needs to provide centralized visibility and proactive action on system performance and usage across their applications, including containerized services and databases. Their current monitoring is via open-source tools and ignored alerts.

    Which Google Cloud service should they use for comprehensive monitoring, logging, and alerting?

    a) Cloud Logging and Cloud Monitoring
    b) Security Command Center
    c) Data Loss Prevention (DLP)
    d) BigQuery

3.  EHR Healthcare has legacy file- and API-based integrations on-premises that need to connect securely and with high performance to their new Google Cloud environment. These systems will remain on-premises for several years.

    Which Google Cloud connectivity option should they choose for this hybrid environment?

    a) IPsec VPN over the public internet
    b) Direct Peering
    c) Cloud Interconnect (Dedicated or Partner)
    d) Establish a public IP for on-prem systems and connect over the internet.

4.  EHR Healthcare's data is stored in various databases, including relational (MySQL, MS SQL Server) and NoSQL (Redis, MongoDB). They need to migrate this data to Google Cloud.

    Which Google Cloud services are appropriate targets for these databases, prioritizing managed services where possible?

    a) MySQL -> Cloud SQL for MySQL; MS SQL Server -> Compute Engine with SQL Server; Redis -> Memorystore for Redis; MongoDB -> MongoDB Atlas on GCP or self-hosted on Compute Engine/GKE.
    b) Migrate all databases to BigQuery.
    c) MySQL, MS SQL Server -> Cloud Spanner; Redis, MongoDB -> Cloud Firestore.
    d) Migrate all databases to Compute Engine VMs with the original database software installed.

5.  EHR Healthcare needs to dynamically scale and provision new environments rapidly due to exponential growth.

    Which Google Cloud services and practices are key to achieving dynamic scaling and rapid provisioning for their containerized applications?

    a) Manual scaling of Compute Engine VMs and shell scripts for provisioning.
    b) Managed Instance Groups (MIGs) with autoscaling and Deployment Manager templates.
    c) Google Kubernetes Engine (GKE) with Cluster Autoscaler and Horizontal Pod Autoscaler (HPA), combined with Infrastructure as Code (e.g., Terraform, Deployment Manager).
    d) App Engine Standard with traffic splitting.

6.  Maintaining regulatory compliance is critical for EHR Healthcare. They handle sensitive patient data.

    Which Google Cloud security and compliance capabilities are essential considerations for handling Electronic Health Records (EHR) data?

    a) Using default Google-managed encryption, basic IAM roles, and public internet connectivity.
    b) Implementing fine-grained IAM policies, using Customer-Managed Encryption Keys (CMEK) for sensitive data storage, enabling Cloud Audit Logs, and potentially using VPC Service Controls.
    c) Relying solely on network firewalls and VPNs.
    d) Storing all data in Compute Engine Persistent Disks encrypted with default keys.

7.  EHR Healthcare wants to decrease infrastructure administration costs and reduce the burden of managing disparate systems.

    Which approach using Google Cloud services aligns with this goal?

    a) Lift-and-shift all applications to Compute Engine VMs and manage them manually.
    b) Leverage managed services like GKE, Cloud SQL, Memorystore, and Cloud Operations, and automate infrastructure provisioning with IaC.
    c) Continue using disparate open-source tools for monitoring and management.
    d) Deploy all applications on App Engine Flex with manual scaling.

---

### Case Study: Helicopter Racing League (HRL) - Questions

**Company Overview:** HRL streams helicopter races globally with live telemetry and predictions. They want to migrate to GCP, use managed AI/ML, reduce viewer latency in emerging markets, increase predictions, and enhance global availability/quality. Existing tech uses VMs for encoding/transcoding/predictions and object storage on another cloud.

8.  HRL needs to reduce viewer latency for their video streams, especially in emerging markets.

    Which Google Cloud service should they use to cache and serve video content closer to their global audience?

    a) Cloud Storage (Standard)
    b) Cloud CDN
    c) Regional External HTTP(S) Load Balancer
    d) Transfer Appliance

9.  HRL performs video encoding and transcoding on VMs. They want to increase performance and manage this process efficiently on Google Cloud.

    Which Google Cloud service is designed for large-scale video processing and transcoding?

    a) Compute Engine VMs with custom scripts
    b) Dataproc
    c) Transcoder API
    d) Cloud Functions

10. HRL wants to increase their predictive capabilities during and before races, incorporating various data points like race results, mechanical failures, and crowd sentiment. They want to move their TensorFlow prediction workloads to Google Cloud.

    Which Google Cloud services are suitable for building, training, and deploying their predictive models at scale?

    a) Compute Engine VMs with manually installed TensorFlow
    b) AI Platform (now Vertex AI)
    c) Cloud Functions
    d) BigQuery ML

11. HRL generates significant live telemetry data during races that needs real-time processing for predictions and insights. They also need a data mart for processing large volumes of historical race data.

    Which combination of Google Cloud services is best for handling the real-time telemetry stream and the large-scale data mart?

    a) Cloud Storage for streaming, Cloud SQL for data mart.
    b) Cloud Pub/Sub -> Dataflow (Streaming) for real-time, BigQuery for data mart.
    c) Cloud Functions for streaming, Cloud Bigtable for data mart.
    d) Compute Engine for streaming, Cloud Storage for data mart.

12. HRL wants to enhance global availability and quality of their broadcasts. Their current mission-critical applications run on another public cloud.

    Which Google Cloud service is essential for distributing traffic globally to backend services hosting their streaming platform?

    a) Internal Load Balancing
    b) Network Load Balancing
    c) External HTTP(S) Load Balancing
    d) TCP Proxy Load Balancing

13. HRL needs to create a data mart to enable processing of large volumes of historical race data for analysis and trend prediction.

    Which Google Cloud service is best suited as a scalable data warehouse for this purpose?

    a) Cloud SQL
    b) Cloud Spanner
    c) Cloud Bigtable
    d) BigQuery

14. HRL wants to expose their predictive models to partners via APIs. They need a flexible and scalable platform for API management.

    Which Google Cloud service is suitable for managing, securing, and publishing APIs?

    a) Cloud Functions
    b) Cloud Endpoints or Apigee
    c) Cloud Pub/Sub
    d) Service Directory

---

### Case Study: Mountkirk Games - Questions

**Company Overview:** Mountkirk Games develops online multiplayer mobile games. They are expanding platforms/regions, prioritizing low latency and dynamic scaling. New FPS game requires global leaderboard (real-time, strong consistency) and GPU rendering. Existing tech is mostly lift-and-shift VMs, moving to GKE, Global LB, multi-region Spanner.

15. Mountkirk Games is building a new FPS game requiring hundreds of simultaneous players in geo-specific digital arenas with minimal latency. They plan to deploy the backend on GKE.

    Which Google Cloud Load Balancer should they use to route players to the closest regional game arenas running on GKE?

    a) Regional Internal HTTP(S) Load Balancer
    b) Global External HTTP(S) Load Balancer
    c) Regional Network Load Balancer
    d) Global External TCP Proxy Load Balancer

16. The new FPS game requires a real-time global leaderboard that displays top players across every active arena and needs strong consistency.

    Which Google Cloud database service is the best fit for this global, strongly consistent, high-throughput leaderboard?

    a) Cloud SQL
    b) Cloud Spanner
    c) Cloud Firestore
    d) Cloud Bigtable

17. Mountkirk Games needs to dynamically scale their game backend on GKE based on game activity (number of active players/games).

    Which GKE features are essential for achieving dynamic scaling of their application pods and underlying infrastructure?

    a) Horizontal Pod Autoscaler (HPA) and Cluster Autoscaler
    b) Vertical Pod Autoscaler (VPA) and Node Auto-provisioning
    c) Manual scaling of Deployments and fixed-size node pools
    d) PodDisruptionBudgets (PDBs) and DaemonSets

18. Mountkirk Games needs to store game activity logs in structured files for future analysis. The volume of logs is expected to be very high.

    Which Google Cloud service is a scalable and cost-effective solution for storing these large volumes of semi-structured log data?

    a) Cloud SQL
    b) Cloud Storage
    c) Cloud Bigtable
    d) Persistent Disks

19. The new game requires server-side GPU processing for rendering graphics for multi-platform support.

    How can Mountkirk Games provision and utilize GPUs within their GKE cluster?

    a) GPUs are automatically available on all GKE node pools.
    b) Configure GKE node pools to use machine types with attached GPUs.
    c) Run a separate cluster of Compute Engine VMs with GPUs and connect to GKE.
    d) GPUs are not supported on GKE.

20. Mountkirk Games wants to maintain most permissions and network policies at a higher level than individual projects for their new games, which are in isolated projects nested below a folder.

    Which Google Cloud resource hierarchy feature enables applying policies consistently across multiple projects?

    a) Labels
    b) Folders
    c) Organizations
    d) Projects

21. Mountkirk Games needs to rapidly iterate on game features, including deploying bug fixes and new functionality frequently.

    Which Google Cloud services are key components of a CI/CD pipeline to support rapid iteration and deployment to GKE?

    a) Cloud Storage, Cloud Functions, Cloud Tasks
    b) Cloud Build, Artifact Registry, Cloud Deploy, GKE
    c) Compute Engine, SSH scripts, manual deployments
    d) BigQuery, Dataflow, Dataproc

---

### Case Study: TerramEarth - Questions

**Company Overview:** TerramEarth manufactures heavy equipment, managing a global fleet with telemetry data. They need to predict malfunctions, optimize costs, improve dev workflow speed/reliability, allow secure remote dev, create API platform for partners, and modernize CI/CD. Existing tech includes GCP presence, private data centers with interconnects (legacy systems), web frontend in GCP.

22. TerramEarth needs to predict and detect vehicle malfunction based on telemetry data. Critical data is real-time, the rest is uploaded daily. They need to process and analyze this data at scale.

    Which Google Cloud services are appropriate for ingesting, processing, and analyzing both the streaming and batch telemetry data?

    a) Real-time: Cloud Functions -> Cloud SQL; Batch: Cloud Storage -> Dataproc.
    b) Real-time: Cloud Pub/Sub -> Dataflow (Streaming) -> BigQuery; Batch: Cloud Storage -> BigQuery or Dataproc.
    c) Real-time: Compute Engine -> Cloud Bigtable; Batch: Transfer Appliance -> Cloud Storage.
    d) Real-time: Cloud IoT Core (deprecated) -> Cloud Functions; Batch: SFTP to Compute Engine.

23. TerramEarth needs to create a new abstraction layer for HTTP API access to their legacy systems hosted in private data centers, enabling a gradual move to the cloud.

    Which Google Cloud services can help build and manage APIs that connect to on-premises backend systems via Cloud Interconnect?

    a) Cloud Functions and Cloud Tasks
    b) App Engine and Cloud Scheduler
    c) Cloud Endpoints or Apigee, combined with Serverless VPC Access or Hybrid Connectivity.
    d) Cloud Pub/Sub and Dataflow.

24. TerramEarth wants to modernize their CI/CD pipelines to allow developers to deploy container-based workloads in highly scalable environments.

    Which Google Cloud services should form the basis of their modern CI/CD pipeline for containerized applications?

    a) Jenkins on Compute Engine, Docker Hub, manual `kubectl` deployments.
    b) Cloud Build, Artifact Registry, Cloud Deploy, GKE or Cloud Run.
    c) Cloud Functions, Cloud Tasks, Cloud Scheduler.
    d) App Engine Standard, Cloud Source Repositories.

25. TerramEarth needs to allow remote developers to be productive without compromising code or data security.

    Which Google Cloud security and identity services can help enable secure remote development access?

    a) Granting broad `editor` roles to developers.
    b) Using Identity-Aware Proxy (IAP) or Context-Aware Access (BeyondCorp) to control access to development environments and tools based on user identity and context.
    c) Opening firewall rules to allow access from any IP address.
    d) Relying solely on VPNs to the corporate network.

26. TerramEarth needs to use cloud-native solutions for keys and secrets management and optimize for identity-based access.

    Which Google Cloud services are designed for secure secrets management and fine-grained identity and access control?

    a) Cloud Storage and Service Accounts
    b) Secret Manager and Cloud KMS for secrets/keys; IAM for identity-based access.
    c) Environment variables and API keys.
    d) Cloud Audit Logs and Security Command Center.

27. TerramEarth wants to improve and standardize tools necessary for application and network monitoring and troubleshooting across their hybrid environment.

    Which Google Cloud service suite provides integrated monitoring, logging, tracing, and error reporting capabilities?

    a) Google Analytics
    b) Security Command Center
    c) Cloud Operations (formerly Stackdriver)
    d) BigQuery

28. TerramEarth needs to create a self-service portal for internal and partner developers to create new projects, request resources for data analytics jobs, and centrally manage access to the API endpoints.

    Which Google Cloud tools or services can facilitate building this self-service capability?

    a) Manually processing requests via email.
    b) Cloud Deployment Manager or Terraform for provisioning, Service Catalog for product offerings, custom application using Google Cloud APIs (e.g., IAM, Resource Manager).
    c) Cloud Shell scripts shared via email.
    d) Google Forms and manual execution.

---

## Google Professional Cloud Architect Exam Sample Questions (Case Studies - Answers and Explanations)

**Purpose:** This section provides the answers and explanations for the sample questions based on the case studies. Use this section to check your work and deepen your understanding of the concepts.

---

### Case Study: EHR Healthcare - Answers and Explanations

1.  **Answer:** b) Deploy the Kubernetes cluster across multiple zones within a single region.
    *Explanation: To achieve 99.9% availability within a region, deploying across multiple zones is necessary to protect against single-zone failures. Deploying across multiple regions (c) would provide even higher availability (e.g., 99.99%) for disaster recovery, but 99.9% can typically be met regionally with multi-zone deployment and robust application design. Single zone (a) is a single point of failure. Running on single VMs (d) doesn't leverage Kubernetes' built-in availability features.*

2.  **Answer:** a) Cloud Logging and Cloud Monitoring
    *Explanation: Cloud Logging is the centralized service for collecting and analyzing logs. Cloud Monitoring provides metrics collection, dashboards, and alerting based on performance and usage data from various Google Cloud services, including GKE and databases. Error Reporting complements this for application errors, and Cloud Trace for distributed tracing.*

3.  **Answer:** c) Cloud Interconnect (Dedicated or Partner)
    *Explanation: Cloud Interconnect provides a dedicated, high-bandwidth, low-latency connection between on-premises and Google Cloud, bypassing the public internet. This is suitable for high-performance, secure connections required for ongoing hybrid operations with legacy systems. IPsec VPN (a) is generally lower bandwidth and higher latency.*

4.  **Answer:** a) MySQL -> Cloud SQL for MySQL; MS SQL Server -> Compute Engine with SQL Server; Redis -> Memorystore for Redis; MongoDB -> MongoDB Atlas on GCP or self-hosted on Compute Engine/GKE.
    *Explanation: Cloud SQL is the managed relational database service for MySQL and PostgreSQL. While Cloud SQL for SQL Server exists, lift-and-shift often involves running SQL Server on a Compute Engine VM initially. Memorystore is the managed Redis service. MongoDB is not offered as a native managed service by Google, so running it on GKE/Compute Engine or using a partner solution like MongoDB Atlas on GCP are common approaches.*

5.  **Answer:** c) Google Kubernetes Engine (GKE) with Cluster Autoscaler and Horizontal Pod Autoscaler (HPA), combined with Infrastructure as Code (e.g., Terraform, Deployment Manager).
    *Explanation: GKE provides the orchestration for containers. Cluster Autoscaler dynamically adjusts the number of nodes, and HPA adjusts the number of pods based on load, providing dynamic scaling. IaC tools enable rapid and repeatable provisioning of the GKE clusters and related infrastructure.*

6.  **Answer:** b) Implementing fine-grained IAM policies, using Customer-Managed Encryption Keys (CMEK) for sensitive data storage, enabling Cloud Audit Logs, and potentially using VPC Service Controls.
    *Explanation: Handling sensitive health data requires strict controls. Fine-grained IAM enforces least privilege. CMEK provides organizational control over encryption keys. Cloud Audit Logs provide an immutable record of access. VPC Service Controls can create security perimeters to prevent unauthorized data movement.*

7.  **Answer:** b) Leverage managed services like GKE, Cloud SQL, Memorystore, and Cloud Operations, and automate infrastructure provisioning with IaC.
    *Explanation: Managed services offload operational overhead (patching, backups, scaling infrastructure). Automating provisioning with IaC reduces manual effort and potential for misconfiguration, directly addressing the goal of decreasing administration costs and improving consistency.*

---

### Case Study: Helicopter Racing League (HRL) - Answers and Explanations

8.  **Answer:** b) Cloud CDN
    *Explanation: Cloud CDN (Content Delivery Network) caches static and dynamic content at edge locations globally, serving it closer to viewers and significantly reducing latency and improving the streaming experience.*

9.  **Answer:** c) Transcoder API
    *Explanation: The Transcoder API is a managed service specifically designed for video transcoding at scale. It's more efficient and easier to manage than running custom scripts on individual VMs for this purpose.*

10. **Answer:** b) AI Platform (now Vertex AI)
    *Explanation: Vertex AI (formerly AI Platform) is Google Cloud's managed machine learning platform. It provides tools and services for building, training, and deploying ML models, including those built with TensorFlow, at scale without managing underlying infrastructure.*

11. **Answer:** b) Cloud Pub/Sub -> Dataflow (Streaming) for real-time, BigQuery for data mart.
    *Explanation: Cloud Pub/Sub is a scalable messaging bus for ingesting high-velocity streams. Dataflow (Streaming) is ideal for real-time processing and analysis of that stream. BigQuery is a petabyte-scale data warehouse perfect for storing and querying large volumes of historical data for the data mart.*

12. **Answer:** c) External HTTP(S) Load Balancing
    *Explanation: External HTTP(S) Load Balancing is a global service that provides a single IP address and distributes HTTP/HTTPS traffic to backends across multiple regions, directing users to the closest healthy backend to minimize latency and enhance global availability.*

13. **Answer:** d) BigQuery
    *Explanation: BigQuery is Google Cloud's fully managed, serverless data warehouse, optimized for storing and analyzing massive datasets using SQL, making it the ideal choice for a data mart processing large volumes of race data.*

14. **Answer:** b) Cloud Endpoints or Apigee
    *Explanation: Cloud Endpoints is suitable for managing APIs built on Google Cloud. Apigee is a more comprehensive, full-lifecycle API management platform. Both can be used to publish, secure, and manage APIs exposed to partners.*

---

### Case Study: Mountkirk Games - Answers and Explanations

15. **Answer:** b) Global External HTTP(S) Load Balancer
    *Explanation: For a global game with players connecting from anywhere, a Global External HTTP(S) Load Balancer provides a single entry point and routes users to the closest regional backend (GKE cluster) based on proximity and health, minimizing latency.*

16. **Answer:** b) Cloud Spanner
    *Explanation: Cloud Spanner is a globally distributed, strongly consistent, and highly available relational database. It's uniquely suited for a real-time global leaderboard that requires high throughput, low latency reads/writes, and guaranteed consistency across regions.*

17. **Answer:** a) Horizontal Pod Autoscaler (HPA) and Cluster Autoscaler
    *Explanation: HPA automatically scales the number of pods in a Deployment or StatefulSet based on metrics like CPU/memory usage or custom metrics derived from game activity. Cluster Autoscaler automatically adjusts the number of nodes in the GKE cluster's node pools to accommodate the scaling pods.*

18. **Answer:** b) Cloud Storage
    *Explanation: Cloud Storage is a highly scalable, durable, and cost-effective object storage service suitable for storing large volumes of structured or semi-structured data like game activity logs in files, which can then be processed by services like BigQuery, Dataproc, or Dataflow.*

19. **Answer:** b) Configure GKE node pools to use machine types with attached GPUs.
    *Explanation: GKE allows you to create node pools using Compute Engine machine types that have GPUs attached. You can then configure your application pods to request GPU resources, and Kubernetes will schedule them onto these GPU-enabled nodes.*

20. **Answer:** b) Folders
    *Explanation: Folders are used in the Google Cloud resource hierarchy to group projects. Applying IAM policies and Organization Policies at the Folder level ensures that these policies are inherited by all projects within that folder, providing consistent governance and control.*

21. **Answer:** b) Cloud Build, Artifact Registry, Cloud Deploy, GKE
    *Explanation: This represents a typical cloud-native CI/CD flow: Cloud Build automates builds and tests, Artifact Registry stores container images, Cloud Deploy manages the release process and deploys to target environments like GKE.*

---

### Case Study: TerramEarth - Answers and Explanations

22. **Answer:** b) Real-time: Cloud Pub/Sub -> Dataflow (Streaming) -> BigQuery; Batch: Cloud Storage -> BigQuery or Dataproc.
    *Explanation: Cloud Pub/Sub is best for ingesting high-velocity streaming data. Dataflow (Streaming) is suitable for real-time processing. BigQuery is a scalable data warehouse for real-time analysis and the batch data mart. For batch data uploaded daily, Cloud Storage is the landing zone, and BigQuery or Dataproc can process it.*

23. **Answer:** c) Cloud Endpoints or Apigee, combined with Serverless VPC Access or Hybrid Connectivity.
    *Explanation: Cloud Endpoints or Apigee are used for API management. To connect these APIs to on-premises backends over the private network, you need Serverless VPC Access (for serverless API implementations like Cloud Functions/Run) or configure the API gateway/proxy (e.g., on GKE/Compute Engine) to use the existing Cloud Interconnect via the VPC network.*

24. **Answer:** b) Cloud Build, Artifact Registry, Cloud Deploy, GKE or Cloud Run.
    *Explanation: Cloud Build automates the build process (including container images). Artifact Registry is the managed container registry. Cloud Deploy orchestrates the continuous delivery process. GKE or Cloud Run are scalable environments for deploying containerized applications.*

25. **Answer:** b) Using Identity-Aware Proxy (IAP) or Context-Aware Access (BeyondCorp) to control access to development environments and tools based on user identity and context.
    *Explanation: IAP and Context-Aware Access allow you to control access to applications and VMs based on user identity and the context of the request (device, location, etc.), providing a more secure alternative to VPNs or broad firewall rules, enabling secure remote access without exposing resources directly to the public internet.*

26. **Answer:** b) Secret Manager and Cloud KMS for secrets/keys; IAM for identity-based access.
    *Explanation: Secret Manager is the recommended service for storing and managing secrets like API keys and passwords. Cloud KMS is for managing cryptographic keys. IAM is the foundation for identity-based access control across all Google Cloud resources.*

27. **Answer:** c) Cloud Operations (formerly Stackdriver)
    *Explanation: Cloud Operations is the integrated suite of services (including Cloud Monitoring, Cloud Logging, Cloud Trace, Error Reporting, Cloud Profiler) that provides comprehensive observability across Google Cloud and hybrid environments, allowing for standardized monitoring and troubleshooting.*

28. **Answer:** b) Cloud Deployment Manager or Terraform for provisioning, Service Catalog for product offerings, custom application using Google Cloud APIs (e.g., IAM, Resource Manager).
    *Explanation: IaC tools (Deployment Manager, Terraform) automate resource provisioning. Service Catalog allows you to curate and offer approved solutions (like pre-configured projects or data analytics environments) to users via a portal. A custom application can be built using Google Cloud APIs to tie these together and provide a user-friendly self-service interface for managing projects, resources, and API access.*

---

### Conclusion

These questions, framed within the context of the case studies, require you to think critically about applying Google Cloud services to solve realistic business and technical challenges. This is the core skill tested in the Professional Cloud Architect exam.

Continue to practice with these scenarios, explore the services mentioned in the answers in more depth, and consider how different solutions compare in terms of cost, performance, complexity, and reliability.

Good luck with your studies!
