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
  class Model {
    +guid: string
    +code: string
    +label: LangString[]
    +comment: LangString[]
    +discipline: string
    +presentationType: string
    +format: string
    +phase: string
    +version: string
    +status: string
    +ownerOrg: string
    +responsibleParty: string
    +cdeLink: URI
  }
  class SubModel
  class DomainModel
  SubModel --|> Model
  DomainModel --|> Model

  ModelPlan "1" o-- "0..*" Model : hasModel
  Model "0..1" <-- "0..*" Model : parent   %% hierarchy for all subtypes
  ```
