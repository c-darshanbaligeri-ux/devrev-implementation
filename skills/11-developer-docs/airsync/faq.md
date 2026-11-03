# Find and troubleshoot sync failures

Source: <https://developer.devrev.ai/airsync/faq>
Scraped: 2026-11-03

Choose the page for the failing phase. Check its symptom and fix, then rerun the affected operation.

| Area                 | Troubleshooting                                                          |
| -------------------- | ------------------------------------------------------------------------ |
| Deployment           | [Deployment troubleshooting](deployment-troubleshooting.md)        |
| Extraction           | [Extraction troubleshooting](extraction-troubleshooting.md)        |
| Mapping and identity | [Mapping and identity troubleshooting](mapping-troubleshooting.md) |
| Runtime              | [Runtime troubleshooting](runtime-troubleshooting.md)              |
| Attachment           | [Attachment troubleshooting](attachment-troubleshooting.md)        |

## Symptoms

### Deployment version never becomes ready

See [Deployment troubleshooting](deployment-troubleshooting.md).

### Package slug conflict

See [Deployment troubleshooting](deployment-troubleshooting.md).

### CLI token expired or wrong organization selected

See [Deployment troubleshooting](deployment-troubleshooting.md).

### Connection passes verification but extraction is unauthorized

See [Extraction troubleshooting](extraction-troubleshooting.md).

### Fixture completes but records are wrong or missing

See [Extraction troubleshooting](extraction-troubleshooting.md).

### Only the first API page is imported

See [Extraction troubleshooting](extraction-troubleshooting.md).

### Incremental sync misses records or reimports everything

See [Extraction troubleshooting](extraction-troubleshooting.md).

### Metadata and normalized records disagree

See [Mapping and identity troubleshooting](mapping-troubleshooting.md).

### Required fields are missing after mapping

See [Mapping and identity troubleshooting](mapping-troubleshooting.md).

### Duplicate records or repeated reverse-sync writes

See [Mapping and identity troubleshooting](mapping-troubleshooting.md).

### Worker emits twice or never finishes

See [Runtime troubleshooting](runtime-troubleshooting.md).

### SDK upgrade compiles but behavior changed

See [Runtime troubleshooting](runtime-troubleshooting.md).

### Attachments absent while records are present

See [Attachment troubleshooting](attachment-troubleshooting.md).
