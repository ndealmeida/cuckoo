# 06 - Vespa Full-Text Search: fieldsets and userQuery()

When moving from Elasticsearch to Vespa, keyword search behaves differently due to Vespa's strict schema and query parsing logic.

## 1. The `fieldset` Concept
In Elasticsearch, a search often defaults to all fields or a specific field like `body`. In Vespa, you must explicitly group fields you want to search together into a `fieldset`.

```vespa
fieldset default {
    fields: title, body
}
```
- **Why?** This allows Vespa to pre-calculate how to combine matches across different fields (e.g., giving more weight to a title match than a body match) at high speed.

## 2. The `userQuery()` Operator
Vespa's query language (YQL) is very powerful, but it's not meant to be written by end-users. `userQuery()` is a placeholder in YQL that tells Vespa: "Inject the natural language string from the `query` parameter here."

### The Difference in Logic:
- **`contains`**: Checks for an exact token or phrase. If you search for "AI Engineering" with `contains`, it might not find a document that says "AI and Engineering."
- **`userQuery()`**: Processes the input string through a tokenizer and linguistics module. It handles stemming (matching "build" with "building") and boolean logic (AND/OR).

## 3. Query Type: `any` vs `all`
- **`any` (OR):** Returns documents containing at least one of the query terms. This matches the default behavior of Elasticsearch.
- **`all` (AND):** Requires every term in the query to be present in the document.

## 4. Summary of Lexical Setup
To make lexical search work in Vespa as it does in ES, we:
1. Define a `fieldset` named `default`.
2. Use `where userQuery()` in our YQL.
3. Pass the query string in the `"query"` property of the JSON request.
4. Set `"type": "any"` to ensure broad matching.
