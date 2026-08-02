# Authentication

Source: <https://developer.devrev.ai/about/authentication>
Scraped: 2026-08-02

## Security token types

- **Application Access Token (AAT)**: Identifies an application belonging to a dev org. Obtained by a dev user with sufficient privileges for a given application, and issued against an application ID (which could represent the dev org's SaaS app). It can only be used to obtain a session token and does not reference any dev user or customer. The expiration time is set at token generation, with lifetimes usually in days. The subject is set to the DON of the application, which is a service account.
  - Example subject: `don:identity:dvrv-us-1:devo/0:svcacc/gG88A`

- **System User Token (SUT)**: Identifies a system user belonging to a dev org. Obtained by a dev user with sufficient privileges for a given system user, and issued for the DON of the corresponding system user. Expiration is defined at token generation, and lifetime is usually in days. Subject is set to the DON of the corresponding system user.
  - Example subject: `don:identity:dvrv-us-1:devo/0:sysu/1`

- **Session Token**: Obtained by an application to access DevRev APIs on behalf of a customer. The application uses its own AAT to authenticate to the STS to obtain a session token, then uses the session token to call DevRev APIs. Lifetime is typically minutes. Subject is set to the DON of the corresponding customer.
  - Example subject: `don:identity:dvrv-us-1:devo/0:revo/6:revu/131`

- **Personal Access Token (PAT)**: Identifies a dev user. Used by external applications to access DevRev APIs on behalf of that dev user. Lifetime is usually in days. Subject is set to the corresponding dev user's DON.
  - Example subject: `don:identity:dvrv-us-1:devo/0:devu/30`

## Personal access token usage

Authenticating to DevRev APIs requires a PAT, which uniquely identifies a dev user in the context of a dev org and can be used by external third-party applications on behalf of that user. A PAT carries "the same set of privileges that the owner of the PAT has on the DevRev platform." You can set its validity duration, but PATs cannot be renewed — you must create a new PAT and update your code accordingly.

Example use case: a VS Code plugin that pulls issues from DevRev for a particular dev user would rely on that user's PAT to authenticate.

If you receive an `invalid token` error, you can validate the token at [jwt.io](https://jwt.io/).

## Generate a personal access token (PAT)

1. In the DevRev app, navigate to the relevant dev org.
2. Go to **Settings** > **Account** > **Personal Access Token**.
3. Click **New token** and complete the creation workflow.

Because the token value cannot be retrieved later, descriptive names are recommended to help distinguish between multiple PATs.

4. Copy the PAT and store it securely — once you leave the page, it cannot be retrieved again.

## Revoke a personal access token

Revocations are permanent — a revoked PAT cannot be restored. Never share tokens with other users or applications, and do not publish them in public code repositories.

1. In the DevRev app, go to the relevant dev org.
2. Go to **Settings** > **Account** > **Personal Access Token**.
3. Click **Revoke** next to the PAT you want to revoke.

You may also click **Revoke all** to revoke every token you have previously generated.

---

**Note:** The source page did not contain any HTTP header specifications, example HTTP requests/responses, endpoint URLs, or code samples (not documented on the page as of scrape date 2026-08-02). The `Authorization: Bearer <token>` convention used in every other skill's reference docs is not spelled out on this specific page.
