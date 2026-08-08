# Authentication API

The Authentication API is responsible for user registration, login, token refresh, logout, and retrieving the currently authenticated user's profile.

Authentication is based on **JWT access tokens** together with **refresh tokens stored in secure HTTP-only cookies**.

---

# Authentication Flow

The backend uses a dual-token authentication mechanism.

- **Access Token**
  - JWT
  - Lifetime: **15 minutes**
  - Sent in the `Authorization` header
  - Used to authenticate protected API requests

- **Refresh Token**
  - Lifetime: **30 days**
  - Stored as an HTTP-only cookie
  - Automatically rotated whenever a new access token is issued
  - Never accessible from JavaScript

Typical flow:

```
Register/Login
        ↓
Access Token (15 min)
Refresh Token (30 days cookie)
        ↓
Authenticated Requests
        ↓
Access Token Expired
        ↓
POST /v1/auth/refresh
        ↓
New Access Token
New Refresh Token
```

---

# Authorization

Protected endpoints require the following header:

```http
Authorization: Bearer <access_token>
```

Missing, expired, or invalid access tokens result in:

```
401 Unauthorized
```

---

# Refresh Token Cookie

The refresh token is stored as an HTTP-only cookie with the following configuration:

| Property | Value |
|----------|-------|
| HttpOnly | true |
| SameSite | Strict |
| Secure | Enabled outside debug mode |
| Max Age | 30 days |

The cookie is automatically created by:

- Login
- Refresh

The cookie is automatically removed by:

- Logout

---

# Endpoints

## Register

**POST**

```
/v1/auth/register
```

Creates a new user account.

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| email | string | Yes | User email address |
| username | string | Yes | Display username |
| password | string | Yes | User password |

### Password Requirements

Passwords must contain:

- Minimum 8 characters
- One uppercase letter
- One lowercase letter
- One digit
- One special character

### Success Response

**201 Created**

```json
{
    "success": true,
    "data": {
        "id": "431c35b8-bed7-48b6-83b2-0efe165da6cd",
        "email": "user@example.com",
        "message": "user registered successfully"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 409 | Email already registered |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Login

**POST**

```
/v1/auth/login
```

Authenticates a user using email and password.

On success:

- Returns an access token
- Creates a refresh token cookie

### Request Body

| Field | Type | Required |
|------|------|----------|
| email | string | Yes |
| password | string | Yes |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "access_token": "431c35b8-bed7-48b6-83b2-0efe165da6cd",
        "expires_in": 900,
        "message": "log in successful"
    },
    "error": null
}
```

### Side Effects

- Creates a refresh token cookie.

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Invalid credentials |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Refresh Access Token

**POST**

```
/v1/auth/refresh
```

Generates a new access token using the refresh token cookie.

This endpoint does **not** require an Authorization header.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "access_token": "431c35b8-bed7-48b6-83b2-0efe165da6cd",
        "expires_in": 900,
        "message": "re login successful"
    },
    "error": null
}
```

### Side Effects

- Rotates the refresh token.
- Replaces the existing refresh token cookie.

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing, expired, revoked, or invalid refresh token |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Current User

**GET**

```
/v1/auth/me
```

Returns information about the currently authenticated user.

### Authentication

Required.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "431c35b8-bed7-48b6-83b2-0efe165da6cd",
        "email": "user@example.com",
        "username": "user123"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Logout

**POST**

```
/v1/auth/logout
```

Logs the user out by revoking the refresh token and deleting the refresh token cookie.

The current access token remains valid until its expiration.

### Authentication

Requires a valid refresh token cookie.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "message": "log out successful"
    },
    "error": null
}
```

### Side Effects

- Deletes the refresh token from the database.
- Deletes the refresh token cookie.

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid refresh token |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 400 | Request does not contain a valid JSON body |
| 401 | Authentication failed |
| 409 | Resource conflict (duplicate email) |
| 422 | Request validation failed |
| 429 | Too many requests |
| 500 | Unexpected server error or Database error |

# Next Steps

Explore [Notebook API](Notebook.md)