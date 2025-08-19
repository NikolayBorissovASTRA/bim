Mermaid supports three graph orientations: Left-to-Right (default), Top-to-Bottom, and Bottom-to-Top.

You can set this with either LR: (for Left-to-Right), TB: (for Top-to-Bottom) or BT: (for Bottom-to-Top) after gitGraph.

Type	Description
<|--	Inheritance
*--	Composition
o--	Aggregation
-->	Association
--	Link (Solid)
..>	Dependency
..|>	Realization
..	Link (Dashed)


```mermaid
classDiagram
  direction TB

  class ModelPlan {
    +guid: string
    +code: string
    +label: LangString[]
    +comment: LangString[]
    +version: string
    +status: string
  }

  class Model {
    +guid: string
    +code: string
    +label: LangString[]
    +comment: LangString[]
    +role: ModelRole          // Federated|Domain|Sub
    +discipline: string       // enum (e.g., TRA, STR, WLK, UMG, BSA, ...)
    +presentationType: string // enum
    +format: string           // enum
    +phase: string            // enum
    +ownerOrg: string
    +responsibleParty: string
    +version: string
    +status: string
    +cdeLink: URI
    +createdAt: datetime
    +modifiedAt: datetime
  }

  class LangString {
    +lang: string
    +value: string
  }

  class ModelRole {
  }

  ModelPlan "1" o-- "0..*" Model : hasModel
  Model "0..1" <-- "0..*" Model : parent
  Model --> "0..*" LangString : label
  Model --> "0..*" LangString : comment
  ```
