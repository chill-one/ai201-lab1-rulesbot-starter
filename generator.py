from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """

    prompt = "You are a board-game rules assistant. Answer only using the provided CONTEXT blocks and do not use outside knowledge. If the answer cannot be fully determined from the context, say you do not know. When you provide a factual statement, immediately follow it with a short citation in square brackets naming the source game, e.g. [Source: Catan]. If the answer uses multiple chunks from different games, list all cited games in a comma-separated bracket, e.g. [Sources: Catan, Monopoly]."

    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )
    
    filter_chunck = [chunk for chunk in retrieved_chunks if chunk["distance"] <= 0.50]

    if not filter_chunck:
      return (
          "I couldn't find anything relevant in the loaded rule books. "
          "Try rephrasing your question — or check that your ingestion pipeline is working."
      )
    
    context = []

    for chunck in filter_chunck:
       context.append(f"[Game: {chunck['game']}] (dist: {chunck['distance']:.3f})\n{chunck['text']}")

    context_text = "\n---\n".join(context)


    messages = [
       {
          "role":"system",
          "content":prompt,
       },
       {
          "role": "user",
          "content": f"Question: {query}\n\nCONTEXT:\n{context_text}\n\nAnswer the question using only the CONTEXT above.",
       }
    ]

    response = _client.chat.completions.create(
      model=LLM_MODEL,
      messages=messages,
    )

    # Your implementation here.
    return response.choices[0].message.content.strip()
