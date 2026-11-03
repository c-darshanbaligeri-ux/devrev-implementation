# Import and export rich text

Source: <https://developer.devrev.ai/airsync/data-model/rich-text-fields>
Scraped: 2026-11-03

## Normalized rich text contract

Rich text is an array containing text strings and mention objects. A plain Markdown value is still wrapped in an array:

```json
["Hello **world**!"]
```

Markdown must conform to [CommonMark 0.30](https://spec.commonmark.org/0.30/). Keep the target's content format consistent; article fields can support Markdown or HTML, whereas not every rich-text field accepts arbitrary HTML.

```json
[
  "Hello ",
  { "ref_type": "users", "id": "external-user-1", "fallback_record_name": "Jane Doe" },
  ", please review this task."
]
```

| Mention field          | Required | Meaning                                                           |
| ---------------------- | -------- | ----------------------------------------------------------------- |
| `id`                   | Yes      | External identity of the referenced record                        |
| `ref_type`             | Yes      | Referenced external record-type key, resolved through its mapping |
| `fallback_record_name` | No       | Text used if the reference cannot be resolved                     |

Emit the referenced user or object, or ensure it was synchronized previously. Do not predict its DevRev ID while normalizing extraction data. Test unresolved references with a useful fallback instead of depending on accidental display behavior.

## Reverse rich-text payload

During loading a transformed rich-text field can be wrapped as:

```json
{
  "type": "rich_text",
  "content": [
    "Hello ",
    {
      "ref_type": "users",
      "id": "don:identity:dvrv-us-1:devo/example:devu/1",
      "fallback_record_name": "Jane Doe"
    }
  ]
}
```

The reference in a reverse payload can be a DevRev ID. Resolve it through [object mappers](../object-mappers.md) before sending an external mention or URL. Denormalize the text into the external API's actual accepted format. Keep a fallback for references that cannot be represented externally; do not send DevRev DONs as external user identifiers.

## Content invariants and failure behavior

Preserve formatting, escapes and link boundaries when splitting content around mentions. Escape external attributes and text according to the destination format. Do not place raw secrets or source-authentication parameters in exported HTML or fallback URLs.

If an inline artifact is missing or fails extraction, verify the fallback and report the failure rather than claiming that the article is fully portable. If a referenced article was filtered out of the import, verify the resulting link behavior. A rendered paragraph alone does not establish successful reference resolution.

<span id="article-content-and-permissions" />

Related:

* [Article content and links](article-content.md).

Next: [Import article content and links](article-content.md).
