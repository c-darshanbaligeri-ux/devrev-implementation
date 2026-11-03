# DevRev object types and fields

Source: <https://developer.devrev.ai/airsync/supported-object-types>
Scraped: 2026-11-03

Choose a DevRev target for each external record type. Open only the field reference you need. Each reference lists required fields, supported capabilities and enum values.

Field tables reflect the July 13, 2026 catalog. Reverse-sync and subtype capabilities for the listed types were checked against mapping metadata on October 16, 2026. Available targets and fields can vary; check the mapping options in your target organization.

## Direction and capability semantics

**Loading** and **Can Load** on this page mean the platform can load external data **into DevRev**. **Extraction** and **Can Extract** mean DevRev records can be transformed **out to the external system**. In SDK worker terminology, extraction is external-to-DevRev and loading is DevRev-to-external. Keep these perspectives distinct when selecting a capability.

Platform support does not implement the connector's external API. Reverse sync also needs loadable EDM, reverse mapping and create/update callbacks. A mapper target type is an identity enum and does not itself establish import or reverse support.

## Summary

| Object Type                                                                                                                    | Object Hierarchy               | Into DevRev | Out of DevRev |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ | :---------: | :-----------: |
| <span id="new_custom_object" />[`new_custom_object`](object-types/new_custom_object.md)                                  | custom\_object                 |      ✔︎     |       ✔︎      |
| <span id="account" />[`account`](object-types/account.md)                                                                | account                        |      ✔︎     |               |
| <span id="airdrop_platform_group" />[`airdrop_platform_group`](object-types/airdrop_platform_group.md)                   | airdrop\_platform\_group       |      ✔︎     |               |
| <span id="article" />[`article`](object-types/article.md)                                                                | article                        |      ✔︎     |               |
| <span id="capability" />[`capability`](object-types/capability.md)                                                       | part→capability                |      ✔︎     |       ✔︎      |
| <span id="channel" />[`channel`](object-types/channel.md)                                                                | chat→channel                   |      ✔︎     |               |
| <span id="comment" />[`comment`](object-types/comment.md)                                                                | comment                        |      ✔︎     |       ✔︎      |
| <span id="component" />[`component`](object-types/component.md)                                                          | part→component                 |      ✔︎     |       ✔︎      |
| <span id="conversation" />[`conversation`](object-types/conversation.md)                                                 | conversation                   |      ✔︎     |               |
| <span id="custom_link" />[`custom_link`](object-types/custom_link.md)                                                    | link                           |      ✔︎     |       ✔︎      |
| <span id="devu" />[`devu`](object-types/devu.md)                                                                         | dev\_user                      |      ✔︎     |               |
| <span id="directory" />[`directory`](object-types/directory.md)                                                          | directory                      |      ✔︎     |               |
| <span id="dm" />[`dm`](object-types/dm.md)                                                                               | chat→dm                        |      ✔︎     |               |
| <span id="enhancement" />[`enhancement`](object-types/enhancement.md)                                                    | part→enhancement               |      ✔︎     |       ✔︎      |
| <span id="feature" />[`feature`](object-types/feature.md)                                                                | part→feature                   |      ✔︎     |       ✔︎      |
| <span id="group" />[`group`](object-types/group.md)                                                                      | group                          |      ✔︎     |               |
| <span id="incident" />[`incident`](object-types/incident.md)                                                             | incident                       |      ✔︎     |       ✔︎      |
| <span id="issue" />[`issue`](object-types/issue.md)                                                                      | work→issue                     |      ✔︎     |       ✔︎      |
| <span id="link" />[`link`](object-types/link.md)                                                                         | link                           |      ✔︎     |       ✔︎      |
| <span id="linkable" />[`linkable`](object-types/linkable.md)                                                             | part→linkable                  |      ✔︎     |       ✔︎      |
| <span id="meeting" />[`meeting`](object-types/meeting.md)                                                                | meeting                        |      ✔︎     |       ✔︎      |
| <span id="microservice" />[`microservice`](object-types/microservice.md)                                                 | part→microservice              |      ✔︎     |       ✔︎      |
| <span id="object_member" />[`object_member`](object-types/object_member.md)                                              | object\_member                 |      ✔︎     |               |
| <span id="opportunity" />[`opportunity`](object-types/opportunity.md)                                                    | work→opportunity               |      ✔︎     |       ✔︎      |
| <span id="product" />[`product`](object-types/product.md)                                                                | part→product                   |      ✔︎     |       ✔︎      |
| <span id="revu" />[`revu`](object-types/revu.md)                                                                         | rev\_user                      |      ✔︎     |               |
| <span id="runnable" />[`runnable`](object-types/runnable.md)                                                             | part→runnable                  |      ✔︎     |       ✔︎      |
| <span id="sprint" />[`sprint`](object-types/sprint.md)                                                                   | vista\_group\_item             |      ✔︎     |               |
| <span id="sprint_board" />[`sprint_board`](object-types/sprint_board.md)                                                 | vista                          |      ✔︎     |               |
| <span id="sysu" />[`sysu`](object-types/sysu.md)                                                                         | sys\_user                      |      ✔︎     |               |
| <span id="tag" />[`tag`](object-types/tag.md)                                                                            | tag                            |      ✔︎     |               |
| <span id="task" />[`task`](object-types/task.md)                                                                         | work→task                      |      ✔︎     |       ✔︎      |
| <span id="team" />[`team`](object-types/team.md)                                                                         | team                           |      ✔︎     |               |
| <span id="ticket" />[`ticket`](object-types/ticket.md)                                                                   | work→ticket                    |      ✔︎     |       ✔︎      |
| <span id="unified_authorization_policy" />[`unified_authorization_policy`](object-types/unified_authorization_policy.md) | unified\_authorization\_policy |      ✔︎     |               |

## Key capabilities

| Capability       | Description                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| Can Load         | Indicates that the object type can be loaded into DevRev with AirSync.                            |
| Can Extract      | Indicates that the object type can be synced out to external systems.                             |
| Can Subtype      | Indicates that the object type supports [subtype](../guides/object-customization.md#subtype) creation. |
| Can App Fragment | Indicates that the object type supports application fragments.                                    |

Read [target field rules](object-field-contract.md) before mapping required fields and references.
