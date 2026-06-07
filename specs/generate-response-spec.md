# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Include the retrieved_chunks in order where each chuck are labeled with [Game: <Game>](dist: DISTANCE:.3f) <CHUNK TEXT> --- Use '---' as delimiter.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
"You are an assistant that must only use the provided CONTEXT blocks to answer the user's question. Do NOT hallucinate or use any outside knowledge. If the answer cannot be fully determined from the context, say you don't know and cite the missing information explicitly."
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
"When you provide a factual statement, immediately follow it with a short citation in square brackets naming the source game, e.g. [Source: Catan]. If the answer uses multiple chunks from different games, list all cited games in a comma-seperated bracket, e.g. [Sources: Catan, Monopoly]."
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
"I couldn't find a clear answer in the loaded rule books. Try rephrasing your question or check that the relevent rule book is loaded."
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
Filter out chunks with distance > 0.50 before building the context. If no chunks remain, return the fallback message. Tradeoffs: This reduces hallucination risk but may drop partial evidance; I will later experiment with the threshold or pass all chunks with distances included.
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
Use one system message containing the grounding + citation instructions. Use the user message to include the original query followed by formatted CONTEXT block (all chunk blocks).
Example user content:
"Question: <user query>\n\nCONTEXT:\n<chunk blocks>\n\nAnswer the question using ONLY the CONTEXT above."
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [your test query]
Response: [abbreviated response]
Correctly grounded? [yes / no]
Cited the right game? [yes / no]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[your answer here]
```
