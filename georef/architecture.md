# IFC4X3_ADD2 Maker - Architecture Overview

## System Purpose
Generates georeferenced IFC files containing pyramid geometries using Swiss LV95 coordinate system (EPSG:2056) with LoGeoRef50 mapping.

## Coordinate System Flow

```mermaid
graph TB
    A[User Input Coordinates] -->|coords_mode| B{LV95 or Local?}
    B -->|lv95 default| C[LV95 Coordinates<br/>E, N, H]
    B -->|local| D[Local Coordinates<br/>x, y, z]
    
    C -->|Inverse Transform| E[Local Placement<br/>small stable coords]
    D -->|Forward Transform| F[LV95 for ASTRA Pset]
    
    E --> G[IFC Object Placement]
    C --> H[ASTRA Property Set]
    F --> H
    
    G --> I[Final IFC File]
    H --> I
    
    style C fill:#e1f5ff
    style D fill:#ffe1e1
    style G fill:#e1ffe1
    style H fill:#fff5e1
```

## LoGeoRef50 Transformation (Option A)

```mermaid
graph LR
    subgraph "Forward: Local → LV95"
        L1[x, y, z] -->|Rotate| L2[xr, yr]
        L2 -->|Scale & Translate| L3[E, N, H]
    end
    
    subgraph "Inverse: LV95 → Local"
        R1[E, N, H] -->|Translate & Scale| R2[dx, dy]
        R2 -->|Rotate Back| R3[x, y, z]
    end
    
    style L3 fill:#e1f5ff
    style R3 fill:#ffe1e1
```

## IFC Structure Hierarchy

```mermaid
graph TD
    A[IfcProject] -->|aggregates| B[IfcSite]
    B -->|contains| C[IfcVirtualElement 1<br/>Pyramid]
    B -->|contains| D[IfcVirtualElement 2<br/>Pyramid]
    B -->|contains| E[IfcVirtualElement N<br/>Pyramid]
    
    C -->|has| F[Body Representation<br/>Tessellated Mesh]
    C -->|has| G[ASTRA PropertySet<br/>LV95 Coords]
    
    H[IfcProjectedCRS<br/>EPSG:2056] -.->|references| A
    I[IfcMapConversion<br/>Transform Params] -.->|references| A
    
    style A fill:#ff6b6b
    style B fill:#ffd93d
    style C fill:#6bcf7f
    style H fill:#4d96ff
    style I fill:#4d96ff
```

## Pyramid Geometry (Apex at Z=0)

```
        Z
        ↑
        * (0, 0, 0) ← Apex
       /|\
      / | \
     /  |  \
    /   |   \
   *----*----* ← Base at Z = -height
  /     |     \
 /      |      \
*-------*-------*
        ↓
     Base vertices at Z = -height
     Range: ±base/2 in X,Y
```

## Code Flow

```mermaid
flowchart TD
    START([CLI Entry]) --> PARSE[Parse Arguments]
    PARSE --> BUILD[build_ifc function]
    
    BUILD --> INIT[Initialize IFC File<br/>Schema: IFC4X3_ADD2]
    INIT --> UNITS[Create Units<br/>Meter, Radian]
    UNITS --> CTX[Create Geometric Contexts<br/>Model + Body]
    CTX --> CRS[Create ProjectedCRS<br/>EPSG:2056]
    CRS --> MAP[Create MapConversion<br/>LoGeoRef50 params]
    MAP --> PROJ[Create Project & Site]
    
    PROJ --> LOOP{For each<br/>pyramid}
    LOOP -->|coords_mode=lv95| INV[Inverse Transform<br/>LV95 → Local placement]
    LOOP -->|coords_mode=local| FWD[Forward Transform<br/>Local → LV95 pset]
    
    INV --> CREATE[Create IfcVirtualElement]
    FWD --> CREATE
    
    CREATE --> GEOM[Add Tessellated Geometry<br/>5 vertices, 6 triangles]
    GEOM --> PSET[Add ASTRA PropertySet<br/>BP coords]
    
    PSET -->|more pyramids?| LOOP
    PSET -->|done| CONTAIN[Create Containment<br/>Site ← Elements]
    CONTAIN --> WRITE[Write IFC File]
    WRITE --> END([Output File])
    
    style START fill:#90EE90
    style END fill:#FFB6C1
    style CRS fill:#87CEEB
    style MAP fill:#87CEEB
```

## Key Features

1. **Dual Coordinate Mode**: Supports both LV95-first (default) and local-first workflows
2. **Stable Numerics**: Uses inverse transform to keep local placements small
3. **Standards Compliant**: Follows LoGeoRef50 Option A specification
4. **ASTRA Integration**: Stores exact LV95 coordinates in custom property sets
5. **Closed Tessellation**: Properly oriented triangular faces (GEM001-safe)
