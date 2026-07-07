# Decision 6: Deferred Access Token Blacklisting

## Decision

Do not implement access-token blacklisting during Phase 3.

## Reason

The current authentication architecture uses:

- Short-lived access tokens (15 minutes)
- Refresh token rotation
- Refresh token revocation on logout

When a user logs out, the refresh token is revoked immediately, preventing issuance of new access tokens. The remaining risk window is limited to the lifetime of the current access token (15 minutes), which is acceptable for the project's scope.

Implementing access-token blacklisting would introduce:

- Redis dependency
- JWT `jti` tracking
- Additional authentication checks on every protected request

without providing significant practical benefit for a learning-focused, non-public project.

## Future Revisit Criteria

Consider access-token blacklisting if:

- Access token lifetime increases significantly
- The application becomes publicly deployed
- Security requirements become stricter
- "Logout everywhere" functionality is introduced