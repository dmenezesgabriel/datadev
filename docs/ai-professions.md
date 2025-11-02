# Professions

```mermaid
graph TD
    subgraph Data/Research constrained
        MR[ML Researcher / Research Scientist]
        MLED[ML Engineer/ Data Scientist/ Research Engineer]
    end

    subgraph Product/User constrained
        AIE[AI Engineer]
        FE[Fullstack Engineer]
    end

    subgraph Focus Areas
        T(training)
        E(evals)
        I(inference)
        D(data)
        C(chains/agents)
        TI(tooling & infra)
        P(product)
        PL(platform)
    end

    MR --- MLED
    MLED -- API --> AIE
    AIE --- FE

    MR --> T
    MR --> E

    MLED --> I
    MLED --> D

    AIE --> C
    AIE --> TI

    FE --> P
    FE --> PL
```
