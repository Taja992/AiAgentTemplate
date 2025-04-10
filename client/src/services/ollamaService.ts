import { apiClient } from './apiClient';
import type { OllamaModel } from './api/api';


export const ollamaService = {
/**
 * Get the list of available models from the Ollama API
 */

    async getModels(): Promise<OllamaModel[]> {
        try {
            const response = await apiClient.api.listAvailableModelsApiModelsGet();
            return response.data;
        } catch (error) {
            console.error('Error fetching models:', error);
            throw error;
        }
    }
};
