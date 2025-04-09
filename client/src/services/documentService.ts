import { apiClient } from './apiClient';
import type { DocumentUploadRequest, RAGResponse, DocumentChunk } from './api/api';

/**
 * Document service for managing documents and RAG functionality
 */
export const documentService = {
  /**
   * Upload a document for processing and indexing
   * 
   * @param document Document details and content to upload
   * @returns Array of document chunk IDs
   */
  async uploadDocument(document: DocumentUploadRequest): Promise<string[]> {
    try {
      const response = await apiClient.api.uploadDocumentsApiRagDocumentsUploadPost(document);
      return response.data;
    } catch (error) {
      console.error('Document upload error:', error);
      throw error;
    }
  },

  /**
   * Perform a RAG query against the document collection
   * 
   * @param query The user's question
   * @param collectionName The document collection to search
   * @param numResults Number of document chunks to retrieve
   * @returns RAG-enhanced response with sources
   */
  async ragQuery(query: string, collectionName = 'default', numResults = 3): Promise<RAGResponse> {
    try {
      const response = await apiClient.api.queryDocumentsApiRagQueryPost({
        query,
        collection_name: collectionName,
        num_results: numResults
      });
      return response.data;
    } catch (error) {
      console.error('RAG query error:', error);
      throw error;
    }
  },
  
  /**
   * Retrieve documents from a collection based on a search query
   * 
   * @param collectionName The collection to search
   * @param query Search query string
   * @param topK Number of top documents to retrieve
   * @returns Array of document chunks
   */
  async retrieveDocuments(collectionName: string, query: string, topK = 3): Promise<DocumentChunk[]> {
    try {
      const response = await apiClient.api.retrieveDocumentsFromCollectionApiRagCollectionsCollectionNameDocumentsGet(
        collectionName,
        { query, top_k: topK }
      );
      return response.data;
    } catch (error) {
      console.error('Document retrieval error:', error);
      throw error;
    }
  },
  
  /**
   * Get all available document collections
   * 
   * @returns List of collection names
   */
  async getCollections(): Promise<string[]> {
    try {
      const response = await apiClient.api.listCollectionsApiRagCollectionsGet();
      return response.data;
    } catch (error) {
      console.error('Get collections error:', error);
      throw error;
    }
  }
};