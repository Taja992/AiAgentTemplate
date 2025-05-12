import './App.css'
import { useState } from 'react'
import { ApiTest } from './components/system/ApiConnectionTest'
import { ChainConfig } from './components/system'
import { ChatPage } from './pages/Chat'
import { DocumentUpload } from './components/documents'
import { DocumentUploadResponse, ChainConfigurationResponse } from './services/api/api'

function App() {
  const [uploadStatus, setUploadStatus] = useState<{
    isError: boolean;
    message: string | null;
    response?: DocumentUploadResponse;
  }>({
    isError: false,
    message: null
  });

  const [chainConfigStatus, setChainConfigStatus] = useState<{
    isError: boolean;
    message: string | null;
  }>({
    isError: false,
    message: null
  });

  const handleUploadComplete = (response: DocumentUploadResponse) => {
    setUploadStatus({
      isError: false,
      message: `Successfully uploaded ${response.document_count} document chunks to collection "${response.collection_name}"!`,
      response
    });
  };

  const handleError = (error: Error) => {
    setUploadStatus({
      isError: true,
      message: `Error: ${error.message}`
    });
  };

  const handleChainConfigSuccess = (response: ChainConfigurationResponse) => {
    setChainConfigStatus({
      isError: false,
      message: `Successfully configured chain "${response.name}" with custom system message!`
    });
  };

  const handleChainConfigError = (error: any) => {
    setChainConfigStatus({
      isError: true,
      message: `Error: ${error.message || 'Failed to configure chain'}`
    });
  };

  return (
    <div className="app-container">
      <div className="main-content">
        {/* Left Panel */}
        <div className="document-section">
          <DocumentUpload 
            onUploadComplete={handleUploadComplete}
            onError={handleError}
          />
          
          {uploadStatus.message && (
            <div className={`status-message ${uploadStatus.isError ? 'error' : 'success'}`}>
              <p>{uploadStatus.message}</p>
              {!uploadStatus.isError && uploadStatus.response && (
                <>
                  <p>Collection: {uploadStatus.response.collection_name}</p>
                  <p>Uploaded {uploadStatus.response.document_count} document chunks</p>
                </>
              )}
            </div>
          )}
          
          <div className="chain-config-container">
            <ChainConfig
              onConfigSuccess={handleChainConfigSuccess}
              onConfigError={handleChainConfigError}
            />
            
            {chainConfigStatus.message && (
              <div className={`status-message ${chainConfigStatus.isError ? 'error' : 'success'}`}>
                <p>{chainConfigStatus.message}</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Center Panel */}
        <div className="chat-section">
          <ChatPage />
        </div>
        
        {/* Right Panel */}
        <div className="api-test-section">
          <ApiTest />
        </div>
      </div>
    </div>
  )
}

export default App