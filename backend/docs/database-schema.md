# Database Schema Documentation

## Overview
This document describes the database schema for the Better Auth integration, including both Better Auth managed tables and application-specific tables.

## Better Auth Tables (Managed by Better Auth)

### users table
- **id** (TEXT, PRIMARY KEY): Unique identifier for the user
- **email** (TEXT, UNIQUE, NOT NULL): User's email address
- **emailVerified** (TIMESTAMPTZ): Timestamp when email was verified
- **createdAt** (TIMESTAMPTZ, DEFAULT): Account creation timestamp
- **updatedAt** (TIMESTAMPTZ, DEFAULT): Last update timestamp
- **disabled** (BOOLEAN, DEFAULT false): Whether the account is disabled

### sessions table
- **id** (TEXT, PRIMARY KEY): Unique session identifier
- **userId** (TEXT, NOT NULL, FOREIGN KEY): Foreign key to users.id
- **expiresAt** (TIMESTAMPTZ, NOT NULL): Session expiration timestamp
- **createdAt** (TIMESTAMPTZ, DEFAULT): Session creation timestamp
- **ipAddress** (TEXT): IP address of session creation
- **userAgent** (TEXT): User agent string of session creation

### accounts table
- **id** (TEXT, PRIMARY KEY): Unique account identifier
- **userId** (TEXT, NOT NULL, FOREIGN KEY): Foreign key to users.id
- **providerId** (TEXT, NOT NULL): Provider identifier
- **providerAccountId** (TEXT, NOT NULL): Provider account identifier
- **createdAt** (TIMESTAMPTZ, DEFAULT): Creation timestamp

### verification table
- **id** (TEXT, PRIMARY KEY): Unique verification identifier
- **identifier** (TEXT, NOT NULL): Verification identifier
- **value** (TEXT, NOT NULL): Verification value
- **expiresAt** (TIMESTAMPTZ, NOT NULL): Expiration timestamp

## Application Tables (Managed by Application)

### user_profiles table
- **id** (TEXT, PRIMARY KEY): Unique identifier for the profile
- **user_id** (TEXT, NOT NULL, UNIQUE, FOREIGN KEY): Foreign key to Better Auth users.id with CASCADE DELETE
- **software_background** (TEXT): User's software background information (nullable until consent given)
- **hardware_background** (TEXT): User's hardware background information (nullable until consent given)
- **consent_given** (BOOLEAN, NOT NULL, DEFAULT false): Whether explicit consent was given for data storage
- **created_at** (TIMESTAMPTZ, DEFAULT): Profile creation timestamp
- **updated_at** (TIMESTAMPTZ, DEFAULT): Last update timestamp

### Schema Definition
```sql
CREATE TABLE user_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    software_background TEXT,
    hardware_background TEXT,
    consent_given BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);

-- Trigger to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
```

## Relationships

### User to UserProfile (One-to-One Optional)
- Each Better Auth user may have one application profile
- UserProfile.user_id references User.id with CASCADE DELETE
- When a Better Auth user is deleted, their profile is automatically deleted

### User to Session (One-to-Many)
- Each Better Auth user may have multiple active sessions
- Session.userId references User.id with CASCADE DELETE
- When a Better Auth user is deleted, all their sessions are automatically deleted

## Privacy and Consent Rules

### Data Storage Policy
- Background information (software/hardware) is only stored when `consent_given` is true
- If `consent_given` is false, background fields must be NULL
- Profile creation requires explicit user consent
- Profile updates require explicit consent for any new background information

### Validation Rules
- `consent_given` must be true before storing background information
- `software_background` and `hardware_background` are optional until consent is given
- `user_id` must reference an existing Better Auth user
- `created_at` and `updated_at` are automatically managed by triggers

## Migration Management

### Database Migration Script
The `database_migrations.py` script handles the creation and management of the `user_profiles` table:

```bash
# Create the user_profiles table
python database_migrations.py create

# Drop the user_profiles table (for development)
python database_migrations.py drop
```

## Security Considerations

### Data Protection
- Personal information is only stored with explicit user consent
- Foreign key relationships ensure data consistency
- Cascade delete ensures cleanup when Better Auth users are removed
- Indexes on foreign keys for performance optimization

### Access Control
- Profile data is only accessible to the authenticated user
- Database connections use connection pooling with appropriate timeouts
- All database queries use parameterized statements to prevent injection