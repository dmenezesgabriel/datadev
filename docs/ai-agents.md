# AI Agents

AI agents are simply workflows, or DAGs, or just graphs if included on a loop. Most steps in these workflows should be regular code, not LLM calls.

## Fundamental Building Blocks

### 1. Intelligence

This is the only truly **AI** component. Without it you just have regular software.

```mermaid
flowchart LR
user["`User input`"]
llm["`LLM Processing`"]
response["`Generated response`"]


user --> llm --> response
```

- [Notebook](notebooks/python/generative-ai/llm-completion.ipynb)

### 2. Memory

LLMs don't remember anything from previous messages. Without memory, each interaction starts from scratch because LLMs are stateless.

### 3. Tools

The LLM call itself is limited just to text, but you want to do more than that, such as API calls and interact with databases.

### 4. Validation

LLMs are probabilistic and can produce inconsistent outputs, make sure that the LLM return structured output A.K.A JSON format that matches your expected schema. If does not you can send it back to the LLM to fix it. Most commonly used tools are **Pydantic** (Python) and **Zod**: (Javascript).

## AI Agents vs. Workflows

| Feature                       | 🟢 Agent                                 | 🔴 Workflow                                    |
| :---------------------------- | :--------------------------------------- | :--------------------------------------------- |
| **How many LLM calls?**       | Many                                     | Many                                           |
| **Who decides when to stop?** | The LLM                                  | Predetermined Steps                            |
| **Good for?**                 | When the path to the solution is unclear | When the path to the solution is known upfront |

## References

- [Video - building-effective-agents, Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Video - How to Build Reliable AI Agents](https://www.youtube.com/watch?v=T1Lowy1mnEg&t=478s)
- [Video - Most devs don't understand what agents are](https://www.youtube.com/watch?v=AtYtuVTZCQU)
