# Troubleshoot attachment imports

Source: <https://developer.devrev.ai/airsync/attachment-troubleshooting>
Scraped: 2026-11-03

Use these checks when the connector fails during attachment.

## Attachments absent while records are present

Check parent IDs/mappers, attachment metadata, download permissions, signed URL expiry and stream results. A successful record import does not prove its attachment URL is readable. Test partial failure and retry without buffering the entire file in memory. See [attachment extraction](extract-attachments.md) and [attachment loading](load-attachments.md).

Related: [troubleshooting index](faq.md).
