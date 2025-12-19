# Data Model: Better Auth Integration

## Entities

### User (Managed by Better Auth)
- **id** (string): Unique identifier for the user
- **email** (string): User's email address (unique, required)
- **emailVerified** (datetime | null): Timestamp when email was verified
- **createdAt** (datetime): Account creation timestamp
- **updatedAt** (datetime): Last update timestamp
- **disabled** (boolean): Whether the account is disabled

### Session (Managed by Better Auth)
- **id** (string): Unique session identifier
- **userId** (string): Foreign key to User.id
- **expiresAt** (datetime): Session expiration timestamp
- **createdAt** (datetime): Session creation timestamp
- **ipAddress** (string | null): IP address of session creation
- **userAgent** (string | null): User agent string of session creation

### UserProfile (Application-owned)
- **id** (string): Unique identifier for the profile
- **userId** (string): Foreign key to Better Auth User.id
- **softwareBackground** (string | null): User's software background information
- **hardwareBackground** (string | null): User's hardware background information
- **consentGiven** (boolean): Whether explicit consent was given for data storage
- **createdAt** (datetime): Profile creation timestamp
- **updatedAt** (datetime): Last update timestamp

## Relationships

### User to UserProfile
- **Type**: One-to-One (Optional)
- **Description**: Each user may have one profile with background information
- **Constraint**: UserProfile.userId references User.id with cascade delete

### User to Session
- **Type**: One-to-Many
- **Description**: Each user may have multiple active sessions
- **Constraint**: Session.userId references User.id with cascade delete

## Validation Rules

### User Validation (from Better Auth)
- Email must be valid format
- Email must be unique across all users
- Email is required for registration

### UserProfile Validation
- consentGiven must be true before storing background information
- softwareBackground and hardwareBackground are optional until consent is given
- userId must reference an existing Better Auth user
- createdAt and updatedAt are automatically managed

### Session Validation (from Better Auth)
- expiresAt must be in the future
- userId must reference an existing user
- Session automatically expires after configured time

## State Transitions

### User Registration Flow
1. User provides email and password
2. Better Auth creates User record
3. User must provide consent and background information
4. Application creates UserProfile record linked to User

### Consent Flow
1. User registers without providing background information
2. User gives explicit consent to store data
3. User provides software and hardware background
4. Application creates UserProfile with consentGiven = true

### Session Lifecycle
1. User authenticates via Better Auth
2. Better Auth creates Session record
3. Session remains active until expiresAt
4. Session can be invalidated by user logout
5. Session automatically expires and is cleaned up

## Database Schema

### Better Auth Tables (Managed by Better Auth)
- `users` - Core user information
- `sessions` - Active and expired sessions
- `accounts` - Social login account links
- `verification` - Email verification tokens

### Application Tables (Managed by Application)
```sql
CREATE TABLE user_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    software_background TEXT,
    hardware_background TEXT,
    consent_given BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```