# Session Behavior and Privacy/Consent Rules

## Session Management

### Session Lifecycle
1. **Session Creation**: When a user successfully authenticates, Better Auth creates a session record
2. **Session Validation**: Sessions are validated on each authenticated request
3. **Session Expiration**: Sessions automatically expire after the configured time (default: 7 days)
4. **Session Termination**: Sessions can be terminated manually via signout or automatically when expired

### Session Configuration
- **Duration**: 7 days (604,800 seconds)
- **Remember Me**: Enabled by default
- **Update Age**: Session age is updated every 24 hours if the session is active
- **Cookie Settings**: Secure, HttpOnly, SameSite cookies for security

### Session Restoration
- Sessions are automatically restored when users visit the application
- The frontend checks for existing sessions on page load
- Session state is maintained across page refreshes and navigation

## Privacy Rules

### Data Collection Principles
- **Minimal Data Collection**: Only collect information necessary for functionality
- **Explicit Consent**: User background information requires explicit consent
- **Transparency**: Users are clearly informed about what data is collected
- **User Control**: Users can update or remove their background information

### Consent Management
- **Explicit Consent Required**: Users must explicitly check a consent box to store background information
- **Consent Validation**: The system validates that consent is given before storing personal information
- **Consent Updates**: Users can update their consent status at any time
- **Consent Revocation**: Users can revoke consent, which triggers data deletion

### Background Information Handling
- **Software Background**: Optional field for user's software development experience
- **Hardware Background**: Optional field for user's hardware experience
- **Consent Requirement**: Both fields require explicit consent before storage
- **Privacy Preservation**: Background information is only accessible to the authenticated user

## Consent Rules

### Consent Validation Process
1. **Form Validation**: Signup form requires explicit consent checkbox to be checked
2. **Backend Validation**: Server-side validation ensures consent is given before storing background data
3. **Database Enforcement**: Database schema enforces that consent must be true before storing background information
4. **API Validation**: Profile endpoints validate consent before processing background information

### Consent-Related Behaviors
- **Default State**: `consent_given` is false by default
- **Required for Storage**: Background information cannot be stored without consent
- **Separate from Authentication**: Users can authenticate without providing background information
- **Revocable**: Users can revoke consent, which may trigger data deletion

### Data Storage Rules
- **With Consent**: Background information is stored in the `user_profiles` table
- **Without Consent**: Only the user account exists, no background information is stored
- **Consent Update**: Users can update consent status and background information separately
- **Deletion**: Revoking consent may trigger background information deletion (implementation dependent)

## Privacy Compliance

### Data Protection Measures
- **Encryption**: Session tokens are encrypted and stored securely
- **Access Control**: Profile data is only accessible to the authenticated user
- **Audit Trail**: Authentication events are logged for security purposes
- **Data Minimization**: Only necessary data is collected and stored

### User Rights
- **Access**: Users can view their profile information
- **Update**: Users can update their profile information
- **Deletion**: Users can request deletion of their personal information
- **Portability**: Users can export their data (future enhancement)

## Implementation Details

### Frontend Consent Flow
1. **Signup Form**: Users see background information fields and consent checkbox
2. **Validation**: Form validation prevents submission without consent
3. **Submission**: Background information is sent only when consent is given
4. **Confirmation**: Users receive confirmation of successful profile creation

### Backend Consent Flow
1. **Request Validation**: API validates consent before processing background information
2. **Database Storage**: Background information is stored only with consent
3. **Session Integration**: User session includes consent status
4. **Privacy Enforcement**: All operations respect user's consent preferences

## Error Handling for Privacy

### Consent Validation Errors
- **Missing Consent**: If consent is required but not given, return 400 error
- **Invalid Consent**: If consent is invalid, return 400 error with clear message
- **Processing Errors**: If consent validation fails, log error and return 500 error

### Privacy Violation Handling
- **Unauthorized Access**: If a user tries to access another user's profile, return 403 error
- **Missing Session**: If session is missing during profile access, return 401 error
- **Expired Consent**: If consent has been revoked, handle gracefully with appropriate messaging