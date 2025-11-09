# Large Language Models - Evaluation

- Besides factual accuracy, is the tone of voice ok?
- How will this behave with real users inputs we haven't seen yet?
- How do we know when the system performance is degrading in production?
- Is our system robust enough to flag prompt injections?

**Core question**: How can we effectively evaluate AI system performance and identify specific areas where improvements are needed?

## Core challenges

- Inconsistent Behavior: Your LLM works great on test cases, but then behaves unpredictably on real user inputs. Small changes in wording can lead to completely different outputs, making your system feel unreliable.

## Success

- Evaluate: Quality: Systematic measurement of your workflow's performance through automated tests, human evaluation, and success metrics.
- Debug Issues: Tools to understand and diagnose failures including trace logging, data inspection and error analysis.
- CHange behavior: Technics to improve your system based on insights from evaluation and debugging.

## What is Evaluation?

Systematic measurement of quality in an AI System

An **Eval** is a single metric that measures a specific aspect of performance

- Factual accuracy
- Tone appropriateness
- Following instructions
- Output format compliance

**Evals** can be operationalized as:

- Background Monitoring: Track performance over time
- Guardrails: Block bad outputs in real-time
- Improvement Tools: Label data for fine-tunning

## The three levels of Evaluation

### 1. Unit tests

Fast, cheap assertions that runs on every code change

- Run: Every commit
- Cost: Very low

Example:

```py hl_lines="7-11" title="test_categorization.py"
def test_ticket_categorization():
    ticket = "My credit card was charged twice this month"

    # Using structured llm output
    result = categorize_ticket(ticket)

    assert result.category in ["billing", "technical", "general"]
    assert isinstance(result.confidence, float)
    assert 0 <= result.confidence <= 1

    assert result.category == "billing"
```

- [Cookbook - Evaluation - Unit Testing](./notebooks/python/generative-ai/evaluation-unit-test.md)

#### When to use

- Data cleaning and validation
- Automatic retries with feedback
- CI/CD workflows
- Catching obvious failures

### 2. Human & Model Evaluation

Systematic review and automatic critique of quality

- Run: Weekly/Biweekly
- Cost: Medium

#### Human Evals

Humans look at system outputs and score them

- Start with binary: Good/Bad

#### Model Evals (LLM as Judge)

Use a LLM to critique your system's outputs

- Generate detailed critiques, not just scores
- Must be aligned with human judgement

Example Prompt:

```txt
Evaluate this customer service response on these criteria:

1. Accuracy: Are the facts correct?
2. Helpfulness: Does it solve the customer's problem?
3. Tone: Is it professional and empathetic?

Provide a detailed critique explaining your reasoning, then rate 1 (Good) or 0 (Bad).
```

Excel worksheet:

| Input | Model Response | Model Critique (Judge) | Model Outcome | Human Critique       | Human Outcome | Alignment | Agreement |
| ----- | -------------- | ---------------------- | ------------- | -------------------- | ------------- | --------- | --------- |
| ...   | ...            | Detailed explanation   | Good/Bad      | Detailed explanation | Good/Bad      | 0/1       | 90%       |

### 3. A/B Testing

Real user experiments to measure business impact

- Run: Major releases
- Cost: High

#### When to use A/B Tests

- System is mature and stable
- You want to measure real user impact
- Testing significant changes
- Need business metric validation
- Comparing different approaches

#### What to measure

- User satisfaction scores
- Task completion rates
- Time to resolution
- User engagement metrics
- Business outcomes (sales, retention)

#### Example: Prompt Comparison

**Hypothesis**: A more conversational prompt will improve user satisfaction

Setup:

- Control (A): Formal, direct responses
- Treatment (B): Conversational, empathetic tone

Results and metrics:

**Metrics**:

- User satisfaction rating (1-5)
- Conversation completion rate
- Follow-up questions needed

**Result**: Treatment B increases satisfaction by 15% with no decrease in accuracy

## Types of Evaluation Metrics

### Reference-Based

Compare LLM output against known "**golden**" answers

- Exact string matches
- Semantic similarity
- Code execution results
- SQL query correctness
- Structured data validation

### Reference-Free

Evaluate inherent properties without "**golden**" answers

- Tone appropriateness
- Length constraints
- No hallucination
- Format compliance
- Safety and toxicity

## Are you succeeding?

- You can deploy changes confidently
- Failures are caught before users see them
- You understand your systems behavior

## References

- [Video - Why Most AI Projects Fail and How to Fix It, Dave Ebbelaar](https://www.youtube.com/watch?v=a3SMraZWNNs&t=18s)
- [Docs - MLFlow LLM Evaluation Examples](https://mlflow.org/docs/2.9.1/llms/llm-evaluate/notebooks/index.html)
