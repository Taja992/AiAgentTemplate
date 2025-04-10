import './App.css'
import { useState } from 'react'
import { ApiTest } from './components/system/ApiConnectionTest'
import { ChatPage } from './pages/Chat'
import { DocumentUpload } from './components/documents'
import { DocumentUploadResponse } from './services/api/api'

function App() {
  const [uploadStatus, setUploadStatus] = useState<{
    isError: boolean;
    message: string | null;
    response?: DocumentUploadResponse;
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

  return (
    <div className="app-container">
      <div className="main-content">
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
          
          <div className="api-test-container">
            <ApiTest />
          </div>
        </div>
        
        <div className="chat-section">
          <ChatPage />
        </div>
      </div>
    </div>
  )
}

export default App