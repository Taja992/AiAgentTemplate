import { apiClient } from './apiClient';
import { ChainConfiguration, ChainConfigurationResponse } from './api/api';

/**
 * Chain service for configuring model chains
 */
export const chainService = {
    /**
     * Configure a chain with custom system message and parameters
     * 
     * @param config Chain configuration containing system message and parameters
     * @returns Promise with the configuration response
     */
    async configureChain(config: ChainConfiguration): Promise<ChainConfigurationResponse> {
        try{
            const response = await apiClient.api.configureChainApiChainsConfigurePost(config);
            return response.data;
        } catch (error) {
            console.error('Error configuring chain:', error);
            throw error;
        }
    }
};