import React, { useState, useRef, useEffect } from 'react';
import { documentService } from '../../services/documentService';
import './DocumentUpload.css';
import { DocumentUploadResponse } from '../../services/api/api';

interface DocumentUploadProps {
  onUploadComplete?: (response: DocumentUploadResponse) => void;
  onError?: (error: Error) => void;
}

export function DocumentUpload({ onUploadComplete, onError }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [collections, setCollections] = useState<string[]>([]);
  const [selectedCollection, setSelectedCollection] = useState<string>("default");
  const [newCollection, setNewCollection] = useState<string>("");
  const [isCreatingNew, setIsCreatingNew] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [chunkSize, setChunkSize] = useState<number>(1000);
  const [chunkOverlap, setChunkOverlap] = useState<number>(200);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch available collections on component mount
  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const collectionsList = await documentService.getCollections();
        setCollections(collectionsList);
      } catch (error) {
        console.error("Failed to fetch collections:", error);
        onError?.(error as Error);
      }
    };

    fetchCollections();
  }, [onError]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) return;
    
    const collectionToUse = isCreatingNew && newCollection.trim() ? newCollection.trim() : selectedCollection;
    
    setIsUploading(true);
    try {
      // Use the documentService with the apiClient to upload the file
      const fileUploadData = {
        file: file,
        collection_name: collectionToUse,
        chunk_size: chunkSize,
        chunk_overlap: chunkOverlap
      };
      
      // Use the API client through the documentService
      const response = await documentService.uploadFile(fileUploadData);
      
      // Reset the form
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      
      onUploadComplete?.(response);
      
      // If we created a new collection, refresh the collections list
      if (isCreatingNew && newCollection.trim()) {
        const updatedCollections = await documentService.getCollections();
        setCollections(updatedCollections);
        setSelectedCollection(newCollection.trim());
        setNewCollection("");
        setIsCreatingNew(false);
      }
    } catch (error) {
      console.error("File upload failed:", error);
      onError?.(error as Error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="document-upload">
      <h2>Upload Document</h2>
      <form onSubmit={handleSubmit}>
        <div className="upload-field">
          <label htmlFor="document-file">Select Document:</label>
          <input
            type="file"
            id="document-file"
            onChange={handleFileChange}
            disabled={isUploading}
            ref={fileInputRef}
            required
          />
        </div>
        
        <div className="collection-field">
          <label>Document Collection:</label>
          
          {!isCreatingNew ? (
            <div className="collection-select-container">
              <select
                value={selectedCollection}
                onChange={(e) => setSelectedCollection(e.target.value)}
                disabled={isUploading}
                className="collection-select"
              >
                {collections.map(collection => (
                  <option key={collection} value={collection}>{collection}</option>
                ))}
              </select>
              <button
                type="button"
                className="new-collection-btn"
                onClick={() => setIsCreatingNew(true)}
                disabled={isUploading}
              >
                New Collection
              </button>
            </div>
          ) : (
            <div className="new-collection-container">
              <input
                type="text"
                value={newCollection}
                onChange={(e) => setNewCollection(e.target.value)}
                placeholder="Enter new collection name"
                disabled={isUploading}
                className="new-collection-input"
              />
              <button
                type="button"
                className="cancel-btn"
                onClick={() => setIsCreatingNew(false)}
                disabled={isUploading}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
        
        <div className="chunking-options">
          <div className="chunk-field">
            <label htmlFor="chunk-size">Chunk Size:</label>
            <input
              type="number"
              id="chunk-size"
              value={chunkSize}
              onChange={(e) => setChunkSize(parseInt(e.target.value))}
              min="100"
              max="10000"
              disabled={isUploading}
            />
          </div>
          
          <div className="chunk-field">
            <label htmlFor="chunk-overlap">Chunk Overlap:</label>
            <input
              type="number"
              id="chunk-overlap"
              value={chunkOverlap}
              onChange={(e) => setChunkOverlap(parseInt(e.target.value))}
              min="0"
              max={chunkSize - 50}
              disabled={isUploading}
            />
          </div>
        </div>
        
        <button 
          type="submit" 
          className="upload-btn"
          disabled={!file || isUploading}
        >
          {isUploading ? 'Uploading...' : 'Upload Document'}
        </button>
      </form>
    </div>
  );
}