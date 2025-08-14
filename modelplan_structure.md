# Modellplan Analysis for ASTRA Infrastructure Context

---

## ✔️ Planned Analysis Steps

- Review and extract requirements for an infrastructure-focused (roads/tunnels) Modellplan.
- Identify and describe the main building blocks with an emphasis on structure and content.
- Summarize key business processes relevant to ASTRA’s infrastructure projects.
- Define entity data structures with attributes, types, descriptions, and cardinality.
- Document ambiguities or missing data as comments.

---

## 1. Requirements

- **Discipline Coverage**: Must represent all relevant disciplines—Architecture, Structural, MEP, Civil, Landscape, Construction, Cost, As-Built, Facility Management—with a strong focus on civil works (roads, tunnels).
- **Level of Detail (LOD)**: Models should support LODs from preliminary (200) to as-built (500), depending on project phase.
- **Interoperability**: Use of standardized formats (RVT, IFC, DWG, NWD) to ensure smooth data exchange among stakeholders.
- **Component Granularity**: Each model must decompose into discipline-specific components (e.g., site, utilities, topography for civil).
- **Traceability and Handover**: Support for tracking changes, as-built validation, and FM-ready data handover (COBie/IFC).

---

## 2. Overview and Content Blocks of a Modellplan

The Modellplan is a federated schema that integrates discipline-specific models. Its major building blocks are:

- **master_model**: The aggregation of all sub-models for coordination and clash detection.
- **architectural_model**: Architectural elements (site, floor plans, interiors).
- **structural_model**: Structural framework (foundations, columns, slabs).
- **mep_model**: Mechanical, Electrical, Plumbing components (HVAC, piping, power).
- **civil_model**: Civil infrastructure (roads, tunnels, topography, utilities).
- **landscape_model**: Hardscape/softscape and site furniture.
- **construction_model**: Temporary works and logistics for construction sequencing.
- **cost_model**: Quantity takeoff and cost estimation.
- **as_built_model**: Verified, as-installed data for each discipline.
- **facility_management_model**: FM-specific data for operation and maintenance.

**Note:** For ASTRA, the _civil_model_ block is most critical, and should be extended for detailed tunnel and road modeling.

---

## 3. Processes

| # | Process                                   | Summary                                                                                  |
|---|-------------------------------------------|------------------------------------------------------------------------------------------|
| 1 | Model Authoring                           | Creation of discipline-specific models (civil, structural, MEP, etc.) at required LODs.  |
| 2 | Model Coordination & Clash Detection      | Aggregation in the master model; spatial/discipline conflict resolution.                  |
| 3 | Data Exchange & Interoperability          | Export/import models in standard formats; synchronize with external stakeholders.         |
| 4 | Construction Planning & Sequencing        | 4D simulation, logistics, and temporary works planning, especially for roads/tunnels.     |
| 5 | Cost Estimation & Quantity Takeoff        | Derivation of quantities and costs for materials, labor, and equipment.                   |
| 6 | As-Built Documentation                   | Validation and recording of the constructed state for handover and compliance.            |
| 7 | Facility Management Preparation           | Extraction/preparation of FM data (COBie/IFC) for long-term maintenance.                  |

---

## 4. Entity Data Structures

### 4.1 master_model

| Attribute Name | Type    | Description                                          | Cardinality         |
|----------------|---------|------------------------------------------------------|---------------------|
| description    | string  | High-level description of the federated model        | 1                   |
| format         | enum    | File format (e.g., NWD)                              | 1                   |
| purpose        | string  | Purpose of the master model                          | 1                   |
| models         | map     | Discipline-specific model references                 | 1..n (per discipline)|

---

### 4.2 civil_model

| Attribute Name       | Type     | Description                        | Cardinality   |
|---------------------|----------|------------------------------------|---------------|
| discipline          | string   | Civil Engineering                  | 1             |
| LOD                 | range    | Level of Detail (200–400)          | 1             |
| format              | enum     | DWG / IFC                          | 1..n          |
| purpose             | string   | Site planning, grading, utilities  | 1             |
| components          | array    | Civil components                   | 1..n          |

#### civil_model.components (example)

| Attribute Name     | Type    | Description                          | Cardinality |
|-------------------|---------|--------------------------------------|-------------|
| name              | string  | Component name (e.g., topography)    | 1           |
| purpose           | string  | Role in civil model                  | 1           |

---

### 4.3 structural_model

| Attribute Name    | Type     | Description                         | Cardinality |
|------------------|----------|-------------------------------------|-------------|
| discipline       | string   | Structural Engineering              | 1           |
| LOD              | range    | Level of Detail (300–500)           | 1           |
| format           | enum     | RVT                                 | 1           |
| purpose          | string   | Structural analysis, load path      | 1           |
| components       | array    | Structural components               | 1..n        |

#### structural_model.components

| Attribute Name  | Type    | Description                         | Cardinality |
|-----------------|---------|-------------------------------------|-------------|
| name            | string  | Component name (e.g., foundations)  | 1           |
| purpose         | string  | Purpose of the component            | 1           |

---

### 4.4 mep_model

| Attribute Name     | Type    | Description                                  | Cardinality |
|-------------------|---------|----------------------------------------------|-------------|
| discipline        | string  | MEP Engineering                             | 1           |
| LOD               | range   | Level of Detail (300–500)                    | 1           |
| format            | enum    | RVT                                          | 1           |
| purpose           | string  | Coordination of services                     | 1           |
| components        | object  | Subsystems: mechanical, electrical, plumbing | 1           |

#### mep_model.components (mechanical/electrical/plumbing)

| Attribute Name | Type    | Description                         | Cardinality |
|---------------|---------|-------------------------------------|-------------|
| name          | string  | Component name                      | 1           |
| purpose       | string  | Purpose of the component            | 1           |

---

### 4.5 as_built_model

| Attribute Name | Type    | Description                                 | Cardinality |
|---------------|---------|---------------------------------------------|-------------|
| discipline    | string  | All disciplines                             | 1           |
| LOD           | range   | Level of Detail (500)                       | 1           |
| format        | enum    | RVT / IFC                                   | 1..n        |
| purpose       | string  | Final record model for handover             | 1           |
| components    | array   | Verified discipline-specific components     | 1..n        |

---

### 4.6 facility_management_model

| Attribute Name    | Type    | Description                             | Cardinality |
|------------------|---------|-----------------------------------------|-------------|
| discipline       | string  | FM / Operations                         | 1           |
| LOD              | range   | Level of Detail (500)                   | 1           |
| format           | enum    | IFC / COBie / RVT                       | 1..n        |
| purpose          | string  | Operation and maintenance management     | 1           |
| components       | array   | FM data components                      | 1..n        |

#### facility_management_model.components

| Attribute Name   | Type    | Description                     | Cardinality |
|------------------|---------|---------------------------------|-------------|
| name             | string  | Component name                  | 1           |
| purpose          | string  | Purpose of the FM component     | 1           |

---

<!-- 
Ambiguity: For tunnel/road-specific attributes (e.g., alignment geometry, cross-section, tunnel systems), extend civil_model.components as per ASTRA requirements.
-->
