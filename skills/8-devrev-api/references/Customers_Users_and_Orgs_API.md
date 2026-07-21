# Customers, users & orgs — DevRev API

Identity and customer-data objects: accounts, rev orgs (workspaces), rev users
(customers/contacts), dev users (internal users), dev orgs, groups, directory,
service accounts, and system users.

| Field | Detail |
| --- | --- |
| Base URL | https://api.devrev.ai |
| Auth | `Authorization: Bearer <TOKEN>` |

---

## 1. Accounts

A company/customer record. Rev orgs and rev users hang off accounts.

```bash
curl -X POST 'https://api.devrev.ai/accounts.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "display_name": "Acme Corp",
      "domains": [ "acme.com" ],
      "owned_by": [ "<DEVU_ID>" ] }'
```

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `accounts.create` / `.update` | `account:write` / `:all` | Create / edit |
| `accounts.delete` | `account:all` | Delete |
| `accounts.merge` | `account:all` | Merge duplicates |
| `accounts.get` / `.list` / `.export` | `account:read` … | Read |

---

## 2. Rev orgs (workspaces / customer orgs)

The customer-side org that contains rev users.

```bash
curl -X POST 'https://api.devrev.ai/rev-orgs.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "display_name": "Acme Prod Workspace",
      "account": "<ACCOUNT_ID>" }'
```

`rev-orgs.get/list/update/delete` — scopes `rev_org:read/write/all`.

---

## 3. Rev users (customers / contacts)

An end customer or external contact.

```bash
curl -X POST 'https://api.devrev.ai/rev-users.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "display_name": "Jane Doe",
      "email": "jane@acme.com",
      "rev_org": "<REV_ORG_ID>" }'
```

| Endpoint | Scope |
| --- | --- |
| `rev-users.create` / `.update` | `rev_user:write` / `:all` |
| `rev-users.delete` / `.merge` | `rev_user:all` |
| `rev-users.get` / `.list` / `.scan` | `rev_user:read` … |

`rev-users.scan` streams large sets; `rev-users.merge` de-dupes contacts.

---

## 4. Dev users (internal team members)

```bash
# Who am I
curl -X POST 'https://api.devrev.ai/dev-users.self' \
-H 'Authorization: Bearer <TOKEN>' -d '{}'
```

| Endpoint | Scope | Purpose |
| --- | --- | --- |
| `dev-users.create` / `.update` | `dev_user:write` / `:all` | Manage users |
| `dev-users.activate` | `dev_user:write` / `:all` | Reactivate |
| `dev-users.deactivate` | `dev_user:all` | Deactivate |
| `dev-users.merge` | `dev_user:all` | Merge |
| `dev-users.identities.link` / `.unlink` | `dev_user:write` / `:all` | External identity mapping |
| `dev-users.get` / `.list` | `dev_user:read` … | Read |
| `dev-users.self` / `.self.update` | None | Current user |

---

## 5. Dev orgs

```bash
curl -X POST 'https://api.devrev.ai/dev-orgs.get' \
-H 'Authorization: Bearer <TOKEN>' -d '{}'
```

`dev-orgs.get` — scope `dev_org:read`/`dev_org:write`. (Provisioning a brand-new
dev org tenant is done in the app / at subscription time, not via this API.)

---

## 6. Groups

Groups organize users for routing/access-control purposes.

```bash
# Create a group, then add a member
curl -X POST 'https://api.devrev.ai/groups.create' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "name": "Support Tier 1", "member_type": "dev_user" }'

curl -X POST 'https://api.devrev.ai/groups.members.add' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{ "group": "<GROUP_ID>", "members": [ "<DEVU_ID>" ] }'
```

| Endpoint | Scope |
| --- | --- |
| `groups.create` / `.update` | `group:write` / `:all` |
| `groups.get` / `.list` | `group:read` … |
| `groups.members.add` / `.remove` | `group_membership:all` |
| `groups.members.list` | `group_membership:read` / `:all` |

<!-- corrected 2026-07-21: was "Groups organize users; directories are the higher-level container" with directories.* listed here as a user/group-organization endpoint. That's wrong — `directory` is the Help Center Article-collection object, unrelated to groups/users. Moved to references/Support_Knowledge_and_SLAs_API.md §3b and references/Directories_Collections_API.md; see docs/LEARNINGS.md. -->

---

## 7. Service accounts & system users

| Endpoint | Scope | Notes |
| --- | --- | --- |
| `service-accounts.create` | None | User auth only; not callable via a service-account token |
| `service-accounts.get` | `svcacc:read` | |
| `sys-users.list` / `.update` | None | System (bot) users |

---

## 8. Object relationships (build order)

`account` → `rev_org` (references account) → `rev_user` (references rev_org).
Create top-down and save each returned DON id. Reference every object by DON,
never display ID.

## 9. Pitfalls

- Creating a rev user without a rev org / a rev org without an account — set the
  parent reference at creation.
- Deleting vs merging — use `.merge` to consolidate duplicate accounts/users;
  `.delete` needs the `:all` scope and is destructive.
- Deactivate (not delete) internal users who leave — `dev-users.deactivate`.
