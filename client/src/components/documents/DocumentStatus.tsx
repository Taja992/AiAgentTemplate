interface DocumentUploadStatusProps {
  isError: boolean;
  message: string | null;
  documentIds?: string[];
}

export function DocumentUploadStatus({ isError, message, documentIds }: DocumentUploadStatusProps) {
  if (!message) return null;

  return (
    <div className={`upload-status ${isError ? 'error' : 'success'}`}>
      <p>{message}</p>
      
      {!isError && documentIds && documentIds.length > 0 && (
        <div className="document-ids">
          <p>Document IDs:</p>
          <ul>
            {documentIds.map(id => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}