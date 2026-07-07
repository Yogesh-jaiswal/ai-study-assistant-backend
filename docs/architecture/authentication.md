# Authentication Architecture

## Purpose

The authentication system provides secure, stateless user authentication using short-lived JWT access tokens and rotating refresh tokens.

The architecture is designed around the following principles:

- Stateless API authentication
- Secure password storage
- Independent multi-device sessions
- Minimal database lookups on authenticated requests
- Separation of authentication logic from business logic
- Production-oriented design with low implementation complexity

Unlike most services in the backend, the authentication system directly depends on the database because user identities and refresh token sessions must be persisted.

---

# Components

Authentication is composed of several independent services.

```text
Authentication
│
├── Registration
├── Login
├── JWT Service
├── Refresh Tokens
├── Logout
├── Password Hashing
└── Route Protection
```

Authentication depends on:

- User Repository
- Refresh Token Repository
- JWT Service
- Password Hashing Service

Business services never manipulate JWTs or passwords directly.

---

# Registration

Registration creates a new user account after validating the request and ensuring that the email address is unique.

Passwords are never stored directly.

### Workflow

```text
Registration Request

↓

Validate payload

↓

Check existing email

↓

Hash password (Argon2)

↓

Create user

↓

Save user

↓

Return success response
```

---

# Login

Login authenticates the user and creates a new authentication session.

A successful login creates:

- One JWT access token
- One refresh token session

The refresh token is hashed before storage.

### Workflow

```text
Login Request

↓

Lookup user

↓

Verify password

↓

Issue access token

↓

Generate refresh token

↓

Hash refresh token

↓

Store refresh token

↓

Return login response
```

Successful login returns:

```json
{
    "access_token": "...",
    "expires_in": 900,
    "message": "..."
}
```

---

# Access Tokens

Access tokens are JWTs signed using **RS256**.

Properties:

- Lifetime: **15 minutes**
- Stateless
- Stored by the frontend
- Sent using the Authorization header
- Verified on every protected request

Claims:

- `sub` (User ID)
- `jti`
- `iat`
- `nbf`
- `exp`

Because access tokens are stateless, authenticated requests do not require a database lookup for session validation.

---

# Refresh Tokens

Refresh tokens are responsible for creating new access tokens without requiring user credentials.

Each login creates an independent refresh token, allowing multiple simultaneous devices.

Properties:

- Lifetime: **30 days**
- Stored as SHA-256 hash
- Rotated after every refresh
- One refresh token per login session
- Supports multiple concurrent devices

Database model:

```text
id
user_id
token_hash
created_at
expires_at
```

Only the token hash is stored.

Raw refresh tokens are never persisted.

### Workflow

```text
Refresh Request

↓

Verify refresh token

↓

Lookup stored token hash

↓

Check expiration

↓

Delete expired token (if expired)

↓

Revoke old refresh token

↓

Issue new access token

↓

Generate new refresh token

↓

Hash refresh token

↓

Store new refresh token

↓

Return login response
```

Refresh behaves like a re-login without requiring user credentials.

---

# Logout

Logout invalidates only the current refresh token.

Access tokens are **not** revoked.

Instead, they naturally expire after their short lifetime.

### Workflow

```text
Logout Request

↓

Verify refresh token

↓

Delete refresh token

↓

Return success response
```

---

# Password Security

Passwords are hashed using **Argon2**.

Validation rules include:

- Minimum length
- Uppercase character
- Lowercase character
- Number
- Special character

To reduce timing attacks, authentication performs a dummy password hash verification even when the requested email address does not exist.

This prevents attackers from distinguishing existing and non-existing accounts based on response timing.

---

# Route Protection

Protected routes are secured using authentication decorators.

The decorator performs authentication before the route executes.

### Workflow

```text
Protected Request

↓

Extract Bearer token

↓

Verify JWT signature

↓

Validate claims

↓

Extract current user

↓

Execute route
```

Business services never parse JWTs directly.

---

# Multi-device Sessions

The authentication system intentionally supports multiple concurrent devices.

Each successful login creates an independent refresh token session.

Benefits include:

- Multiple active devices
- Independent logout per device
- Independent refresh token rotation

Global logout ("Logout everywhere") is intentionally not implemented.

---

# Security Decisions

## Stateless Authentication

The backend uses JWT access tokens to avoid maintaining server-side authentication sessions.

Only refresh tokens require database persistence.

---

## Refresh Token Rotation

Every refresh request invalidates the previous refresh token and creates a completely new authentication session.

This reduces replay attacks using previously issued refresh tokens.

---

## No Access Token Blacklist

Access token blacklisting has intentionally been deferred.

Reasons:

- Access tokens live only 15 minutes.
- Refresh tokens are revoked immediately on logout.
- Blacklisting would require Redis lookups on every authenticated request.
- The additional complexity provides little practical benefit for the current project.

See [Decision 006](../decisions/006-deferred-access-token-blacklisting.md).

---

# Current Limitations

The current implementation intentionally accepts several trade-offs.

- Expired refresh tokens remain in the database until they are encountered again.
- Automatic cleanup of expired refresh tokens is not implemented.
- Global logout ("Logout everywhere") is not implemented.
- Access-token blacklisting is deferred.

These trade-offs simplify the authentication architecture while remaining appropriate for a learning-focused backend project.

---

# Future Improvements

Potential future enhancements include:

- Automatic cleanup of expired refresh tokens
- Access-token blacklisting
- Session monitoring
- Remote logout ("Logout everywhere")
- Device metadata
- Login history
- Security notifications for new logins