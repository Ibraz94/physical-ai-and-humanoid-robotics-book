# User Consent Revocation and Data Deletion

## Overview
This document describes how users can revoke their consent and have their personal background information deleted from the system, in compliance with privacy regulations and user preferences.

## Consent Revocation Process

### User-Initiated Consent Revocation
Users can revoke their consent through the following methods:

1. **Through Profile Update**:
   - Users can update their profile with `consent_given: false`
   - This will remove their background information while preserving their account
   - The system will remove `software_background` and `hardware_background` fields

2. **Account Deletion**:
   - Users can delete their account entirely
   - This triggers a cascade delete that removes their profile data
   - All personal information is permanently removed

### Automated Data Deletion
When consent is revoked (`consent_given: false`), the system automatically:
- Removes the `software_background` field value
- Removes the `hardware_background` field value
- Maintains the profile record with `consent_given: false` and empty background fields
- Preserves the user account for authentication purposes

## API Implementation

### Profile Update Endpoint
The `/api/v1/profile` endpoint handles consent revocation:

```python
# When consent_given is set to False
if not profile_data.consent_given:
    # Background information will be set to None/empty
    software_background = None
    hardware_background = None
```

### Data Deletion Logic
```sql
-- When consent is revoked, background information is set to NULL
UPDATE user_profiles
SET software_background = NULL,
    hardware_background = NULL,
    consent_given = FALSE,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = $1 AND consent_given = TRUE;
```

## Privacy Compliance

### GDPR Compliance
- Users have the right to withdraw consent at any time
- Data deletion is processed within a reasonable timeframe
- Users are informed about the consequences of consent revocation
- Audit logs maintain records of consent changes (without identifying information)

### Data Minimization
- Only essential data is retained after consent revocation
- Background information is deleted when consent is withdrawn
- User accounts remain active for continued service access
- Minimal data retention helps ensure privacy compliance

## User Experience

### Consent Revocation Interface
- Clear and accessible consent management in user profiles
- Confirmation steps to prevent accidental consent revocation
- Information about what data will be deleted
- Options to retain account while removing personal information

### Post Revocation State
- Users can continue to use RAG functionality anonymously
- Personalized features remain disabled until consent is re-granted
- Profile remains in system but with minimal data
- User authentication continues to work normally

## Administrative Controls

### Admin Data Deletion
Administrators can also initiate data deletion for compliance purposes:
- Bulk consent revocation for policy changes
- Emergency data deletion for security incidents
- Audit trail for all administrative data deletion actions

### Data Retention Policies
- Default: Background information deleted immediately on consent revocation
- Extended retention possible for legal compliance (with user notification)
- Regular cleanup of outdated consent records

## Security Considerations

### Data Deletion Verification
- Confirmation that data has been properly deleted
- Verification that deleted data cannot be recovered
- Logging of deletion events for audit purposes

### Access Control
- Only authenticated users can revoke their own consent
- Administrative access to consent revocation is logged
- No unauthorized access to consent status or background information

## Implementation Notes

### Database Constraints
The user_profiles table enforces the consent rule:
```sql
-- Background information can only exist when consent is given
-- This is enforced in application logic and should be validated at the API level
```

### API Validation
- API validates that consent is properly handled
- Error responses are clear and informative
- Validation prevents inconsistent states

## Future Enhancements

### Enhanced Privacy Controls
- Granular consent options for different types of data
- Temporary consent with automatic expiration
- Data portability options for exported information

### Audit and Monitoring
- Enhanced logging for consent changes
- Monitoring for unusual consent revocation patterns
- Automated compliance reporting