Below is a thorough cross-check and technical review of your current PIM/AIM page, mapped against the reality of modern infrastructure projects (highways, bridges, tunnels) and ISO 19650-aligned delivery. I’ve also provided a fully revised file that corrects standards, tightens terminology, upgrades the mermaid diagrams to render correctly, and adds concrete practices used by national road agencies.

Key review findings and suggested improvements

1) Fix standards and terminology
- ISO reference typo: “ISO 90650” should be “SN EN ISO 19650”. Use “Exchange Information Requirements (EIR)” per ISO 19650; “Employer’s” stems from legacy PAS 1192 usage. You can mention both, but default to “Exchange”.
- For infrastructure, explicitly call out IFC 4.3 (roads/bridges/rail alignment, linear assets). This is now the reference for openBIM infra exchanges.
- Add related standards that are widely used on real projects:
  - IDS (Information Delivery Specification) for machine-checkable data validation
  - bSDD for harmonized classification/semantics
  - BCF 2.1/3.0 for issue exchange
  - ISO 19650-5 for security-minded information management
- Swiss context: reference “SN EN ISO 19650” and SIA 2051 as relevant. If you require national coordinates, prefer EPSG:2056 (CH1903+/LV95) and LHN95 for heights; ensure IFC georeferencing via IfcMapConversion.

2) Strengthen lifecycle and governance
- Add the information hierarchy: OIR → AIR → PIR → EIR → IDP/MIDP/TIDP. This is what real infra clients and delivery teams map to responsibilities and milestones.
- Replace “data drops” with “information delivery milestones” (ISO 19650 language).
- Emphasize CDE states: WIP → Shared → Published → Archive with approvals and audit trails standard on infrastructure programs.

3) PIM→AIM handover content and validation
- Real projects hand over more than IFC:
  - IFC 4.3 Reference View for as-built geometry and aligned property sets
  - IDS rulesets (.ids) for validating what’s delivered (properties, classifications, MVD constraints)
  - Structured asset registers (may be COBie where applicable; infra projects increasingly prefer IFC 4.3 + IDS/bSDD over COBie-only)
  - O&M docs (PDFs), test certificates, warranties, spares
  - Linear Referencing (LRS) and segmentation data for highways (route ID, chainage, events)
- Add a QA/QC stack:
  - Model checks: georeferencing, units, valid GUIDs, clash/scope checks
  - Data checks: required property presence and constraints (via IDS), classification coverage (bSDD/Uniclass/ASTRA schema)
  - Handover acceptance criteria with measurable thresholds.

4) Interoperability and GIS integration
- For highways: LRS is essential. Show how the alignment and segmentation connect with AIM and GIS (OGC API – Features, GeoPackage, CityJSON/CityGML 3.0 where applicable).
- Highlight IfcAlignment and IfcLinearPlacement in IFC 4.3 to anchor assets to a route/chainage.

5) Correct and improve diagrams
- Your mermaid styles reference non-existent IDs (“style PIM …”), so the styles don’t apply. Target actual node IDs defined in the graph.
- Update the CDE diagram to show WIP/Shared/Published/Archive, and situate standards (IFC/IDS/BCF/bSDD/GIS) clearly along the exchange points.
- Add an LRS diagram to make infra realities explicit.

6) Swiss/ASTRA context
- If you intend to reference specific ASTRA systems, keep it generic unless formally defined (e.g., “ASTRA Asset Management Platform”). Avoid “ASTRA DS” unless you define it.
- If you adopt ASTRA-specific naming (e.g., data dictionaries, classification, or a national asset catalog), note them explicitly and tie them to bSDD/IFC property sets.

7) Clean up content issues
- Remove duplicated intro sentence.
- Expand truncated sections.
- Use consistent terms: Appointing Party, Lead Appointed Party, Appointed Parties (ISO 19650), and reflect roles in responsibilities for OIR/AIR/PIR/EIR.

Proposed updated file

I’ve integrated all fixes, added concrete infra practices, corrected standards, and replaced the diagrams with validated mermaid that should render correctly. I also added an IDS example snippet to illustrate validation.


# PIM and AIM for Infrastructure (ASTRA Context)

This document explains the Project Information Model (PIM) and the Asset Information Model (AIM) for infrastructure projects, aligned to SN EN ISO 19650 and openBIM standards used across roads, bridges, and tunnels. It includes lifecycle governance, information delivery, handover validation, and GIS/LRS integration that real highway authorities and operators use in practice.

## 1) Definitions and Lifecycle

In SN EN ISO 19650, information management spans the project phase (PIM) and the operational phase (AIM):

- Project Information Model (PIM): The aggregated graphical and non-graphical information produced during design, construction, and commissioning. It is progressively developed and quality-controlled in the CDE.
- Asset Information Model (AIM): The single, validated source of asset data used in operation and maintenance. The AIM is established from accepted as-built project information at handover and is maintained throughout the asset lifecycle.

Related information requirements and plans:
- OIR: Organizational Information Requirements
- AIR: Asset Information Requirements
- PIR: Project Information Requirements
- EIR: Exchange Information Requirements (ISO 19650 term; historically “Employer’s” under PAS 1192)
- IDP/MIDP/TIDP: Information Delivery Plan / Master Information Delivery Plan / Task Information Delivery Plan

PIM-to-AIM is executed at information delivery milestones with acceptance criteria, not a single “big-bang” drop.

## 2) Standards and Open Formats

- ISO 19650 (SN EN ISO 19650-1/2/3/5): Organization, delivery, asset operation, and security-minded approach
- IFC 4.3 (ISO 16739): Open exchange for infrastructure (roads, bridges, rail); support alignments, linear assets, placements
- IDS (Information Delivery Specification): Machine-checkable rules for properties, classification, and structure
- bSDD: buildingSMART Data Dictionary for harmonized semantics/classifications
- BCF 2.1/3.0: Issue exchange
- GIS/OGC: OGC API – Features, GeoPackage, CityJSON/CityGML 3.0 where relevant

Swiss context:
- SN EN ISO 19650 for information management
- SIA 2051 for BIM principles
- Coordinate reference: EPSG:2056 (CH1903+/LV95) and LHN95 for heights; implement IFC georeferencing via IfcMapConversion

## 3) Information Lifecycle Overview

This diagram shows the journey from EIR to PIM and accepted AIM, including validation and handover content beyond geometry.

````mermaid
flowchart TD
    subgraph PD[Project Delivery Phase]
        need[Project Need] --> eir["Exchange Information Requirements (EIR)"]
        eir --> appoint[Tender/Appointment]
        appoint --> pim["Project Information Model (PIM)"]
        pim --> vv{"Verification & Validation<br/>(Model + Data + Docs)"}
    end

    subgraph HO[Handover]
        vv --> pkg[Handover Package<br/>IFC 4.3 + IDS + Docs + Registers]
    end

    subgraph OP[Asset Operation Phase]
        pkg --> aim["Asset Information Model (AIM)"]
        aim --> oam{Operation & Maintenance}
        oam --> changes[Works / Updates / Renovations]
        changes --> aim
    end

    style pim fill:#cfe9ff,stroke:#333,stroke-width:1.2px
    style aim fill:#cfe9ff,stroke:#333,stroke-width:1.2px
    style pkg fill:#f9f9c5,stroke:#666,stroke-width:1px
````
Process highlights:
1. Appointing Party defines OIR/AIR and sets EIR; Lead Appointed Party plans MIDP/TIDP/IDP.
2. PIM grows through design, construction, and commissioning, managed in the CDE.
3. Verification and Validation apply to model quality, data completeness/accuracy (via IDS), classification (via bSDD), georeferencing, and documentation.
4. Handover includes geometry (IFC 4.3 Reference View), asset registers, O&M documentation, warranties/spares, and validation evidence.
5. AIM is maintained as the living source in operations and updated after changes.

## 4) CDE States, Interoperability, and Governance

Real infrastructure programs use formal CDE states and approvals.

````mermaid
flowchart LR
    subgraph CDE[Common Data Environment]
        WIP[WIP<br/>Authoring] --> Shared[Shared<br/>Coordinated]
        Shared --> Published[Published<br/>Approved]
        Published --> Archived[Archived<br/>Record]
    end

    subgraph Standards[Open Standards]
        IFC[IFC 4.3]:::std
        IDS[IDS]:::std
        BCF[BCF 2.1/3.0]:::std
        bSDD[bSDD]:::std
        GIS[OGC APIs / GPKG]:::std
    end

    subgraph Stakeholders
        Designers
        Contractors
        Owner["Owner/Operator (ASTRA)"]
    end

    Designers -->|Models/Issues| WIP
    Contractors -->|Models/Docs| Shared
    Shared -->|Coordination via BCF| Designers
    Shared -->|IDS Validation| Published
    Published -->|IFC+IDS+Docs| Owner
    Owner -->|AIM updates| Archived

    IFC -. used by .-> Shared
    IDS -. used by .-> Published
    BCF -. used by .-> Shared
    bSDD -. semantics .-> Shared
    GIS -. context .-> Published

    classDef std fill:#fff,stroke:#333,stroke-dasharray: 5 5;
````
Include governance:
- Naming, versioning, and persistent IDs (GUID retention across revisions)
- Approval workflows and audit trails
- Security-minded approach per ISO 19650-5 (sensitive locations, redactions if required)
- Retention and archival policies

## 5) Linear Referencing (LRS) and GIS Integration

For highways, LRS is essential to locate assets by route and chainage and to support segmentation, inspections, and events.

````mermaid
flowchart LR
    align[Alignment + IfcLinearPlacement] --> lrs[LRS / Route + Chainage]
    lrs --> segments["Operational Segments<br/>(e.g., km 0.0–5.0, 5.0–10.0)"]
    segments --> assets["Asset Instances<br/>(barriers, signs, lighting, drainage)"]
    GIS[GIS Layers / OGC API] --> segments
    assets --> aim[AIM / Asset Register]

    style lrs fill:#eef6ff,stroke:#333,stroke-width:1px
    style aim fill:#cfe9ff,stroke:#333,stroke-width:1.2px
````
Implementation notes:
- Use IFC 4.3 IfcAlignment and IfcLinearPlacement to anchor assets.
- Maintain EPSG:2056 georeferencing with IfcMapConversion; validate vertical datum (LHN95).
- Synchronize AIM keys (route IDs, section IDs, chainage) with GIS layers for queries and dashboards.

## 6) Handover Content and Acceptance Criteria

Typical accepted content from real infrastructure programs:
- Geometry: IFC 4.3 Reference View; bridge, road, tunnel objects with correct placements and relationships
- Data: Required property sets and classifications (bSDD codes or national/ASTRA schema)
- Registers: Asset register with unique IDs and status, inspection/test certificates, warranty/spares lists
- Documentation: O&M manuals, maintenance plans, method statements as PDFs or structured docs
- Validation Evidence: IDS validation reports, model check logs, geospatial check reports

Suggested measurable acceptance criteria:
- 100% presence of mandatory properties per IDS across defined object scope
- 100% valid georeferencing (EPSG:2056), vertical datum consistent, elevation sanity checks
- 0 critical clashes in Published; < N minor clashes documented with BCF and risk accepted
- 100% object GUID stability between pre-handover and as-built delivery
- Classification coverage ≥ 98% for mandated classes

## 7) Validation with IDS (example snippet)

Below is a minimal IDS illustration for an infrastructure handover to enforce key properties. Adjust classes, properties, and enumerations to ASTRA’s AIR/EIR.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ids:ids xmlns:ids="http://standards.buildingsmart.org/IDS"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         version="1.0">
  <ids:specification name="AIM Handover – Road Assets">
    <ids:applicability>
      <ids:entity name="IfcFacilityPart"/>
      <ids:classification system="bSDD" value="roadAsset"/>
    </ids:applicability>
    <ids:requirements>
      <ids:property name="AssetID" minOccurs="1" ifc:propertySet="Pset_AssetCommon"/>
      <ids:property name="InstallationDate" minOccurs="1" ifc:propertySet="Pset_ManufacturerOccurrence"/>
      <ids:property name="MaintenanceClass" minOccurs="1" enumeration="A;B;C"/>
      <ids:classification system="ASTRA" value="ASTRA-CLASS-CODE" minOccurs="1"/>
    </ids:requirements>
  </ids:specification>
</ids:ids>
```

## 8) Observations from real infrastructure programs

- IFC 4.3 adoption: Road/bridge agencies are standardizing on IFC 4.3 for handover geometry; COBie is sometimes used but increasingly replaced or complemented by IFC 4.3 + IDS + bSDD for infra.
- Progressive handovers: Information delivery milestones align with commissioning stages; early acceptance reduces end-of-project risk.
- LRS-first AIM: Operations rely on route/chainage and segmentation for inspections, events, and maintenance planning—ensure alignment objects and linear placement are correct in PIM before handover.
- CDE rigor: WIP/Shared/Published/Archive states with approvals and audit logs are enforced; BCF is used to close-out coordination issues pre-handover.
- Security-minded approach: Sensitive assets or locations may require masking/redaction and controlled distribution per ISO 19650-5.

## 9) ASTRA-specific considerations (to confirm/define)

If ASTRA uses specific:
- Classification systems or data dictionaries (publish mapping to bSDD/IFC)
- Asset management systems (define required import formats and endpoint specs)
- Naming/ID schemes (publish a stable URI/URN/ID policy for AIM persistence)
- Additional Swiss standards (reference SIA/VSS where applicable)

Document these explicitly in AIR/EIR and mirror them in IDS rules.

## 10) Summary of improvements applied in this document

- Corrected standard references (SN EN ISO 19650, IFC 4.3, IDS, bSDD, BCF)
- Replaced legacy “Employer’s” with ISO’s “Exchange” in EIR context
- Added OIR/AIR/PIR/EIR and IDP/MIDP/TIDP alignment
- Introduced CDE states and governance
- Expanded PIM→AIM handover content, validation stack, and acceptance criteria
- Added infra-specific LRS and geospatial guidance (EPSG:2056, LHN95)
- Fixed mermaid diagrams (valid node references and styles)
- Added IDS example for machine-checkable validation

By adopting these practices, ASTRA’s PIM→AIM process will reflect real-world infrastructure program delivery, reduce handover risk, and produce an AIM that is operationally useful from day one.

