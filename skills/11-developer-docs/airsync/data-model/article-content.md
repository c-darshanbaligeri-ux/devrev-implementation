# Import article content and links

Source: <https://developer.devrev.ai/airsync/data-model/article-content>
Scraped: 2026-11-03

## Article content and permissions

Articles can contain Markdown or HTML and references to artifacts and other articles. Map scope, owner and `shared_with` according to the source model; content alone does not reproduce access restrictions. See [permissions](permissions.md) and the [article field reference](../supported-object-types.md#article).

## Inline article attachments

Extract source-hosted inline files as DevRev artifacts and put an artifact mention at the exact link position. Copying the content file without rewriting the article's reference leaves it dependent on the source URL and credentials.

For an external image with ID `external-image-1`, this normalized HTML content places the mention inside the image URL:

```json
[
  "<p>This article contains an image.</p><img src=\"",
  { "ref_type": "artifact", "id": "external-image-1", "fallback_record_name": "https://example.com/fallback-image.png" },
  "\" alt=\"Diagram\">"
]
```

After artifact resolution, the content has a DevRev artifact reference:

```html
<p>This article contains an image.</p>
<img src="don:core:dvrv-us-1:devo/example:artifact/1" alt="Diagram">
```

A Markdown image follows the same principle: place the artifact mention in the image destination between its opening and closing parentheses. The resolved mention value is not automatically wrapped in quotes, so the surrounding content must supply any required quoting. Ensure that attachment extraction uses the same external file ID.

## Links to other articles

Use a mention with the external article record-type key, such as `documents`, to create an internal article link. The referenced article must exist from a previous sync or be included in the current import.

```json
[
  "See <a data-article-id=\"",
  { "ref_type": "documents", "id": "external-article-2", "fallback_record_name": "Related article" },
  "\" target=\"_self\">the related article</a>."
]
```

The platform resolves the DevRev article ID and adds the appropriate link target. HTML can also appear inside Markdown article content. Keep `ref_type` tied to the external record type that maps to `article`; do not use a different type name simply because the target is an article.

## Verification

Test plain text, Markdown formatting, an imported-user mention, an unresolved mention, an inline image and a cross-article link. Confirm resolved references point to the intended DevRev objects and remain usable without source credentials. Test reverse rich text separately, including a reference lacking an external mapper.

Related contracts: [attachments](../extract-attachments.md), [object identity](../object-mappers.md), [data loading](../load-data.md).

Related: [Rich text](rich-text-fields.md).

Next: [Customize attachment processing](../customize-attachment-processing.md).
