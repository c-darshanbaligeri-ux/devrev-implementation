# Ask the Agent Guides

Ask any question about building, debugging, or improving DevRev AI agents. The knowledge base will be consulted to provide expert answers.

When your answer touches **retrieval** (ART-30502):

- **FetchObjectContext** — Explain that when the user or context provides a concrete **object id**, the agent should fetch that object directly before broad search.
- **HybridSearch** — Use this name for scoped search over configured knowledge (articles, objects, etc.). If discussing a user-named skill (e.g. `search_docs`), say it is implemented with **HybridSearch** unless the architecture is different.
- **Priority** — Default order: FetchObjectContext when an id is known → targeted tools → HybridSearch for discovery → NL2SQL only when the agent is built for structured data queries (and annotations exist).

See `CLAUDE.md` → "Naming retrieval in agent designs" and `/agent-create` for how writeups should name these mechanisms.

$ARGUMENTS
