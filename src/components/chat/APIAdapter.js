/**
 * API Adapter to map ChatKit format to existing backend format
 * This adapter ensures compatibility between ChatKit's expected format and our existing backend API
 */

class APIAdapter {
  constructor(backendUrl) {
    // Use provided URL or default to localhost
    this.backendUrl = backendUrl || 'http://localhost:8000';
  }

  /**
   * Maps ChatKit message format to our backend format
   * @param {Object} chatKitMessage - Message in ChatKit format
   * @returns {Object} - Message in backend format
   */
  mapToBackendFormat(chatKitMessage) {
    // Determine context type based on whether user selected text
    let context = null;
    
    if (chatKitMessage.selectedText) {
      // User selected text - use user_selected context
      context = {
        type: "user_selected",
        content: chatKitMessage.selectedText
      };
    } else {
      // No selected text - use Qdrant retrieval
      context = {
        type: "qdrant",
        filters: null,
        max_chunks: 10
      };
    }

    return {
      query: chatKitMessage.text || chatKitMessage.content,
      context: context
    };
  }

  /**
   * Maps backend response format to ChatKit format
   * @param {Object} backendResponse - Response from our backend
   * @returns {Object} - Response in ChatKit-compatible format
   */
  mapToChatKitFormat(backendResponse) {
    if (!backendResponse) {
      return null;
    }

    // Map the backend response to ChatKit message format
    const chatKitResponse = {
      id: backendResponse.id || Date.now().toString(),
      text: backendResponse.answer || backendResponse.content || '',
      sender: 'assistant',
      timestamp: new Date().toISOString(),
      citations: backendResponse.citations || [],
      confidence: backendResponse.confidence || 'grounded'
    };

    // If the response indicates insufficient context, adjust accordingly
    if (backendResponse.answer &&
        (backendResponse.answer.includes("I don't know based on the provided text") ||
         backendResponse.confidence === 'insufficient_context')) {
      chatKitResponse.confidence = 'insufficient_context';
    }

    return chatKitResponse;
  }

  /**
   * Makes a request to our backend API
   * @param {Object} message - Message in ChatKit format
   * @returns {Promise<Object>} - Response in ChatKit format
   */
  async sendToBackend(message) {
    try {
      const backendRequest = this.mapToBackendFormat(message);

      const response = await fetch(`${this.backendUrl}/api/v1/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer dev-api-key-change-in-production'
        },
        body: JSON.stringify(backendRequest)
      });

      if (!response.ok) {
        throw new Error(`Backend API error: ${response.status} ${response.statusText}`);
      }

      const backendResponse = await response.json();
      return this.mapToChatKitFormat(backendResponse);
    } catch (error) {
      console.error('API Adapter error:', error);
      throw error;
    }
  }

  /**
   * Validates if a response has proper citations
   * @param {Object} response - Response from backend
   * @returns {boolean} - True if response has valid citations
   */
  hasValidCitations(response) {
    if (!response || !response.citations) {
      return false;
    }

    return Array.isArray(response.citations) &&
           response.citations.length > 0 &&
           response.citations.every(citation =>
             citation.chunk_id && citation.module && citation.chapter && citation.anchor
           );
  }

  /**
   * Checks if response indicates insufficient context
   * @param {Object} response - Response from backend
   * @returns {boolean} - True if response indicates insufficient context
   */
  hasInsufficientContext(response) {
    if (!response) {
      return true;
    }

    const answer = response.answer || response.content || '';
    return answer.includes("I don't know based on the provided text") ||
           response.confidence === 'insufficient_context';
  }
}

export default APIAdapter;
