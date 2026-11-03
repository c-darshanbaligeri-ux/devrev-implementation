# Custom objects

Source: <https://developer.devrev.ai/guides/custom-objects>
Scraped: 2026-11-03

Custom objects allow you to extend DevRev's data model beyond the standard use-cases
served by the native apps like Build and Support. Custom objects allow you to create
and manage object types tailored to your specific business needs.

## Key concepts

1. **Leaf type**: The base type of a custom object. For example, "campaign".
2. **Subtype**: A categorization of a leaf type. For example, "promotion" or "advertising" for a "campaign" leaf type.
3. **Schema fragment**: A schema fragment defines the schema for an object.
4. **Custom fields**: User-defined fields that store specific data for your custom object.
5. **ID prefix**: A unique prefix used to generate the display ID for the custom object. If the `id_prefix` is "CAMP", the generated custom object display ID is "C-CAMP-1". The display ID is used to identify the custom object in the UI, similar to the standard DevRev object display IDs like "ISS-001" for issues.

For more details on customization concepts, please refer to the
[Customization](object-customization.md) documentation.

## Custom object lifecycle

Let's say you want to manage marketing campaigns on DevRev. This guide goes through the process of creating a "Campaign" custom object with relevant fields.

All DevRev objects require a schema. First, create a schema for the "Campaign" custom object. Make sure to replace the `` with your API token.

### Create custom objects

```bash
curl --location 'https://api.devrev.ai/schemas.custom.set' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "type": "tenant_fragment",
    "description": "Attributes for Campaign",
    "leaf_type": "campaign",
    "leaf_type_display_name": "Campaign",
    "is_custom_leaf_type": true,
    "id_prefix": "CAMP"
    "fields": [
        {
            "name": "name",
            "field_type": "tokens",
            "description": "Name of the campaign"
        },
        {
            "name": "start_date",
            "field_type": "date",
            "description": "Start date of the campaign"
        },
        {
            "name": "end_date",
            "field_type": "date",
            "description": "End date of the campaign"
        },
        {
            "name": "budget",
            "field_type": "int",
            "description": "Budget allocated for the campaign"
        },
        {
            "name": "target_audience",
            "field_type": "enum",
            "description": "Target audience for the campaign",
            "allowed_values": [
                "Professionals",
                "Students"
            ]
        }
    ]
}'
```

Note that for custom object schemas, `is_custom_leaf_type` must be set to `true` to
differentiate it from standard DevRev object schemas.

Once the schema is created, you can create a custom object of type "Campaign":

```bash
curl --location 'https://api.devrev.ai/custom-objects.create' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "leaf_type": "campaign",
    "custom_schema_spec": {
        "tenant_fragment": true
    },
    "custom_fields": {
        "tnt__name": "Summer Sale 2023",
        "tnt__start_date": "2023-06-01",
        "tnt__end_date": "2023-08-31",
        "tnt__budget": 10000,
        "tnt__target_audience": "Professionals"
    }
}'
```

The response of the above API call is the ID of the custom object created.

```json {12-21}
{
  "custom_object": {
    "id": "don:core:dvrv-us-1:devo/demo:custom_object/campaign/1",
    "created_by": {...},
    "created_date": "2024-10-01T07:02:58.958Z",
    "modified_by": {...},
    "modified_date": "2024-10-01T07:02:58.958Z",
    "display_id": "C-CAMP-1",
    "leaf_type": "campaign",
    "stock_schema_fragment": "don:core:dvrv-us-1:stock_sf/1",
    "custom_schema_fragments": [
      "don:core:dvrv-us-1:devo/demo:tenant_fragment/1"
    ],
    "custom_fields": {
      "tnt__name": "Summer Sale 2023",
      "tnt__start_date": "2023-06-01",
      "tnt__end_date": "2023-08-31",
      "tnt__budget": 10000,
      "tnt__target_audience": "Professionals"
    }
  }
}
```

Note that the `id` field in the above response is the system generated unique ID for the custom object.

The sections below provide more details on the available API endpoints for interacting with custom objects.

### Get custom objects

To get a custom object, use the `custom-objects.get` endpoint:

```bash
curl --location 'https://api.devrev.ai/custom-objects.get' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "id": "don:core:dvrv-us-1:devo/demo:custom_object/campaign/1"
}'
```

### List custom objects

To list custom objects, use the `custom-objects.list` endpoint:

```bash
curl --location 'https://api.devrev.ai/custom-objects.list' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "leaf_type": "campaign",
    "filter": [
      "eq",
      "$custom_fields.tnt__target_audience",
      "Young adults"
    ]
}'
```

### Update custom objects

To update an existing custom object, use the `custom-objects.update` endpoint. The
following example updates the budget of the previously created campaign custom object:

```bash
curl --location 'https://api.devrev.ai/custom-objects.update' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "id": "don:core:dvrv-us-1:devo/demo:custom_object/campaign/1",
    "custom_fields": {
        "tnt__budget": 15000
    }
}'
```

### Delete custom objects

To delete a custom object, use the `custom-objects.delete` endpoint.
The following example deletes the previously created campaign custom object:

```bash
curl --location 'https://api.devrev.ai/custom-objects.delete' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "id": "don:core:dvrv-us-1:devo/demo:custom_object/campaign/1"
}'
```

## Extended use cases

### Reference custom objects in other objects

Let's say you want to reference all the campaigns that have been run for a customer
workspace. You can do so by adding a field of type "id" and "id\_type: custom\_object.campaign"
in the account tenant schema.

```bash {13-14}
curl --location 'https://api.devrev.ai/schemas.custom.set' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "type": "tenant_fragment",
    "description": "Tenant attributes for Account",
    "leaf_type": "account",
    "fields": [
        {
            "name": "campaigns",
            "field_type": "array",
            "base_type": "id",
            "id_type": [ "custom_object.campaign" ],
        },
        ... // other fields
    ],
}'
```

### Add subtypes to custom objects

Adding subtypes to custom objects allows you to categorize and manage your custom
objects more effectively. The process is the same as adding subtypes to other standard
DevRev objects like issues and tickets.

Let's say you have run different types of campaigns like social media and email
marketing. You can create a subtype for each of these variants. If you want to create a
campaign custom object with subtype "social\_media", you can do so as follows:

```bash {8, 17-18}
curl --location 'https://api.devrev.ai/custom-objects.create' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "leaf_type": "campaign",
    "custom_schema_spec": {
        "subtype": "social_media",
        "tenant_fragment": true
    },
    "custom_fields": {
        "tnt__name": "Summer Sale 2023",
        "tnt__start_date": "2023-06-01",
        "tnt__end_date": "2023-08-31",
        "tnt__budget": 10000,
        "tnt__target_audience": "Professionals",
        "ctype__social_media_platform": "Facebook",
        "ctype__post_id": "1234567890"
    }
}'
```

### Use unique keys for custom objects

A unique identifier for each custom object can be used to maintain idempotency
when retrying custom object creation requests. No other custom object of the
same type can have the same unique key.

```bash {10}
curl --location 'https://api.devrev.ai/custom-objects.create' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "leaf_type": "campaign",
    "custom_schema_spec": {
        "tenant_fragment": true
    },
    "unique_key": "CAMP-1",
    "custom_fields": {
        "tnt__name": "Summer Sale 2023",
        "tnt__start_date": "2023-06-01",
        "tnt__end_date": "2023-08-31",
        "tnt__budget": 10000,
        "tnt__target_audience": "Professionals"
    }
}'
```

## Access control

By default, a custom object is not accessible to anyone. This is intentional since custom objects often model sensitive domain data where unrestricted access would be inappropriate.
For example, a **financial\_record** custom object containing revenue figures, cost breakdowns, or salary data should not be accessible to all users, including admins, unless explicitly granted.

As an admin, configure object access when creating the custom object schema on the [**Settings > Object customization**](https://app.devrev.ai/?setting=object-customization) page.
The following image shows the **Object customization** page during the creation of **campaign** custom object:

*[image: custom-object-creation — see source page]*

### Field access control

By default, all users have read and write access on all fields of a custom object.
However, this is not effective until object-level access is granted and object access is restricted.

Configure field access roles in [**Settings > User Management > Roles**](https://app.devrev.ai/?setting=user-roles).
The following image shows field access configuration for the **campaign** custom object:

*[image: custom-object-field-access — see source page]*
