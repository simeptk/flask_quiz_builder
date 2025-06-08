# Google Cloud Professional Architect Exam Patterns – Revised

This document outlines high-level architectures and best practices for four Professional Cloud Architect case studies. It is intended to help you understand the trade-offs of various design decisions and prepare for the exam by linking business requirements with robust, optimized cloud solutions.

---

## Overview of the Case Studies

Below are four case studies that illustrate how to design scalable, secure, and cost-effective solutions for diverse business scenarios on Google Cloud Platform (GCP).

---

### 1. EHR Healthcare

**Company Overview:**  
EHR Healthcare delivers electronic health record software as a service (SaaS) to hospitals, insurance providers, and multi-national offices.

**Business Requirements:**
- **Rapid Onboarding & High Availability:** Must support quick integration of new insurance providers with a minimum of 99.9% uptime.
- **Security & Compliance:** Secure remote access, integration with on-premises legacy systems, and adherence to regulatory standards.
- **Cost & Performance Optimization:** Efficiently process and store large datasets while managing operational expenses.

**Proposed Architecture:**
- **Hybrid Connectivity:** Secure Cloud Interconnect between on-premises systems and GCP.
- **Container Management:** Use GKE for container orchestration, ensuring dynamic scaling and high availability.
- **Managed Databases & Data Platform:** Leverage Cloud SQL, Memorystore, and BigQuery for efficient data handling.
- **API Integration:** Use Apigee or Cloud Endpoints to abstract legacy integrations.
- **Monitoring & Operations:** Employ Cloud Monitoring, Cloud Logging, Cloud Trace, and DevOps tools (Cloud Build/Deploy) for centralized operations.

**Key Points:**
- Secure connectivity with a multi-region VPC
- Managed services to reduce administrative overhead
- Use Cloud Armor, IAM, and Secret Manager for security and compliance

---

### 2. Helicopter Racing League (HRL)

**Company Overview:**  
HRL is a global sports league streaming helicopter races with live telemetry and real-time predictions.

**Business Requirements:**
- **Global Content Delivery:** Ensure low-latency video streaming and real-time analytics.
- **High-Performance Processing:** Efficiently handle streaming telemetry and video transcoding.
- **Operational Efficiency:** Simplify deployment and management across regions.

**Proposed Architecture:**
- **Global Load Balancing & CDN:** Route traffic efficiently with Cloud CDN and Global HTTP(S) Load Balancers.
- **Compute Options:** Use Compute Engine for video processing tasks (with GPU support) and consider GKE for containerized workloads.
- **Real-Time Data Pipeline:** Implement Pub/Sub for telemetry ingestion and Dataflow pipelines for processing.
- **ML & Analytics:** Deploy Vertex AI for prediction models and BigQuery for data analysis.

**Key Points:**
- Low latency delivery through global load balancing and optimized network routes.
- Scalability through managed compute, serverless processing, and autoscaling policies.
- Robust monitoring to track performance metrics in real time.

---

### 3. Mountkirk Games

**Company Overview:**  
Mountkirk Games develops online, multiplayer mobile games and is expanding its portfolio to new platforms.

**Business Requirements:**
- **Dynamic Scaling:** Support rapid scaling based on real-time game activity.
- **Low Latency:** Maintain responsive gameplay and global leaderboard updates.
- **Cost Efficiency:** Optimize resource use, especially for GPU-intensive rendering.

**Proposed Architecture:**
- **Containerized Game Servers:** Deploy game servers on multi-region GKE clusters.
- **Global Leaderboard:** Use Cloud Spanner to maintain real-time, globally distributed leaderboards.
- **Scalable Data Analytics:** Ingest and analyze game logs using Pub/Sub, Dataflow, and BigQuery.
- **GPU Support:** Utilize GKE Node Pools with GPUs for performance demands.

**Key Points:**
- Leverage horizontal and cluster autoscaling to manage resources efficiently.
- Integrate managed services to streamline operations and reduce overhead.
- Implement strict monitoring and logging to maintain game performance and reliability.

---

### 4. TerramEarth

**Company Overview:**  
TerramEarth manufactures heavy equipment and focuses on predictive maintenance and enhanced customer/dealer interactions.

**Business Requirements:**
- **Data-Driven Decisions:** Ingest massive telemetry data for predictive maintenance.
- **Cost-Aware Scalability:** Optimize operations to handle seasonal workload fluctuations.
- **Developer Enablement:** Provide secure, self-service environments for both internal and partner developers.

**Proposed Architecture:**
- **Hybrid Data Ingestion:** Use Pub/Sub and Dataflow for processing both streaming and batch telemetry.
- **Scalable Data Warehouse:** Utilize BigQuery as the central repository for analysis.
- **API Platform:** Create an abstraction layer using Apigee or Cloud Endpoints for secure API access.
- **Developer Tools:** Enhance CI/CD pipelines with Cloud Build, Artifact Registry, and Terraform/Deployment Manager to automate provisioning.
- **Enhanced Security:** Use IAM, VPC Service Controls, IAP, Cloud KMS, and Secret Manager to safeguard resources.

**Key Points:**
- Focus on flexible resource provisioning to support seasonality.
- Centralize security controls to protect sensitive data and maintain compliance.
- Automate operations to boost developer productivity and streamline deployments.

---

## Key Exam Topics and How They Apply

### Logging & Monitoring
- **Objective:** Gain full visibility into system performance and operational health.
- **Strategy:**  
  - Use Cloud Monitoring and Cloud Logging to create dashboards, track metrics, and set alert policies.
  - Incorporate Cloud Trace and Profiler for performance analysis.
  
**Examples:**
- **EHR Healthcare:** Implement centralized dashboards for Kubernetes and database performance.
- **HRL:** Monitor the reliability of transcoding and real-time pipelines.
- **Mountkirk Games:** Track resource utilization and latency to maintain gameplay quality.
- **TerramEarth:** Use logs to troubleshoot API integrations and data processing failures.

### Container Orchestration (GKE)
- **Objective:** Efficiently deploy and manage containerized applications.
- **Strategy:**  
  - Choose between GKE Standard and Autopilot based on control versus management needs.
  - Use autoscaling features (HPA, Cluster Autoscaler) for resource optimization.
  
**Examples:**
- **EHR Healthcare & TerramEarth:** Migrate legacy workloads to GKE to reduce administration.
- **Mountkirk Games:** Leverage GKE to support dynamic scaling and container-based game servers.

### Compute & Serverless Options
- **Objective:** Select the appropriate compute service based on workload characteristics.
- **Strategy:**  
  - Use Compute Engine for heavy-lifting or legacy migrations.
  - Employ Cloud Functions and Cloud Run for event-driven or containerized microservices.
  
**Examples:**
- **HRL:** Use GPU-enabled Compute Engine instances for transcoding.
- **TerramEarth:** Implement serverless options to reduce operational cost and scale automatically.

### Networking & Security
- **Objective:** Build secure, reliable, low-latency networks.
- **Strategy:**  
  - Design multi-region VPCs with proper firewall and access controls.
  - Implement Cloud Interconnect, VPN, and VPC Service Controls for hybrid connectivity.
  
**Examples:**
- **EHR Healthcare:** Secure on-premises connectivity and API access.
- **TerramEarth:** Use VPC Service Controls and IAP for a secure development environment.

### Automation & Cost Optimization
- **Objective:** Automate deployment and optimize expenditures.
- **Strategy:**  
  - Use CI/CD pipelines with Cloud Build/Deploy.
  - Manage infrastructure as code with Terraform or Deployment Manager.
  - Focus on autoscaling and managed services to align costs with demand.
  
**Examples:**
- **Mountkirk Games:** Automate game server deployments while ensuring cost-effective GPU usage.
- **TerramEarth:** Use cost management tools alongside automated provisioning to adapt to changing workload patterns.

### Reliability & Compliance
- **Objective:** Ensure high availability and adhere to regulatory requirements.
- **Strategy:**  
  - Deploy across multiple zones and regions; implement disaster recovery strategies.
  - Use identity management, encryption, and audit tools to maintain compliance.
  
**Examples:**
- **EHR Healthcare:** Use fully managed services and robust DR planning to meet HIPAA standards.
- **TerramEarth:** Ensure all access and data handling meet industry-specific security guidelines.

---

## Conclusion

This revised document rephrases and consolidates your exam preparation topics while addressing warnings by ensuring clarity and removing redundancy. It presents a concise yet comprehensive look at the architectures and best practices needed to design effective solutions on GCP across varied business scenarios.

Good luck with your exam preparation!