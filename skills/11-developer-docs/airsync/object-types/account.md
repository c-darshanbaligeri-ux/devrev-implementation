# account fields

Source: <https://developer.devrev.ai/airsync/object-types/account>
Scraped: 2026-11-03

Field reference for the `account` target. Required fields must be mapped or have a supported creation fallback.

Catalog generated July 13, 2026. Validate the mapping in your target organization. Can Load means external → DevRev; Can Extract means DevRev → external. See [field rules](../object-field-contract.md) for required values and references.

**Resource Type:** `account`

**Capabilities:** Can App Fragment, Can Load

## Fields

| Field                 | Type                                       | Required | Description                                                                                  |
| --------------------- | ------------------------------------------ | -------- | -------------------------------------------------------------------------------------------- |
| `address`             | struct                                     |          | Address of the Organization.                                                                 |
| `airsync_shared_with` | permission (collection)                    |          | List of users and groups who have explicit access to the item and the corresponding roles.   |
| `created_by_id`       | reference → \[#category:user]              |          | User ID of the user that created the object.                                                 |
| `description`         | rich\_text                                 |          | Description of the corresponding Account.                                                    |
| `display_name`        | text                                       | ✔︎       | Name of the Organization.                                                                    |
| `environment`         | enum                                       |          | The environment of the Org. Defaults to 'production' if not specified.                       |
| `external_refs`       | text (collection)                          |          | External refs are unique identifiers from your customer system of records, stored as a list. |
| `industry`            | enum                                       |          | Industry of the company.                                                                     |
| `item_url_field`      | text                                       |          | Link to the item in the origin system.                                                       |
| `lead_source`         | enum                                       |          | The source that connected/introduced/referred the company.                                   |
| `modified_by_id`      | reference → \[#category:user]              |          | User ID of the user that last modified the object.                                           |
| `owned_by`            | reference (collection) → \[#category:user] | ✔︎       | List of Dev user IDs owning this Account.                                                    |
| `phone_number`        | struct (collection)                        |          | Phone numbers of the Organization.                                                           |
| `phone_numbers`       | text (collection)                          |          | Phone numbers of the Organization.                                                           |
| `state`               | enum                                       | ✔︎       | State of the Organization.                                                                   |
| `tags`                | reference (collection) → \[#record:tag]    |          | Tags associated with an object.                                                              |
| `tier`                | enum                                       |          | The Tier of the corresponding Account.                                                       |
| `total_revenue`       | int                                        |          | Total sales revenue brought in by the company.                                               |
| `websites`            | text (collection)                          |          | Websites.                                                                                    |

## Enum values

**environment**

| Value        | Name       | Description |
| ------------ | ---------- | ----------- |
| `PRODUCTION` | PRODUCTION | -           |
| `STAGING`    | STAGING    | -           |
| `TEST`       | TEST       | -           |

**industry**

| Value                                                                      | Name                                                                             | Description |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------- |
| `accommodation_and_food_services`                                          | accommodation\_and\_food\_services                                               | -           |
| `administrative_and_support_and_waste_management_and_remediation_services` | administrative\_and\_support\_and\_waste\_management\_and\_remediation\_services | -           |
| `agriculture_forestry_fishing_and_hunting`                                 | agriculture\_forestry\_fishing\_and\_hunting                                     | -           |
| `arts_entertainment_and_recreation`                                        | arts\_entertainment\_and\_recreation                                             | -           |
| `construction`                                                             | construction                                                                     | -           |
| `educational_services`                                                     | educational\_services                                                            | -           |
| `finance_and_insurance`                                                    | finance\_and\_insurance                                                          | -           |
| `health_care_and_social_assistance`                                        | health\_care\_and\_social\_assistance                                            | -           |
| `information`                                                              | information                                                                      | -           |
| `management_of_companies_and_enterprises`                                  | management\_of\_companies\_and\_enterprises                                      | -           |
| `manufacturing`                                                            | manufacturing                                                                    | -           |
| `mining_quarrying_and_oil_and_gas_extraction`                              | mining\_quarrying\_and\_oil\_and\_gas\_extraction                                | -           |
| `other_services_except_public_administration`                              | other\_services\_except\_public\_administration                                  | -           |
| `professional_scientific_and_technical_services`                           | professional\_scientific\_and\_technical\_services                               | -           |
| `public_administration`                                                    | public\_administration                                                           | -           |
| `real_estate_and_rental_and_leasing`                                       | real\_estate\_and\_rental\_and\_leasing                                          | -           |
| `retail_trade`                                                             | retail\_trade                                                                    | -           |
| `transportation_and_warehousing`                                           | transportation\_and\_warehousing                                                 | -           |
| `utilities`                                                                | utilities                                                                        | -           |
| `wholesale_trade`                                                          | wholesale\_trade                                                                 | -           |

**lead\_source**

| Value               | Name               | Description |
| ------------------- | ------------------ | ----------- |
| `direct_traffic`    | direct\_traffic    | -           |
| `email_marketing`   | email\_marketing   | -           |
| `employee_referral` | employee\_referral | -           |
| `external_referral` | external\_referral | -           |
| `offline_sources`   | offline\_sources   | -           |
| `organic_search`    | organic\_search    | -           |
| `organic_social`    | organic\_social    | -           |
| `other`             | other              | -           |
| `other_campaigns`   | other\_campaigns   | -           |
| `paid_search`       | paid\_search       | -           |
| `paid_social`       | paid\_social       | -           |
| `partner`           | partner            | -           |
| `partner_referral`  | partner\_referral  | -           |
| `phone_inquiry`     | phone\_inquiry     | -           |
| `public_relations`  | public\_relations  | -           |
| `purchased_list`    | purchased\_list    | -           |
| `referrals`         | referrals          | -           |
| `trade_show`        | trade\_show        | -           |
| `web`               | web                | -           |
| `word_of_mouth`     | word\_of\_mouth    | -           |

**state**

| Value      | Name     | Description |
| ---------- | -------- | ----------- |
| `ACTIVE`   | ACTIVE   | -           |
| `INACTIVE` | INACTIVE | -           |
| `LOCKED`   | LOCKED   | -           |

**tier**

| Value    | Name    | Description |
| -------- | ------- | ----------- |
| `tier_1` | tier\_1 | -           |
| `tier_2` | tier\_2 | -           |
| `tier_3` | tier\_3 | -           |

### Structs

#### phone\_number

| Field         | Type | Required | Description                      |
| ------------- | ---- | -------- | -------------------------------- |
| `e164_number` | text | ✔︎       | The phone number in e164 format. |
| `extension`   | text |          | An optional extension.           |

#### postal\_address

| Field            | Type | Required | Description                                                            |
| ---------------- | ---- | -------- | ---------------------------------------------------------------------- |
| `country`        | text |          | Country name component.                                                |
| `formatted`      | text |          | Full mailing address, formatted for display or use on a mailing label. |
| `locality`       | text |          | Town, city.                                                            |
| `postal_code`    | text |          | Zip code of the address.                                               |
| `region`         | text |          | State, province, prefecture, or region component.                      |
| `street_address` | text |          | Full street address component.                                         |
