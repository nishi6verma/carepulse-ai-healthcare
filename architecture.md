# CarePulse architecture (concept)

```mermaid
flowchart LR
    A[Authorised patient data sources] --> B[API / event ingestion]
    B --> C[Validation and normalisation]
    C --> D[Clinical rules + validated model]
    D --> E[Priority worklist and alert service]
    E --> F[Clinician review]
    F --> G[Audit log and feedback]
    G --> D
    H[IBM Z / LinuxONE target platform] -. potential hosting .-> B
    H -. potential hosting .-> D
    H -. potential hosting .-> E
```

The current application is a local Streamlit prototype using synthetic records. The diagram shows a proposed target architecture, not an existing IBM deployment. Any clinical model, thresholds, or workflow must be validated and governed by qualified healthcare professionals before use.
