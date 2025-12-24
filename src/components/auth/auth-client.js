/**
 * Better Auth React Client for Docusaurus frontend
 * Provides authentication functionality for the frontend application
 */

import { createAuthClient } from "better-auth/react";

// Initialize the Better Auth client with configuration
const authClient = createAuthClient({
    baseURL: "https://ibraz-api-ai-book.hf.space", // FastAPI backend that proxies to Better Auth
    fetchOptions: {
        credentials: 'include', // Important: include cookies for session management
    },
});

// Export the client
export { authClient };

// Export individual methods for easier usage
export const signIn = authClient.signIn;
export const signUp = authClient.signUp;
export const signOut = authClient.signOut;
export const useSession = authClient.useSession;
export const getClientSession = authClient.getClientSession;
export const forgotPassword = authClient.forgotPassword;
export const resetPassword = authClient.resetPassword;
export const changePassword = authClient.changePassword;
export const updateEmail = authClient.updateEmail;
export const verifyEmail = authClient.verifyEmail;
export const sendVerificationEmail = authClient.sendVerificationEmail;
export const getSession = authClient.getSession;
export const setSession = authClient.setSession;
export const clearSession = authClient.clearSession;

// Additional utility functions
export const isAuthenticated = async () => {
    try {
        const session = await authClient.getClientSession();
        return !!session?.user;
    } catch (error) {
        console.warn("Error checking authentication status:", error);
        return false;
    }
};

// Hook to get user profile information
export const useUserProfile = () => {
    const { data: session, isLoading } = authClient.useSession();

    return {
        user: session?.user || null,
        isLoading,
        isAuthenticated: !!session?.user,
        userId: session?.user?.id || null
    };
};

// Function to update user profile with background information
export const updateUserProfile = async (profileData) => {
    try {
        // This would typically call a backend endpoint to update user profile
        // The actual implementation would depend on your backend API structure
        const session = await authClient.getClientSession();
        const response = await fetch('/api/user-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${session?.accessToken || ''}`
            },
            body: JSON.stringify(profileData)
        });

        if (!response.ok) {
            throw new Error('Failed to update user profile');
        }

        return await response.json();
    } catch (error) {
        console.error('Error updating user profile:', error);
        throw error;
    }
};

export default authClient;