import React, { useState } from 'react';
import { chainService } from '../../services';
import './ChainConfig.css'; 

interface ChainConfigProps {
  onConfigSuccess?: (response: any) => void;
  onConfigError?: (error: any) => void;
}

const ChainConfig: React.FC<ChainConfigProps> = ({ onConfigSuccess, onConfigError }) => {
  const [systemMessage, setSystemMessage] = useState<string>('');
  const [temperature, setTemperature] = useState<number>(0.7);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTemperatureChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTemperature(parseFloat(e.target.value));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const config = {
        system_message: systemMessage,
        parameters: {
          temperature
        },
        name: "customizable" // Using the default customizable chain
      };

      const result = await chainService.configureChain(config);
      setSuccess("Chain configuration updated successfully!");
      
      if (onConfigSuccess) {
        onConfigSuccess(result);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to configure chain';
      setError(errorMessage);
      
      if (onConfigError) {
        onConfigError(err);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chain-config-window">
      <div className="chain-config-header">
        <h3>Configure AI System Prompt</h3>
      </div>
      
      <div className="chain-config-content">
        {error && (
          <div className="chat-error">
            {error}
          </div>
        )}
        
        {success && (
          <div className="chain-config-success">
            {success}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div className="chain-config-input-group">
            <label>System Message:</label>
            <textarea
              className="chain-config-textarea"
              rows={6}
              placeholder="Enter instructions for the AI assistant..."
              value={systemMessage}
              onChange={(e) => setSystemMessage(e.target.value)}
              disabled={isLoading}
            />
            <small className="chain-config-help">
              This prompt defines how the AI will behave in all conversations
            </small>
          </div>
          
          <div className="chain-config-input-group">
            <label>Temperature: {temperature}</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={temperature}
              onChange={handleTemperatureChange}
              className="chain-config-slider"
              disabled={isLoading}
            />
            <small className="chain-config-help">
              Controls randomness: Lower values are more deterministic, higher more creative
            </small>
          </div>
          
          <button 
            type="submit" 
            className="send-button"
            disabled={isLoading || !systemMessage.trim()}
          >
            {isLoading ? 'Updating...' : 'Update Configuration'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChainConfig;