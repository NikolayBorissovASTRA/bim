Mermaid supports three graph orientations: Left-to-Right (default), Top-to-Bottom, and Bottom-to-Top.

You can set this with either LR: (for Left-to-Right), TB: (for Top-to-Bottom) or BT: (for Bottom-to-Top) after gitGraph.

| Symbol    | Relationship Type | Description         |
|-----------|-------------------|---------------------|
| `<|--`    | Inheritance       | Represents a "is-a" relationship (generalization) where one class inherits from another. |
| `*--`     | Composition       | Strong "has-a" relationship; the child cannot exist independently of the parent. |
| `o--`     | Aggregation       | Weak "has-a" relationship; the child can exist independently of the parent. |
| `-->`     | Association       | Indicates a relationship between classes where objects interact. |
| `--`      | Link (Solid)      | A solid line link, often used for a generic connector. |
| `..>`     | Dependency        | Shows that a class depends on another (uses, but does not own or inherit). |
| `..|>`    | Realization       | Denotes that a class implements an interface (realization). |
| `..`      | Link (Dashed)     | A dashed line link, typically used for less strong relationships or notes. |


The different cardinality options are:

| Symbol  | Meaning              | Description                              |
|---------|----------------------|------------------------------------------|
| 1       | Only 1               | Exactly one instance; mandatory.         |
| 0..1    | Zero or One          | Optional; at most one instance.          |
| 1..*    | One or more          | At least one instance; no upper limit.   |
| *       | Many                 | Zero or more instances; no upper limit.  |
| n       | n (where n > 1)      | Exactly n instances, where n > 1.        |
| 0..n    | Zero to n (n > 1)    | Any number from zero up to n (n > 1).    |
| 1..n    | One to n (n > 1)     | At least one and at most n (n > 1).      |

