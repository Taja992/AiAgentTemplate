import { apiClient } from './apiClient';
import type { Message, AgentResponse } from './api/api';

/**
 * Chat service providing interface to the AI Agent API
 */
export const chatService = {
  /**
   * Send a message to the AI agent and get a response
   * 
   * @param messages Array of conversation messages
   * @param options Optional parameters like temperature, maxTokens
   * @returns The AI agent's response
   */
  async chat(messages: Message[], options: {
    temperature?: number;
    max_tokens?: number;
    use_rag?: boolean;
    rag_collection?: string;
    skip_memory?: boolean;
  } = {}): Promise<AgentResponse> {
    try {
      const response = await apiClient.api.chatApiChatPost({
        messages,
        temperature: options.temperature ?? 0.7,
        max_tokens: options.max_tokens ?? 1000
      }, {
        use_rag: options.use_rag ?? true,
        rag_collection: options.rag_collection ?? 'default',
        skip_memory: options.skip_memory ?? false
      });
      
      return response.data;
    } catch (error) {
      console.error('Chat service error:', error);
      throw error;
    }
  },

  /**
   * Check the health status of the API
   * 
   * @returns Health status information
   */
  async health() {
    try {
      const response = await apiClient.api.healthCheckApiHealthGet();
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
};