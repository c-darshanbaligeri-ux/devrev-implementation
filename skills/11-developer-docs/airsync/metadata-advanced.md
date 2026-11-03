# Describe categories, conditions and stages

Source: <https://developer.devrev.ai/airsync/metadata-advanced>
Scraped: 2026-11-03

Use these schema features when the external system has dynamic record types, fields that depend on other values or a workflow with stages. Start with the basic [external schema](external-domain-metadata.md) and [field definitions](metadata-fields.md).

## Categories

A category can declare `are_record_type_conversions_possible` when a record can move between its types without changing identity. Use category mappings when dynamic record types should inherit consistent [initial mapping](initial-domain-mapping.md).

## Conditional fields

Conditions are keyed by a controlling field. Each condition provides `value`, comparator `eq` or `ne`, `affected_fields` and effect `require` or `show`. These describe the external schema's conditional fields; they are different from authorization-policy conditions.

## Workflow stages

A stage diagram declares `controlling_field`, a map of `stages`, optional `starting_stage`, custom `states`, and `all_transitions_allowed`. Stage keys must match the controlling enum field's values. Each stage can name a state and `transitions_to`; custom state definitions supply name, end-state flag and ordinal. Built-in state names include `open`, `in_progress` and `closed`.

## Verify the schema

Check that category keys exist, condition fields and affected fields are declared, and stage keys match the controlling enum. Test a new dynamic type and a stage transition in an import.

If your source does not need these features, keep the basic schema and continue with its metadata worker.

Next: [Extract and upload schema metadata](metadata-extraction.md).
