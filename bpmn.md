# BPMN

# Techniken

[https://www.linkedin.com/pulse/loops-bpmn-youll-finally-remember-what-iii-mean-filip-stachecki/]

[https://knowhow.visual-paradigm.com/business-process-modeling/bpmn-gateways/]


<img width="1156" height="368" alt="image" src="https://github.com/user-attachments/assets/99b2930c-9311-49c5-b586-7745f8d88978" />


<img width="850" height="262" alt="image" src="https://github.com/user-attachments/assets/21aa04f9-0f61-4a06-bb9d-0aaefe2fdc0b" />


<img width="744" height="200" alt="image" src="https://github.com/user-attachments/assets/5762194a-da55-41e2-b3d0-25035f531f2d" />


<img width="744" height="214" alt="image" src="https://github.com/user-attachments/assets/abc71fa4-4788-42e1-82f3-045cbedb3438" />

<img width="744" height="316" alt="image" src="https://github.com/user-attachments/assets/8dd2cf1f-0b3d-4731-a4ef-56c1ee7de838" />


# Example: BPMN-like Business Process with Mermaid

```mermaid
flowchart TD
  %% Roles
  subgraph Client
    C1[Start Process] 
  end

  subgraph "Business Analyst"
    BA1[Gather Requirements]
    BA2[/Document: Requirement Spec/]
    BA3([Text: Validate with Stakeholders])
  end

  subgraph "IT Department"
    IT1[Develop Solution]
    IT2((Decision: Solution Approved?))
    IT3[Update Documentation]
  end

  subgraph "Quality Assurance"
    QA1[Perform Testing]
    QA2((Decision: Pass Tests?))
    QA3[/Document: Test Report/]
  end

  subgraph "Management"
    M1[Approve Deployment]
    M2[End Process]
  end

  %% Flow
  C1 --> BA1
  BA1 --> BA2
  BA2 --> BA3
  BA3 --> IT1
  IT1 --> IT2
  IT2 -- Yes --> QA1
  IT2 -- No --> IT3
  IT3 --> IT1
  QA1 --> QA2
  QA2 -- Yes --> M1
  QA2 -- No --> IT1
  M1 --> M2
  QA1 --> QA3
```

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Team Availability - August 2025
    excludes    weekends

    section Alice
    Available       :a1, 2025-08-11, 5d
    Vacation        :a2, 2025-08-18, 3d

    section Bob
    Sick Leave      :b1, 2025-08-11, 2d
    Available       :b2, 2025-08-13, 7d

    section Carol
    Available       :c1, 2025-08-11, 10d
```
