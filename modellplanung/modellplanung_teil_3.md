# 🎯 BIM-Modellplanung: Vollständige Enterprise-Lösung

**Projekt**: BIM-Modellplanung Systematik  
**Datum**: 2025-10-09  
**Verantwortlich**: NikolayBorissovASTRA  
**Status**: ✅ Production-Ready

---

## 📊 Teil 3: Konzepte (Fortsetzung) - Produktionsreife Visualisierungen

### 3.4 Deployment-Sicht - Kubernetes Infrastructure (Fortsetzung)

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'fontSize':'14px'}}}%%
graph TB
    subgraph Internet["🌐 Internet"]
        USERS[👥 End Users<br/>Web Browsers]
    end
    
    subgraph CloudEdge["☁️ Cloud Edge - CDN & Security"]
        CDN[CloudFlare CDN<br/>📦 Static Assets<br/>🛡️ DDoS Protection]
        WAF[Web Application Firewall<br/>🔒 OWASP ModSecurity<br/>Rate Limiting]
        LB[Load Balancer<br/>⚖️ NGINX Ingress<br/>🔐 SSL/TLS Termination]
    end
    
    subgraph K8sCluster["☸️ Kubernetes Cluster - Production"]
        subgraph NSFrontend["Namespace: frontend"]
            FE_SVC[Service: frontend-svc<br/>ClusterIP]
            FE_HPA[HPA: 2-10 replicas<br/>CPU: 70% target]
            FE1[Pod: frontend-1<br/>React 18<br/>NGINX<br/>CPU: 0.5, Mem: 512Mi]
            FE2[Pod: frontend-2]
            FE3[Pod: frontend-3]
        end
        
        subgraph NSBackend["Namespace: backend"]
            API_SVC[Service: api-svc<br/>ClusterIP]
            API_HPA[HPA: 3-15 replicas<br/>CPU: 75% target]
            BE1[Pod: api-1<br/>FastAPI<br/>CPU: 1, Mem: 1Gi]
            BE2[Pod: api-2]
            BE3[Pod: api-3]
            
            AUTH_SVC[Service: auth-svc]
            AUTH1[Pod: auth-1<br/>JWT Service]
            AUTH2[Pod: auth-2]
        end
        
        subgraph NSWorkers["Namespace: workers"]
            QUEUE_SVC[Service: queue-svc]
            W1[Pod: worker-1<br/>Celery Worker<br/>CPU: 2, Mem: 2Gi]
            W2[Pod: worker-2]
            W3[Pod: worker-3]
        end
        
        subgraph NSServices["Namespace: services"]
            VAL_SVC[Service: validation-svc]
            VAL[Pod: validator<br/>IDS Engine<br/>CPU: 2, Mem: 4Gi]
            
            IFC_SVC[Service: ifc-svc]
            IFC[Pod: ifc-analyzer<br/>IfcOpenShell<br/>CPU: 4, Mem: 8Gi]
        end
        
        subgraph NSIngress["Ingress Controller"]
            INGRESS[NGINX Ingress<br/>🔀 Path-based Routing<br/>🔐 TLS 1.3]
        end
    end
    
    subgraph DataTier["💾 Data Tier - Persistent Storage"]
        subgraph DBCluster["PostgreSQL HA Cluster"]
            DB_PRIMARY[(🔴 Primary<br/>PostgreSQL 15<br/>Write: 1000 TPS<br/>SSD: 500GB)]
            DB_STANDBY[(🟡 Standby<br/>Sync Replication<br/>Auto-failover)]
            DB_READ1[(🟢 Replica 1<br/>Read-only)]
            DB_READ2[(🟢 Replica 2<br/>Read-only)]
        end
        
        subgraph RedisCluster["Redis Sentinel HA"]
            REDIS_M[(🔴 Master<br/>Redis 7<br/>Cache + Queue<br/>16GB RAM)]
            REDIS_S1[(🟢 Sentinel 1<br/>Auto-failover)]
            REDIS_S2[(🟢 Sentinel 2)]
        end
        
        subgraph ObjectStorage["Object Storage"]
            S3[📦 S3 Bucket<br/>modellplan-files<br/>Versioning: ON<br/>Encryption: AES-256]
        end
        
        subgraph PersistentVolumes["Persistent Volumes"]
            PV1[PV: postgres-data<br/>500GB SSD<br/>RWO]
            PV2[PV: redis-data<br/>50GB SSD<br/>RWO]
        end
    end
    
    subgraph Monitoring["📊 Observability Stack"]
        PROM[Prometheus<br/>📈 Metrics Collection<br/>Retention: 30d]
        ALERT[Alertmanager<br/>🚨 PagerDuty<br/>Slack Integration]
        GRAF[Grafana<br/>📊 Dashboards<br/>15 Panels]
        JAEGER[Jaeger<br/>🔍 Distributed Tracing<br/>APM]
        LOKI[Loki<br/>📝 Log Aggregation<br/>10GB/day]
    end
    
    subgraph External["🔌 External Services"]
        AAD[Azure AD<br/>🔐 SSO/OAuth2<br/>SAML 2.0]
        SENDGRID[SendGrid<br/>📧 Email Service<br/>10k/month]
        BIM360[BIM 360 API<br/>📐 CDE Integration<br/>Webhook Support]
    end
    
    subgraph BackupDR["💿 Backup & Disaster Recovery"]
        VELERO[Velero<br/>K8s Backup<br/>Daily Snapshots]
        PGBACKUP[pg_dump<br/>📦 Encrypted Backups<br/>Retention: 30d]
        S3BACKUP[S3 Backup<br/>Cross-Region Replication<br/>Frankfurt → Ireland]
        DR[🔄 DR Site<br/>Standby Cluster<br/>RPO: 15min<br/>RTO: 1h]
    end
    
    %% User Flow
    USERS -->|HTTPS :443| CDN
    CDN -->|HTTPS| WAF
    WAF -->|HTTPS| LB
    LB -->|HTTPS| INGRESS
    
    %% Ingress Routing
    INGRESS -->|"/"| FE_SVC
    INGRESS -->|"/api/*"| API_SVC
    INGRESS -->|"/auth/*"| AUTH_SVC
    
    %% Frontend
    FE_HPA -.->|scales| FE1
    FE_HPA -.->|scales| FE2
    FE_HPA -.->|scales| FE3
    FE_SVC --> FE1
    FE_SVC --> FE2
    FE_SVC --> FE3
    
    %% Backend
    API_HPA -.->|scales| BE1
    API_HPA -.->|scales| BE2
    API_HPA -.->|scales| BE3
    API_SVC --> BE1
    API_SVC --> BE2
    API_SVC --> BE3
    
    AUTH_SVC --> AUTH1
    AUTH_SVC --> AUTH2
    
    %% Workers
    QUEUE_SVC --> W1
    QUEUE_SVC --> W2
    QUEUE_SVC --> W3
    
    %% Services
    VAL_SVC --> VAL
    IFC_SVC --> IFC
    
    %% API to Services
    BE1 --> VAL_SVC
    BE1 --> IFC_SVC
    BE1 --> QUEUE_SVC
    BE2 --> VAL_SVC
    BE3 --> VAL_SVC
    
    %% Database Connections
    BE1 -->|Write| DB_PRIMARY
    BE1 -.->|Read| DB_READ1
    BE2 -->|Write| DB_PRIMARY
    BE2 -.->|Read| DB_READ2
    BE3 -->|Write| DB_PRIMARY
    W1 -->|Write| DB_PRIMARY
    
    DB_PRIMARY -.->|Sync Replication| DB_STANDBY
    DB_PRIMARY -.->|Async Replication| DB_READ1
    DB_PRIMARY -.->|Async Replication| DB_READ2
    
    %% Redis Connections
    BE1 --> REDIS_M
    BE2 --> REDIS_M
    W1 --> REDIS_M
    W2 --> REDIS_M
    
    REDIS_M -.->|Replication| REDIS_S1
    REDIS_M -.->|Replication| REDIS_S2
    
    %% Storage
    BE1 --> S3
    W1 --> S3
    VAL --> S3
    
    %% PV Claims
    DB_PRIMARY -.->|mounts| PV1
    REDIS_M -.->|mounts| PV2
    
    %% External Services
    AUTH1 -->|OAuth2| AAD
    W1 -->|SMTP| SENDGRID
    BE1 -->|REST| BIM360
    
    %% Monitoring
    BE1 -.->|metrics :9090| PROM
    BE2 -.->|metrics| PROM
    FE1 -.->|metrics| PROM
    W1 -.->|metrics| PROM
    VAL -.->|metrics| PROM
    
    PROM --> GRAF
    PROM --> ALERT
    
    BE1 -.->|traces| JAEGER
    BE1 -.->|logs| LOKI
    W1 -.->|logs| LOKI
    
    %% Backup
    DB_PRIMARY -.->|daily| PGBACKUP
    K8sCluster -.->|daily| VELERO
    S3 -.->|continuous| S3BACKUP
    
    PGBACKUP -.->|replicate| DR
    S3BACKUP -.->|replicate| DR
    
    %% Styling
    classDef internet fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef edge fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef k8s fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef monitor fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#ffe0b2,stroke:#e64a19,stroke-width:2px
    classDef backup fill:#e0f2f1,stroke:#00796b,stroke-width:2px
    
    class USERS internet
    class CDN,WAF,LB edge
    class NSFrontend,NSBackend,NSWorkers,NSServices,INGRESS,FE1,FE2,FE3,BE1,BE2,BE3,AUTH1,AUTH2,W1,W2,W3,VAL,IFC k8s
    class DBCluster,RedisCluster,DB_PRIMARY,DB_STANDBY,DB_READ1,DB_READ2,REDIS_M,REDIS_S1,REDIS_S2,S3,PV1,PV2 data
    class PROM,ALERT,GRAF,JAEGER,LOKI monitor
    class AAD,SENDGRID,BIM360 external
    class VELERO,PGBACKUP,S3BACKUP,DR backup
```

### 3.5 Sicherheits-Architektur (Defense in Depth)

```mermaid
%%{init: {'theme':'base'}}%%
graph TD
    subgraph Layer1["🛡️ Layer 1: Perimeter Security"]
        DDoS[DDoS Protection<br/>CloudFlare<br/>100 Gbps Mitigation]
        GEO[Geo-Blocking<br/>Allow: CH, DE, AT, FR<br/>Block: High-Risk Countries]
        RATE[Rate Limiting<br/>100 req/min per IP<br/>1000 req/min per User]
    end
    
    subgraph Layer2["🔐 Layer 2: Network Security"]
        WAF[Web Application Firewall<br/>OWASP Top 10<br/>SQL Injection Prevention<br/>XSS Protection]
        TLS[TLS 1.3 Only<br/>HSTS Enabled<br/>Perfect Forward Secrecy]
        VPN[VPN Gateway<br/>Admin Access Only<br/>WireGuard]
    end
    
    subgraph Layer3["🔑 Layer 3: Identity & Access"]
        MFA[Multi-Factor Auth<br/>TOTP Required<br/>SMS Backup]
        SSO[SSO Integration<br/>Azure AD<br/>SAML 2.0]
        RBAC[Role-Based Access Control<br/>15 Predefined Roles<br/>Least Privilege]
        JWT[JWT Tokens<br/>15min Expiry<br/>Refresh Token Rotation]
    end
    
    subgraph Layer4["🔒 Layer 4: Application Security"]
        CSRF[CSRF Protection<br/>Double Submit Cookie<br/>SameSite Strict]
        CORS[CORS Policy<br/>Whitelist Only<br/>Credentials Required]
        INPUT[Input Validation<br/>Pydantic Schema<br/>Sanitization]
        OUTPUT[Output Encoding<br/>XSS Prevention<br/>Content Security Policy]
    end
    
    subgraph Layer5["💾 Layer 5: Data Security"]
        ENC_TRANSIT[Encryption in Transit<br/>TLS 1.3<br/>AES-256-GCM]
        ENC_REST[Encryption at Rest<br/>PostgreSQL: pgcrypto<br/>S3: AES-256]
        SECRETS[Secret Management<br/>HashiCorp Vault<br/>Auto-Rotation]
        BACKUP_ENC[Encrypted Backups<br/>GPG Encryption<br/>Offsite Storage]
    end
    
    subgraph Layer6["👁️ Layer 6: Monitoring & Detection"]
        IDS[Intrusion Detection<br/>Falco<br/>Anomaly Detection]
        SIEM[SIEM Integration<br/>Splunk<br/>Real-time Alerts]
        AUDIT[Audit Logging<br/>Immutable Logs<br/>5 Year Retention]
        VULN[Vulnerability Scanning<br/>Trivy + Snyk<br/>Weekly Scans]
    end
    
    subgraph Layer7["🚨 Layer 7: Incident Response"]
        ALERT_SYS[Alert System<br/>PagerDuty<br/>24/7 On-Call]
        PLAYBOOK[Incident Playbooks<br/>15min Response Time<br/>Automated Containment]
        FORENSICS[Forensic Logging<br/>Tamper-Proof<br/>Chain of Custody]
        RECOVERY[Disaster Recovery<br/>RTO: 1h<br/>RPO: 15min]
    end
    
    %% Data Flow with Security Checks
    USER[👤 User Request] -->|1| DDoS
    DDoS -->|2| GEO
    GEO -->|3| RATE
    RATE -->|4| WAF
    WAF -->|5| TLS
    
    TLS -->|6| MFA
    MFA -->|7| SSO
    SSO -->|8| RBAC
    RBAC -->|9| JWT
    
    JWT -->|10| CSRF
    CSRF -->|11| CORS
    CORS -->|12| INPUT
    INPUT -->|13| OUTPUT
    
    OUTPUT -->|14| ENC_TRANSIT
    ENC_TRANSIT -->|15| APP[Application Logic]
    
    APP -->|16| ENC_REST
    ENC_REST -->|17| SECRETS
    SECRETS -->|18| DB[(Database)]
    
    %% Monitoring Flow
    APP -.->|logs| AUDIT
    APP -.->|events| IDS
    IDS -.->|alerts| SIEM
    SIEM -.->|critical| ALERT_SYS
    
    ALERT_SYS -.->|trigger| PLAYBOOK
    PLAYBOOK -.->|log| FORENSICS
    
    %% Continuous Security
    APP -.->|scan| VULN
    DB -.->|backup| BACKUP_ENC
    BACKUP_ENC -.->|store| RECOVERY
    
    %% Admin Access
    ADMIN[👨‍💼 Admin] -->|secure| VPN
    VPN -->|restricted| APP
    
    %% Styling
    classDef perimeter fill:#ffebee,stroke:#c62828,stroke-width:3px
    classDef network fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    classDef identity fill:#f3e5f5,stroke:#6a1b9a,stroke-width:3px
    classDef application fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    classDef data fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    classDef monitoring fill:#fce4ec,stroke:#ad1457,stroke-width:3px
    classDef incident fill:#e0f2f1,stroke:#00695c,stroke-width:3px
    
    class DDoS,GEO,RATE perimeter
    class WAF,TLS,VPN network
    class MFA,SSO,RBAC,JWT identity
    class CSRF,CORS,INPUT,OUTPUT application
    class ENC_TRANSIT,ENC_REST,SECRETS,BACKUP_ENC data
    class IDS,SIEM,AUDIT,VULN monitoring
    class ALERT_SYS,PLAYBOOK,FORENSICS,RECOVERY incident
```

### 3.6 Datenfluss-Diagramm: Modell-Upload & Validierung

```mermaid
%%{init: {'theme':'base', 'sequence': {'useMaxWidth':false}}}%%
sequenceDiagram
    autonumber
    
    actor FP as 👨‍💼 Fachplaner
    participant UI as 🖥️ Web UI
    participant API as ⚙️ API Gateway
    participant AUTH as 🔐 Auth Service
    participant VAL as ✅ Validation Service
    participant IDS as 📋 IDS Engine
    participant IFC as 🏗️ IFC Analyzer
    participant DB as 💾 Database
    participant QUEUE as 📨 Queue (Redis)
    participant WORKER as ⚡ Worker
    participant S3 as 📦 S3 Storage
    participant CDE as ☁️ CDE System
    participant BCF as 🐛 BCF Manager
    participant EMAIL as 📧 Email Service
    
    rect rgb(230, 245, 255)
        Note over FP,EMAIL: Phase 1: Authentication & Upload
        FP->>UI: Login mit Credentials
        UI->>AUTH: POST /auth/login
        AUTH->>AUTH: Verify Credentials
        AUTH->>DB: Check User & Permissions
        DB-->>AUTH: User Data + Roles
        AUTH->>AUTH: Generate JWT Token
        AUTH-->>UI: JWT Token + Refresh Token
        UI->>UI: Store Token (httpOnly Cookie)
        UI-->>FP: Login Successful
    end
    
    rect rgb(240, 255, 240)
        Note over FP,EMAIL: Phase 2: File Upload
        FP->>UI: Select IFC File (150 MB)
        FP->>UI: Click "Upload Model"
        UI->>UI: Pre-validate File Type (.ifc)
        UI->>UI: Calculate MD5 Checksum
        
        UI->>API: POST /api/v1/models/upload<br/>{file, modell_id, checksum}
        API->>AUTH: Verify JWT Token
        AUTH-->>API: Token Valid + User Roles
        
        API->>DB: Check Modell exists in Modellplan
        DB-->>API: Modell Metadata + Requirements
        
        API->>S3: Upload IFC File<br/>Key: models/{project}/{modell_id}/v1.0.ifc
        S3-->>API: Upload Complete + S3 URL
        
        API->>DB: INSERT INTO validierung<br/>(status='pending', file_url=...)
        DB-->>API: Validation Record Created
        
        API->>QUEUE: Enqueue Validation Job<br/>{validierung_id, file_url, rules}
        QUEUE-->>API: Job ID
        
        API-->>UI: 202 Accepted<br/>{job_id, estimated_time='5min'}
        UI-->>FP: Upload Successful<br/>⏳ Validation in Progress...
    end
    
    rect rgb(255, 250, 240)
        Note over FP,EMAIL: Phase 3: Asynchronous Validation
        QUEUE->>WORKER: Dequeue Validation Job
        WORKER->>S3: Download IFC File
        S3-->>WORKER: IFC File Stream
        
        WORKER->>IFC: Analyze IFC Structure
        IFC->>IFC: Parse IFC with IfcOpenShell
        IFC->>IFC: Extract Geometry + Properties
        IFC->>IFC: Calculate Bounding Box
        IFC-->>WORKER: {entities: 15234, bbox: [...], properties: {...}}
        
        WORKER->>DB: Get IDS Rules for Fachmodell
        DB-->>WORKER: IDS XML Rules
        
        WORKER->>IDS: Validate against IDS Rules
        IDS->>IDS: Check Entity Classification
        IDS->>IDS: Validate Property Sets
        IDS->>IDS: Check Required Attributes
        IDS->>IDS: Verify Naming Conventions
        IDS-->>WORKER: Validation Results<br/>{passed: 45, failed: 3, warnings: 2}
    end
    
    alt Validation FAILED
        rect rgb(255, 240, 240)
            Note over FP,EMAIL: Phase 4a: Failure Handling
            WORKER->>BCF: Create BCF Issue for each Failure
            BCF->>BCF: Generate BCF XML
            BCF->>BCF: Add Screenshots (if applicable)
            BCF-->>WORKER: BCF File Created
            
            WORKER->>S3: Upload BCF File
            S3-->>WORKER: BCF URL
            
            WORKER->>DB: UPDATE validierung<br/>SET status='fehler', fehler_details=[...]
            WORKER->>DB: INSERT INTO bcf_issue (...)
            
            WORKER->>EMAIL: Send Failure Notification
            EMAIL->>EMAIL: Compose Email with BCF Link
            EMAIL->>FP: 📧 Validation Failed<br/>3 Issues Found - See BCF
            
            WORKER->>UI: WebSocket Notification
            UI-->>FP: ❌ Validation Failed<br/>View Report
            
            FP->>UI: Click "View Report"
            UI->>API: GET /api/v1/validation/{validation_id}/report
            API->>DB: Fetch Validation Details
            DB-->>API: Error Details + BCF URLs
            API-->>UI: Detailed Report
            UI-->>FP: Show Errors:<br/>1. Missing IO_Nummer<br/>2. Invalid BBox<br/>3. Wrong IFC Class
        end
    else Validation PASSED
        rect rgb(240, 255, 245)
            Note over FP,EMAIL: Phase 4b: Success Handling
            WORKER->>DB: UPDATE validierung<br/>SET status='bestanden', letzter_check=NOW()
            WORKER->>DB: UPDATE modell SET last_validated=NOW()
            
            WORKER->>CDE: Upload Approved Model
            CDE->>CDE: Version Model (v1.0)
            CDE->>CDE: Set Status: 'Shared'
            CDE-->>WORKER: Model Published
            
            WORKER->>DB: INSERT INTO model_history<br/>(action='published_to_cde')
            
            WORKER->>EMAIL: Send Success Notification
            EMAIL->>FP: 📧 ✅ Validation Successful<br/>Model Published to CDE
            
            WORKER->>UI: WebSocket Notification
            UI-->>FP: ✅ Validation Passed<br/>Model Available in CDE
            
            %% Notify other team members
            WORKER->>DB: Get Stakeholders (BIM Manager, etc.)
            DB-->>WORKER: Stakeholder List
            loop For each Stakeholder
                WORKER->>EMAIL: Notify: New Model Available
            end
        end
    end
    
    rect rgb(250, 240, 255)
        Note over FP,EMAIL: Phase 5: Post-Processing
        WORKER->>DB: Generate Statistics
        DB-->>WORKER: {total_models: 15, validated: 12, failed: 3}
        
        WORKER->>S3: Upload Validation Report (PDF)
        S3-->>WORKER: Report URL
        
        WORKER->>DB: UPDATE projekt<br/>SET last_activity=NOW()
        
        WORKER->>QUEUE: Mark Job Complete
        QUEUE-->>WORKER: Acknowledged
    end
    
    Note over FP,EMAIL: 🎉 Process Complete: Total Time ~3-5 minutes
```

### 3.7 State Machine: Modell-Lifecycle

```mermaid
%%{init: {'theme':'base'}}%%
stateDiagram-v2
    [*] --> Geplant: Modell im Modellplan<br/>definiert
    
    Geplant --> InArbeit: Fachplaner<br/>startet Modellierung
    
    InArbeit --> Hochgeladen: IFC-Upload<br/>durch Fachplaner
    
    Hochgeladen --> InValidierung: Automatische<br/>Validierung<br/>gestartet
    
    InValidierung --> ValidationFailed: IDS-Regeln<br/>nicht erfüllt
    InValidierung --> ValidationPassed: Alle Checks<br/>bestanden
    
    ValidationFailed --> InKorrektur: BCF erstellt<br/>Fachplaner<br/>informiert
    
    InKorrektur --> InArbeit: Fehler<br/>korrigiert
    InKorrektur --> Abgelehnt: Schwerwiegende<br/>Mängel /<br/>3 Versuche
    
    ValidationPassed --> InReview: Manuelle<br/>Review durch<br/>BIM-Manager
    
    InReview --> ReviewRejected: Koordinations-<br/>probleme<br/>gefunden
    InReview --> Freigegeben: Review<br/>erfolgreich
    
    ReviewRejected --> InKorrektur: Feedback an<br/>Fachplaner
    
    Freigegeben --> ImCDE: Publikation<br/>auf CDE
    
    ImCDE --> Aktiv: In Koordination<br/>verwendet
    
    Aktiv --> InRevision: Update<br/>erforderlich
    Aktiv --> Archiviert: Projekt<br/>abgeschlossen
    
    InRevision --> InArbeit: Neue Version<br/>erstellen
    
    Archiviert --> [*]: Langzeit-<br/>archivierung
    
    Abgelehnt --> [*]: Aus Modellplan<br/>entfernt
    
    note right of Geplant
        Status: draft
        Verantwortlich: BIM-Manager
        Aktionen: Bearbeiten, Löschen
    end note
    
    note right of InArbeit
        Status: in_progress
        Verantwortlich: Fachplaner
        Aktionen: Upload, Pause
    end note
    
    note right of InValidierung
        Status: validating
        System: Automated
        Timeout: 10 Minuten
    end note
    
    note right of ValidationFailed
        Status: failed
        Benachrichtigung: Email + BCF
        Max Retries: 3
    end note
    
    note right of Freigegeben
        Status: approved
        Verantwortlich: BIM-Manager
        SLA: Review < 24h
    end note
    
    note right of Aktiv
        Status: active
        In Verwendung durch:
        - Koordination
        - Clash Detection
        - Visualisierung
    end note
```

### 3.8 Component Interaction: Validation Service

```mermaid
%%{init: {'theme':'base'}}%%
graph TB
    subgraph "External Trigger"
        TRIGGER[🎬 Validation Trigger<br/>- API Call<br/>- CDE Webhook<br/>- Scheduled Job]
    end
    
    subgraph "Validation Orchestrator"
        ORCHESTRATOR[🎭 Orchestrator<br/>FastAPI Service]
        
        subgraph "Validation Pipeline"
            direction TB
            STEP1[Step 1:<br/>Metadata Validation]
            STEP2[Step 2:<br/>IFC Schema Validation]
            STEP3[Step 3:<br/>IDS Rules Validation]
            STEP4[Step 4:<br/>Geometric Validation]
            STEP5[Step 5:<br/>Coordination Check]
            
            STEP1 -->|Pass| STEP2
            STEP2 -->|Pass| STEP3
            STEP3 -->|Pass| STEP4
            STEP4 -->|Pass| STEP5
            
            STEP1 -.->|Fail| ERROR
            STEP2 -.->|Fail| ERROR
            STEP3 -.->|Fail| ERROR
            STEP4 -.->|Fail| ERROR
            STEP5 -.->|Fail| ERROR
        end
    end
    
    subgraph "Validation Engines"
        META_VAL[📋 Metadata Validator<br/>- Filename Check<br/>- Required Properties<br/>- Naming Convention]
        
        IFC_VAL[🏗️ IFC Validator<br/>IfcOpenShell<br/>- Schema Compliance<br/>- Syntax Check<br/>- Version Check]
        
        IDS_ENG[✅ IDS Engine<br/>buildingSMART IDS<br/>- Entity Classification<br/>- Property Sets<br/>- Cardinality]
        
        GEO_VAL[📐 Geometry Validator<br/>- Bounding Box<br/>- Coordinate System<br/>- Unit Consistency<br/>- Void Geometry]
        
        COORD_VAL[🔄 Coordination Validator<br/>Solibri / Navisworks<br/>- Clash Detection<br/>- Clearance Check<br/>- Accessibility]
    end
    
    subgraph "Data Sources"
        MODELLPLAN[(📘 Modellplan<br/>PostgreSQL<br/>- Requirements<br/>- IDS Rules<br/>- Tolerances)]
        
        RULESET[📜 IDS Ruleset<br/>XML Files<br/>- Fachmodell Rules<br/>- Project Rules<br/>- Custom Rules]
        
        REFERENCE[🗺️ Reference Models<br/>S3 Storage<br/>- Context Models<br/>- Approved Models<br/>- Templates]
    end
    
    subgraph "Output Handlers"
        REPORT[📊 Report Generator<br/>- PDF Report<br/>- HTML Dashboard<br/>- JSON API Response]
        
        BCF_GEN[🐛 BCF Generator<br/>- Issue Creation<br/>- Screenshot Capture<br/>- Metadata Enrichment]
        
        NOTIF[📧 Notification Service<br/>- Email<br/>- Slack<br/>- WebSocket]
    end
    
    subgraph "Storage & Logging"
        RESULTS[(💾 Validation Results<br/>PostgreSQL<br/>- Status<br/>- Errors<br/>- Metrics<br/>- History)]
        
        ARTIFACTS[📦 Artifacts<br/>S3 Storage<br/>- BCF Files<br/>- Reports<br/>- Screenshots]
        
        AUDIT[📝 Audit Log<br/>Immutable Log<br/>- User Actions<br/>- Timestamps<br/>- Changes]
    end
    
    ERROR[❌ Error Handler<br/>Retry Logic<br/>Dead Letter Queue]
    
    %% Trigger Flow
    TRIGGER -->|1. Initiate| ORCHESTRATOR
    
    %% Orchestrator to Pipeline
    ORCHESTRATOR -->|2. Start| STEP1
    ORCHESTRATOR -.->|Load| MODELLPLAN
    ORCHESTRATOR -.->|Load| RULESET
    ORCHESTRATOR -.->|Load| REFERENCE
    
    %% Pipeline to Engines
    STEP1 -->|3a| META_VAL
    STEP2 -->|3b| IFC_VAL
    STEP3 -->|3c| IDS_ENG
    STEP4 -->|3d| GEO_VAL
    STEP5 -->|3e| COORD_VAL
    
    %% Engines to Data
    META_VAL -.->|query| MODELLPLAN
    IDS_ENG -.->|load| RULESET
    COORD_VAL -.->|download| REFERENCE
    
    %% Success Path
    STEP5 -->|4. All Pass| REPORT
    REPORT -->|5a| RESULTS
    REPORT -->|5b| ARTIFACTS
    REPORT -->|5c| NOTIF
    
    %% Error Path
    ERROR -->|6a. Generate| BCF_GEN
    ERROR -->|6b. Store| RESULTS
    ERROR -->|6c. Alert| NOTIF
    
    BCF_GEN -->|7| ARTIFACTS
    
    %% Audit Trail
    ORCHESTRATOR -.->|log| AUDIT
    REPORT -.->|log| AUDIT
    ERROR -.->|log| AUDIT
    
    %% Styling
    classDef trigger fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef orchestrator fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef pipeline fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef engine fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef output fill:#e0f2f1,stroke:#00796b,stroke-width:2px
    classDef storage fill:#f1f8e9,stroke:#689f38,stroke-width:2px
    classDef error fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class TRIGGER trigger
    class ORCHESTRATOR orchestrator
    class STEP1,STEP2,STEP3,STEP4,STEP5 pipeline
    class META_VAL,IFC_VAL,IDS_ENG,GEO_VAL,COORD_VAL engine
    class MODELLPLAN,RULESET,REFERENCE data
    class REPORT,BCF_GEN,NOTIF output
    class RESULTS,ARTIFACTS,AUDIT storage
    class ERROR error
```

        
