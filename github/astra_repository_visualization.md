# ASTRA Repository-Organisation Visualisierung

## Gesamt-Organisationsstruktur

```mermaid
graph TB
    subgraph "ASTRA GitHub Enterprise Organisation"
        A[ASTRA Admin] --> B[Organisationseinstellungen]
        B --> B1[SAML SSO]
        B --> B2[IP Allowlists]
        B --> B3[Audit Log Streaming]
        B --> B4[2FA Enforcement]
        
        A --> C[Teams]
        C --> C1[fa:fa-shield Governance-Team<br/>5 Mitglieder]
        C --> C2[fa:fa-edit Dokumentations-Editoren<br/>8 Mitglieder]
        C --> C3[fa:fa-server IT-Operations<br/>10 Mitglieder]
        C --> C4[fa:fa-users Projekt-Teams<br/>7+ Mitglieder]
        
        C1 --> D[Admin Repositories]
        C2 --> E[Dokumentations Repositories]
        C3 --> F[Infrastructure Repositories]
        C4 --> G[Projekt Repositories]
    end
    
    style A fill:#f96,stroke:#333,stroke-width:4px
    style C1 fill:#69f,stroke:#333,stroke-width:2px
    style C2 fill:#9f6,stroke:#333,stroke-width:2px
    style C3 fill:#f69,stroke:#333,stroke-width:2px
    style C4 fill:#ff6,stroke:#333,stroke-width:2px
```

## Repository-Kategorisierung nach Sichtbarkeit

```mermaid
pie title Repository-Verteilung nach Sichtbarkeit
    "Öffentlich (10%)" : 10
    "Intern (70%)" : 70
    "Privat (20%)" : 20
```

## Repository-Struktur und Namenskonvention

```mermaid
graph LR
    subgraph "Namenskonvention"
        N["[abteilung]-[projekt]-[typ]"]
    end
    
    subgraph "Öffentliche Repositories"
        P1[fa:fa-globe astra-api-dokumentation]
        P2[fa:fa-globe astra-open-data]
        P3[fa:fa-globe astra-developer-portal]
    end
    
    subgraph "Interne Repositories"
        I1[fa:fa-building strassen-digital-transform-docs]
        I2[fa:fa-building admin-policy-templates]
        I3[fa:fa-building infrastructure-monitoring-api]
        I4[fa:fa-building verkehr-analysis-web]
        I5[fa:fa-building bim-standards-docs]
        I6[fa:fa-building sicherheit-prozess-docs]
    end
    
    subgraph "Private Repositories"
        PR1[fa:fa-lock security-audit-reports]
        PR2[fa:fa-lock personal-data-processing]
        PR3[fa:fa-lock incident-response-tools]
    end
    
    N --> P1
    N --> I1
    N --> PR1
    
    style P1 fill:#9f9,stroke:#333,stroke-width:2px
    style P2 fill:#9f9,stroke:#333,stroke-width:2px
    style I1 fill:#ff9,stroke:#333,stroke-width:2px
    style I2 fill:#ff9,stroke:#333,stroke-width:2px
    style PR1 fill:#f99,stroke:#333,stroke-width:2px
    style PR2 fill:#f99,stroke:#333,stroke-width:2px
```

## Branching-Workflow

```mermaid
gitGraph
    commit id: "Initial Setup" tag: "v0.1.0"
    branch develop
    checkout develop
    commit id: "Development Start"
    
    branch feature/neue-api
    checkout feature/neue-api
    commit id: "API Grundgerüst"
    commit id: "Tests hinzugefügt"
    commit id: "Dokumentation"
    
    checkout develop
    merge feature/neue-api
    
    branch feature/sicherheits-update
    checkout feature/sicherheits-update
    commit id: "Security Patch"
    commit id: "Validierung"
    
    checkout develop
    merge feature/sicherheits-update
    
    checkout main
    merge develop tag: "v1.0.0"
    
    branch hotfix/kritischer-fehler
    checkout hotfix/kritischer-fehler
    commit id: "Fehlerkorrektur"
    
    checkout main
    merge hotfix/kritischer-fehler tag: "v1.0.1"
    
    checkout develop
    merge hotfix/kritischer-fehler
```

## Pull Request Review-Prozess

```mermaid
sequenceDiagram
    participant E as Entwickler
    participant G as GitHub
    participant R1 as Reviewer 1
    participant R2 as Reviewer 2
    participant CO as Code Owner
    participant CI as CI/CD Pipeline
    
    E->>G: Feature Branch erstellen
    E->>E: Code entwickeln
    E->>G: Push Changes
    E->>G: Pull Request öffnen
    
    G->>CI: Trigger Automated Tests
    CI->>CI: Run Tests
    CI->>CI: Security Scan
    CI->>CI: Code Quality Check
    CI->>G: Status Check ✅
    
    G->>R1: Review Request
    G->>R2: Review Request
    G->>CO: Code Owner Review Required
    
    R1->>G: Review + Approve ✅
    R2->>G: Review + Changes Required ⚠️
    
    E->>G: Fix Issues
    E->>G: Push Updates
    
    Note over G: Stale Reviews Dismissed
    
    G->>R2: Re-Review Request
    R2->>G: Approve ✅
    CO->>G: Approve ✅
    
    G->>G: All Checks Passed
    E->>G: Squash and Merge
    G->>G: Delete Feature Branch
```

## Security-Schichten

```mermaid
graph TB
    subgraph "Basis-Sicherheit (Kostenlos)"
        B1[2FA Pflicht]
        B2[Signed Commits]
        B3[Branch Protection]
        B4[IP Allowlists]
        B5[SAML SSO]
    end
    
    subgraph "Secret Protection (+19 CHF/Committer)"
        S1[200+ Secret Patterns]
        S2[Push Protection]
        S3[Custom Patterns]
        S4[Security Campaigns]
        S5[Alert Management]
    end
    
    subgraph "Code Security (+30 CHF/Committer)"
        C1[CodeQL Analysis]
        C2[Dependency Scanning]
        C3[SARIF Integration]
        C4[AI-powered Fixes]
        C5[Supply Chain Security]
    end
    
    B1 --> S1
    S1 --> C1
    
    style B1 fill:#9f9,stroke:#333,stroke-width:2px
    style S1 fill:#ff9,stroke:#333,stroke-width:2px
    style C1 fill:#f99,stroke:#333,stroke-width:2px
```

## Team-Zugriffsmatrix

```mermaid
graph LR
    subgraph "Teams"
        T1[Governance]
        T2[Dokumentation]
        T3[IT-Ops]
        T4[Projekte]
    end
    
    subgraph "Zugriffsrechte"
        A[Admin]
        W[Write]
        R[Read]
    end
    
    subgraph "Repository-Typen"
        RT1[Policy Repos]
        RT2[Docs Repos]
        RT3[Infra Repos]
        RT4[Project Repos]
    end
    
    T1 -->|Admin| RT1
    T1 -->|Read| RT2
    T1 -->|Read| RT3
    T1 -->|Read| RT4
    
    T2 -->|Read| RT1
    T2 -->|Admin| RT2
    T2 -->|Read| RT3
    T2 -->|Write| RT4
    
    T3 -->|Read| RT1
    T3 -->|Write| RT2
    T3 -->|Admin| RT3
    T3 -->|Write| RT4
    
    T4 -->|Read| RT1
    T4 -->|Write| RT2
    T4 -->|Write| RT3
    T4 -->|Admin| RT4
```

## Migration Timeline

```mermaid
gantt
    title ASTRA GitHub Migration Zeitplan
    dateFormat  YYYY-MM-DD
    section Phase 1 - Setup
    Enterprise Account Setup           :done, p1_1, 2024-12-01, 7d
    SAML SSO Configuration             :done, p1_2, after p1_1, 5d
    Team Structure Creation            :active, p1_3, after p1_2, 3d
    IP Allowlists                      :p1_4, after p1_3, 2d
    
    section Phase 2 - Security
    Secret Protection Aktivierung      :p2_1, 2024-12-20, 5d
    Audit Log Streaming               :p2_2, after p2_1, 3d
    CODEOWNERS Setup                  :p2_3, after p2_2, 7d
    Branch Protection Rules           :p2_4, after p2_3, 5d
    
    section Phase 3 - Migration
    Repository Migration (Batch 1)     :p3_1, 2025-01-08, 10d
    Repository Migration (Batch 2)     :p3_2, after p3_1, 10d
    CI/CD Pipeline Migration          :p3_3, after p3_2, 14d
    Legacy System Abschaltung         :milestone, after p3_3, 0d
    
    section Phase 4 - Training
    GitHub Skills Rollout             :p4_1, 2024-12-15, 30d
    Expert Services Training          :p4_2, 2025-01-15, 5d
    Champions Training                :p4_3, after p4_2, 3d
    Team Workshops                    :p4_4, after p4_3, 10d
```

## CODEOWNERS Beispiel-Struktur

```mermaid
graph TD
    subgraph "CODEOWNERS Hierarchie"
        ROOT["/"]
        ROOT -->|@astra/admins| ALL["* (Alle Dateien)"]
        
        DOCS["/docs/"]
        DOCS -->|@astra/documentation| DOCS_ALL["*.md, *.adoc"]
        
        POLICIES["/policies/"]
        POLICIES -->|@astra/governance @astra/legal| POL_ALL["Alle Policy-Dateien"]
        
        INFRA["/infrastructure/"]
        INFRA -->|@astra/it-ops| INFRA_CODE["*.tf, *.yaml"]
        
        SECURITY["/security/"]
        SECURITY -->|@astra/security-team| SEC_ALL["Sicherheits-relevante Dateien"]
        
        API["/api/"]
        API -->|@astra/backend-team| API_CODE["*.py, *.java"]
    end
    
    style ROOT fill:#f96,stroke:#333,stroke-width:4px
    style SECURITY fill:#f66,stroke:#333,stroke-width:2px
    style POLICIES fill:#66f,stroke:#333,stroke-width:2px
```

## Compliance-Dashboard Konzept

```mermaid
graph TB
    subgraph "Compliance Monitoring"
        D[Dashboard]
        D --> M1[ISO 27001 Status ✅]
        D --> M2[SOC 2 Reports ✅]
        D --> M3[GDPR/DSG Compliance ✅]
        D --> M4[Audit Logs 📊]
        D --> M5[Security Alerts 🔔]
        
        M4 --> A1[User Activities]
        M4 --> A2[Repository Changes]
        M4 --> A3[Permission Changes]
        M4 --> A4[Security Events]
        
        M5 --> S1[Secret Exposures: 0]
        M5 --> S2[Vulnerabilities: 3 Low]
        M5 --> S3[Dependencies: 127 OK]
    end
    
    subgraph "Automated Reports"
        R1[Weekly Security Report]
        R2[Monthly Compliance Report]
        R3[Quarterly Audit Report]
    end
    
    D --> R1
    D --> R2
    D --> R3
    
    style D fill:#69f,stroke:#333,stroke-width:4px
    style M1 fill:#9f9,stroke:#333,stroke-width:2px
    style M2 fill:#9f9,stroke:#333,stroke-width:2px
    style M3 fill:#9f9,stroke:#333,stroke-width:2px
```

## Support-Eskalationspfad

```mermaid
flowchart TD
    U[User Issue] --> T{Ticket Priority?}
    
    T -->|Low| L[48h Response<br/>Community Forum]
    T -->|Normal| N[48h Response<br/>Email Support]
    T -->|High| H[4h Response<br/>Phone Callback]
    T -->|Urgent| UR[30min Response<br/>Dedicated Engineer]
    
    L --> R[Resolution]
    N --> R
    H --> E[Escalation if needed]
    UR --> E
    
    E --> CSM[Customer Success Manager<br/>Premium Plus Only]
    CSM --> ENG[GitHub Engineering Team]
    ENG --> R
    
    style UR fill:#f66,stroke:#333,stroke-width:2px
    style CSM fill:#ff9,stroke:#333,stroke-width:2px
```

---

*Diese Visualisierungen zeigen die geplante GitHub Enterprise Organisation für ASTRA mit allen wichtigen Strukturen, Prozessen und Abhängigkeiten.*
