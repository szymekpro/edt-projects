# Project 2 – Semantic search and knowledge extraction

> Status: **requirements only** – no code in the repository yet.

## 1. Goal

Design and implement a GUI application that supports:

- a **text document collection**,
- **multiple search methods**,
- automatic **named entity recognition (NER)**.

Integrate:

1. document management,
2. keyword search,
3. TF-IDF search,
4. semantic search,
5. entity recognition in documents.

## 2. Document collection

| ID | Requirement |
|----|-------------|
| P2-DB-01 | Add documents in **TXT and PDF**. |
| P2-DB-02 | **Automatic reading and processing** of content. |
| P2-DB-03 | **Store documents and metadata.** |
| P2-DB-04 | **Browse** documents. |
| P2-DB-05 | **Delete** documents. |
| P2-DB-06 | **Automatic preparation** for search and NER (indexing, embeddings, NER on ingest, etc.). |

## 3. Search module

Three methods:

| ID | Method | Description |
|----|--------|-------------|
| P2-S-01 | Keywords | Documents containing given **words or phrases**. |
| P2-S-02 | TF-IDF | **Rank** by textual similarity. |
| P2-S-03 | Semantic | Documents **similar in meaning** to the query. |

Result and UI requirements:

| ID | Requirement |
|----|-------------|
| P2-S-04 | Each hit: **document name**, **match score**, **snippet** related to the query. |
| P2-S-05 | User can **open** the full document. |
| P2-S-06 | **One query** → **side-by-side** keyword, TF-IDF, and semantic results. |
| P2-S-07 | Show **ranking differences** between methods. |
| P2-S-08 | Filter search results by **entity** or **entity type** (NER integration). |

## 4. NER module

Detect at least:

- **Persons**
- **Organizations**
- **Locations**
- **Dates and time periods**
- **Other types** supported by the chosen model

| ID | Requirement |
|----|-------------|
| P2-N-01 | Automatic detection of the above types. |
| P2-N-02 | Show entities with **types** and **text spans**. |
| P2-N-03 | **Visual highlighting** in the document view. |
| P2-N-04 | **Search entities** and list documents containing them. |
| P2-N-05 | Filter search (section 3) by entity/type (= P2-S-08). |

## 5. Graphical user interface

Three main views:

| View | Content |
|------|---------|
| **Document base** | Add, browse, delete. |
| **Search** | Method choice and results. |
| **NER** | Entity list, filter by type, documents per entity. |

| ID | Requirement |
|----|-------------|
| P2-G-01 | All three views. |
| P2-G-02 | **Document details**, metadata, and **highlighted entities** from list or search results. |

## 6. Priorities (from assignment)

- **Text processing and exploration** matter more than UI polish or architecture.
- **Most important:** **compare** keyword, TF-IDF, and semantic search.
- Enable **comparing rankings** across methods.

## 7. Optional extensions

| ID | Extension |
|----|-----------|
| P2-X-01 | Panel of **top entities** (people, orgs, locations). |
| P2-X-02 | Stats: **document count**. |
| P2-X-03 | Stats: **text lengths**. |
| P2-X-04 | Stats: **frequent terms**. |
| P2-X-05 | Stats: **entity type distribution**. |
| P2-X-06 | Visualize ranking differences between methods. |

## 8. Done criteria

- [ ] TXT/PDF ingest, metadata, browse, delete.
- [ ] Automatic prep for search and NER.
- [ ] Three search methods with name, score, snippet.
- [ ] Comparative view: one query → three result columns.
- [ ] Ranking comparison.
- [ ] NER: persons, orgs, locations, dates (+ model types).
- [ ] Entity highlighting in document view.
- [ ] Entity search and search filtered by entity/type.
- [ ] Three GUI views + document details.
- [ ] (Optional) top entities panel and statistics.

## 9. Open decisions

- Document language (PL / EN) → NER and embedding models.
- NER model (spaCy, HuggingFace, etc.) and embeddings (e.g. sentence-transformers).
- Storage: SQLite + files vs folder + JSON; vector index (FAISS / numpy).
- GUI technology.
