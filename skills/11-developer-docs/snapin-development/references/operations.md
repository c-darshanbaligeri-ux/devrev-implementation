# Snap-in operations

Source: <https://developer.devrev.ai/snapin-development/references/operations>
Scraped: 2026-11-03

An operation exposes a snap-in function as a reusable step in workflows or agents. Its manifest entry describes what the operation does, which function executes it, the inputs and outputs available to its caller, and the permissions and connections it requests. Install and activate the snap-in to make its exposed operations available.

## Define an operation

Add an entry to `operations` in the version 2 snap-in manifest. This example formats text without calling DevRev or an external service, so both scope declarations are explicitly empty:

```yaml
version: "2"
name: Text formatter
description: Format text for workflows.

service_account:
  display_name: Text formatter
  scopes:
    self: []

functions:
  - name: operation_handler
    description: Run text formatting operations.

operations:
  - name: uppercase_text
    display_name: Uppercase text
    description: Convert the supplied text to uppercase.
    slug: uppercase_text
    function: operation_handler
    type: action
    metadata:
      is_workflow_node: true
      is_agent_skill: true
    static_scopes:
      self: []
    inputs:
      fields:
        - name: text
          field_type: text
          is_required: true
          description: Text to convert.
          ui:
            display_name: Text
    outputs:
      fields:
        - name: result
          field_type: text
          description: Uppercase text.
          ui:
            display_name: Result
```

The main operation properties are:

| Field                            | Purpose                                                                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                           | Nonempty name, unique among operations in the snap-in.                                                                                |
| `display_name` and `description` | Label and explanation presented to builders. Describe the action, expected inputs, and meaningful side effects.                       |
| `slug`                           | Unique identifier used to route invocations to the handler.                                                                           |
| `function`                       | Name of a function declared under `functions` and implemented in the snap-in code. Multiple operations may share a handler.           |
| `type`                           | Only `action` is supported for external snap-in operations. Custom `trigger`, `control`, and `blocking` operations are not supported. |
| `inputs` and `outputs`           | Field definitions for the values accepted and returned. Declare both keys, even if an operation has no fields (`fields: []`).         |
| `metadata`                       | Controls whether an action is exposed as a workflow node, agent skill, or MCP tool.                                                   |
| `static_scopes`                  | DevRev permissions requested by this operation when used in a workflow or agent; separate from the snap-in service account's scopes.  |
| `keyrings`                       | Connections needed by this operation to access external services.                                                                     |
| `execute_options` and `methods`  | Optional execution settings and lifecycle or dynamic-schema methods.                                                                  |

Do not set `namespace` on an external operation; DevRev assigns it. Keep operation names and slugs unique, and ensure `function` matches a declared function.

## Describe inputs and outputs

Each `inputs.fields` entry defines a field in the builder's form. Each `outputs.fields` entry describes a value that subsequent steps or an agent can use. An operation supports one input port and one output port. Give fields stable names and descriptive labels; values returned by the handler must match the declared output names and types.

Fields can use types such as `text`, `int`, `bool`, `enum`, `id`, `rich_text`, `array`, and `composite`. Use `is_required` and `default_value` for input behavior, `allowed_values` for an enum, `id_type` for a DevRev object reference, and `base_type` for an array. For structured values, declare a composite under `inputs.composites` or `outputs.composites` and reference it with `field_type: composite` and `composite_type`.

For example, an operation that queries an external service can accept a required schedule ID and a site selected from an enum. It can return structured data through a composite output:

```yaml
inputs:
  fields:
    - name: schedule_id
      field_type: text
      is_required: true
      ui:
        display_name: Schedule ID
    - name: site
      field_type: enum
      allowed_values: [US1, EU]
      default_value: US1
      ui:
        display_name: Site
outputs:
  composites:
    - name: shift
      fields:
        - name: start
          field_type: text
        - name: end
          field_type: text
  fields:
    - name: on_call_shift
      field_type: composite
      composite_type: shift
      ui:
        display_name: On-call shift
```

The example above is an `inputs` and `outputs` excerpt from an operation entry, not a complete manifest. When no inputs are needed, use `inputs: { fields: [] }`; declare `outputs` as well, even if its fields are empty.

### Dynamic fields and validation

If fields depend on a builder's selections, declare a `schema_handler` method on the operation. The handler returns the input and output ports appropriate for the selected values. A `validate` method can report configuration errors before the operation runs. For example, an HTTP operation can derive output fields from a sample response and validate that the sample is valid JSON:

```yaml
methods:
  - name: schema_handler
  - name: validate
```

These are operation-level methods, not separate entries under `functions`. The function named by `operations[].function` receives the invocation; route it by `event.execution_metadata.operation_method` to `schema_handler`, `validate`, or the normal `run` method. Keep `inputs` and `outputs` in the manifest even when a schema handler supplies their fields dynamically.

## Choose the available surfaces

For an action, use `metadata` to mark the surfaces where builders can use it:

```yaml
metadata:
  is_workflow_node: true
  is_agent_skill: true
  is_mcp_tool: false
```

* `is_workflow_node`: Exposes the action in Workflow Builder.

* `is_agent_skill`: Makes the action available as an agent skill.

* `is_mcp_tool`: Exposes the action as an MCP tool. If enabled, provide `mcp_hints` that describe whether it is destructive, idempotent, open-world, or read-only.

You can set more than one surface to `true`. Use these flags instead of the deprecated `is_tool` field. For an action with a `metadata` block, enabling none of these surfaces logs a validation warning. Declare the surfaces on which builders should find the operation. For a read-only MCP tool, the annotations can look like this:

```yaml
metadata:
  is_mcp_tool: true
  mcp_hints:
    destructive_hint: false
    idempotent_hint: true
    open_world_hint: false
    read_only_hint: true
```

Set the hints to match the operation's actual behavior; they describe the tool, not the DevRev permissions it requests.

## Declare permissions separately

The snap-in manifest has two distinct permission declarations:

* `service_account.scopes`: Access needed by the snap-in's own service account for its functions and other snap-in behavior.

* `operations[].static_scopes`: Access requested by a particular operation when a workflow or agent uses it. Each operation declares its own permissions; these are not inherited from `service_account.scopes`.

If the snap-in function and its operation both need to read issues, declare `issue:read` in both places. An operation that writes tickets can request `ticket:write`, while an operation that only formats text can declare `static_scopes: { self: [] }`. Even an operation that requests no DevRev permissions needs an explicit `static_scopes` declaration for scope-enforced snap-ins.

Under `static_scopes`, use `self` for access needed by the workflow or agent's execution identity. If the operation acts on behalf of a user, use `impersonation` with an `act_as` value and nested scopes. The corresponding key under `service_account.scopes` is spelled `impersonate`, not `impersonation`:

```yaml
static_scopes:
  impersonation:
    - act_as: all_devusers
      scopes:
        - scope: issue:read
          optional: false
          reason: Read issues on behalf of the user.
```

Supported `act_as` values are `all_devusers`, `all_revusers`, and `devusers_explicit`. See [Snap-in scopes](scopes.md) for permission levels, optional scopes, and the API-to-scope mapping.

## Add connections and execution settings

An operation can declare `keyrings` for the external credentials its handler needs. Define the connection type and present the appropriate keyring for selection when the operation is configured. The handler receives selected credentials in `resources.keyrings`:

```yaml
keyrings:
  - name: external_api_key
    display_name: External API key
    description: Credential for the external API.
    types:
      - snap_in_secret
```

This is a per-operation `keyrings` excerpt. Do not place secrets in the manifest or log them from the handler. A snap-in that uses an external API but no DevRev API can still declare `static_scopes: { self: [] }`; the keyring provides an external credential, not a DevRev scope.

Use `execute_options.default_timeout` for a longer-running operation. `default_timeout` and `max_execution_timeout` must each be between 10 and 300 seconds. If you specify `max_execution_timeout`, set `is_timeout_configurable: true`, and keep the default no greater than the maximum:

```yaml
execute_options:
  default_timeout: 120
  is_timeout_configurable: true
  max_execution_timeout: 180
```

## Implement and route the handler

Create a folder for the declared function, such as `src/functions/operation_handler/`. Its exported `run` function receives an array of events. Read `payload.metadata.slug` to select the operation, `payload.data` for the input values, and `event.input_data.resources` for selected connections. Return an `OperationOutput` whose `output.values` entry matches the manifest's output fields, or return a typed error.

For the `uppercase_text` manifest above, `src/functions/operation_handler/index.ts` can contain:

```typescript
import {
  Error_Type,
  ExecuteOperationInput,
  FunctionInput,
  OperationOutput,
} from '@devrev/typescript-sdk/dist/snap-ins';

export const run = async (events: FunctionInput[]): Promise<OperationOutput> => {
  const input = events[0].payload as ExecuteOperationInput;

  if (input.metadata?.slug !== 'uppercase_text') {
    return OperationOutput.fromJSON({
      error: { message: 'Unknown operation', type: Error_Type.InvalidRequest },
    });
  }

  const text = (input.data as { text?: string }).text;
  if (typeof text !== 'string') {
    return OperationOutput.fromJSON({
      error: { message: 'Text is required', type: Error_Type.InvalidRequest },
    });
  }

  return OperationOutput.fromJSON({
    output: { values: [{ result: text.toUpperCase() }] },
  });
};

export default run;
```

For multiple operations, dispatch by `slug` in the handler or map each slug to a class extending `OperationBase`. An `OperationBase` implementation receives `context`, `input`, and `resources` in its `run` method. Use `context.devrev_endpoint` and `context.secrets.access_token` for DevRev API access; read an operation-level secret from `resources.keyrings.<name>.secret`. Validate required inputs, handle API failures, and return field values that match the declared output schema.

Test a successful invocation and error cases with local fixtures before deploying the snap-in. For a complete sample project, see the [snap-in operations example](https://github.com/devrev/snap-in-examples/tree/main/14-operations). The [locally testing snap-ins](../locally-testing-snap-ins.md) guide covers running a handler during development.
