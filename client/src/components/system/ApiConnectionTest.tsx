import { useState } from 'react';
import { chatService } from '../../services';

export function ApiTest() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [response, setResponse] = useState<any>(null);

  const testHealthCheck = async () => {
    setStatus('loading');
    try {
      const data = await chatService.health();
      setResponse(data);
      setStatus('success');
    } catch (error) {
      console.error('Health check failed:', error);
      setResponse(error);
      setStatus('error');
    }
  };

  return (
    <div className="api-test">
      <h2>API Connection Test</h2>
      <button 
        onClick={testHealthCheck}
        disabled={status === 'loading'}
      >
        {status === 'loading' ? 'Checking...' : 'Test API Connection'}
      </button>
      
      {status === 'success' && (
        <div className="success">
          <p>✅ Connected successfully!</p>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
      
      {status === 'error' && (
        <div className="error">
          <p>❌ Connection failed. Make sure the API is running at http://localhost:8000</p>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}