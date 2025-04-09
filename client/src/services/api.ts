/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/**
 * AgentRequest
 * Represents the complete request from a client to the agent.
 *
 * Similar to C# API controller request model.
 * Contains all parameters needed to generate a response, including
 * conversation history, model selection, and generation parameters.
 */
export interface AgentRequest {
  /**
   * Messages
   * List of conversation messages
   */
  messages: Message[];
  /**
   * Model
   * Model to use for generating response (Like ollama:llama2)
   */
  model?: string | null;
  /**
   * Temperature
   * Creativity parameter (0-1)
   * @default 0.7
   */
  temperature?: number;
  /**
   * Max Tokens
   * Maximum number of tokens to generate
   * @default 1000
   */
  max_tokens?: number;
  /**
   * Additional Params
   * Additional model-specific parameters
   */
  additional_params?: object;
}

/**
 * AgentResponse
 * Response schema for agent interactions
 */
export interface AgentResponse {
  /**
   * Response
   * Response from the model
   */
  response: string;
  /**
   * Model
   * Model used for generating the response
   */
  model: string;
  /**
   * Usage
   * Token usage information
   */
  usage?: object;
}

/** Body_upload_file_api_rag_documents_upload_file_post */
export interface BodyUploadFileApiRagDocumentsUploadFilePost {
  /**
   * File
   * @format binary
   */
  file: File;
  /**
   * Collection Name
   * @default "default"
   */
  collection_name?: string;
  /**
   * Chunk Size
   * @default 1000
   */
  chunk_size?: number;
  /**
   * Chunk Overlap
   * @default 200
   */
  chunk_overlap?: number;
}

/**
 * DocumentChunk
 * A chunk of text from a document with its metadata.
 */
export interface DocumentChunk {
  /**
   * Content
   * Text content of the chunk
   */
  content: string;
  /** Metadata for the document */
  metadata?: DocumentMetadata;
  /**
   * Chunk Id
   * Unique identifier for the chunk
   */
  chunk_id?: string | null;
  /**
   * Embedding
   * Vector embedding of the chunk
   */
  embedding?: number[] | null;
}

/**
 * DocumentMetadata
 * Metadata for a document.
 */
export interface DocumentMetadata {
  /**
   * Source
   * Source of the document(e.g., URL, file path)
   */
  source?: string | null;
  /**
   * Author
   * Author of the document
   */
  author?: string | null;
  /**
   * Created At
   * Creation date of the document
   */
  created_at?: string | null;
  /**
   * Document Type
   * Type of the document (e.g., PDF, DOCX)
   */
  document_type?: string | null;
  /**
   * Page Number
   * Page number for paginated documents
   */
  page_number?: number | null;
  /**
   * Extra
   * Additional metadata fields
   */
  extra?: object;
}

/**
 * DocumentUploadRequest
 * Request for uploading a document.
 */
export interface DocumentUploadRequest {
  /**
   * Document Name
   * Name of the document
   */
  document_name: string;
  /**
   * Content
   * Content of the document
   */
  content: string;
  /** Optional metadata for the document */
  metadata?: DocumentMetadata | null;
  /**
   * Collection Name
   * Collection name to store the document in
   * @default "default"
   */
  collection_name?: string;
  /**
   * Chunk Size
   * Size of each chunk in characters
   * @default 1000
   */
  chunk_size?: number;
  /**
   * Chunk Overlap
   * Overlap size between chunks in characters
   * @default 200
   */
  chunk_overlap?: number;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/**
 * HealthResponse
 * Model for Health Check Response
 */
export interface HealthResponse {
  /** Status */
  status: string;
  /** Version */
  version: string;
  /** Timestamp */
  timestamp: number;
  /** Uptime */
  uptime: number;
  /** Environment */
  environment: string;
  /** System Info */
  system_info: object;
  /** Services */
  services: Record<string, string>;
}

/**
 * Message
 * A message in a conversation with a model.
 */
export interface Message {
  /**
   * Role
   * The role of the messeng sender (ex. 'user, 'assistant', 'system').
   */
  role: string;
  /**
   * Content
   * The content of the message.
   */
  content: string;
}

/**
 * RAGRequest
 * Request for a RAG-augmented response.
 */
export interface RAGRequest {
  /**
   * Query
   * User query or retrieval request
   */
  query: string;
  /**
   * Collection Name
   * Name of document collection to query
   * @default "default"
   */
  collection_name?: string | null;
  /**
   * Num Results
   * Number of documents to retrieve
   * @default 3
   */
  num_results?: number;
  /**
   * Use Semantic Ranker
   * Whether to use semantic ranking
   * @default true
   */
  use_semantic_ranker?: boolean;
  /**
   * Include Sources
   * Whether to include source references in response
   * @default true
   */
  include_sources?: boolean;
  /**
   * Model
   * Model to use for generation
   */
  model?: string | null;
}

/**
 * RAGResponse
 * Response from RAG-augmented query.
 */
export interface RAGResponse {
  /**
   * Answer
   * Generated answer
   */
  answer: string;
  /**
   * Sources
   * Source documents used for generation
   */
  sources?: DocumentChunk[];
  /**
   * Model
   * Model used for generation
   */
  model: string;
  /**
   * Embedding Model
   * Model used for embeddings
   */
  embedding_model?: string | null;
  /**
   * Usage
   * Token usage information
   */
  usage?: object;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, HeadersDefaults, ResponseType } from "axios";
import axios from "axios";

export type QueryParamsType = Record<string | number, any>;

export interface FullRequestParams extends Omit<AxiosRequestConfig, "data" | "params" | "url" | "responseType"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseType;
  /** request body */
  body?: unknown;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> extends Omit<AxiosRequestConfig, "data" | "cancelToken"> {
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<AxiosRequestConfig | void> | AxiosRequestConfig | void;
  secure?: boolean;
  format?: ResponseType;
}

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public instance: AxiosInstance;
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private secure?: boolean;
  private format?: ResponseType;

  constructor({ securityWorker, secure, format, ...axiosConfig }: ApiConfig<SecurityDataType> = {}) {
    this.instance = axios.create({ ...axiosConfig, baseURL: axiosConfig.baseURL || "" });
    this.secure = secure;
    this.format = format;
    this.securityWorker = securityWorker;
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected mergeRequestParams(params1: AxiosRequestConfig, params2?: AxiosRequestConfig): AxiosRequestConfig {
    const method = params1.method || (params2 && params2.method);

    return {
      ...this.instance.defaults,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...((method && this.instance.defaults.headers[method.toLowerCase() as keyof HeadersDefaults]) || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected stringifyFormItem(formItem: unknown) {
    if (typeof formItem === "object" && formItem !== null) {
      return JSON.stringify(formItem);
    } else {
      return `${formItem}`;
    }
  }

  protected createFormData(input: Record<string, unknown>): FormData {
    if (input instanceof FormData) {
      return input;
    }
    return Object.keys(input || {}).reduce((formData, key) => {
      const property = input[key];
      const propertyContent: any[] = property instanceof Array ? property : [property];

      for (const formItem of propertyContent) {
        const isFileType = formItem instanceof Blob || formItem instanceof File;
        formData.append(key, isFileType ? formItem : this.stringifyFormItem(formItem));
      }

      return formData;
    }, new FormData());
  }

  public request = async <T = any, _E = any>({
    secure,
    path,
    type,
    query,
    format,
    body,
    ...params
  }: FullRequestParams): Promise<AxiosResponse<T>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const responseFormat = format || this.format || undefined;

    if (type === ContentType.FormData && body && body !== null && typeof body === "object") {
      body = this.createFormData(body as Record<string, unknown>);
    }

    if (type === ContentType.Text && body && body !== null && typeof body !== "string") {
      body = JSON.stringify(body);
    }

    return this.instance.request({
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type ? { "Content-Type": type } : {}),
      },
      params: query,
      responseType: responseFormat,
      data: body,
      url: path,
    });
  };
}

/**
 * @title AI Agent API
 * @version 0.1.0
 *
 * API for interacting with various AI models.
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * @description Chat with an AI agent using various models. the model is specified in the request, defaulting to the configurted default model. This endpoint works with all supported model providers (Ollama, Huggingface, etc.) without changing the API contract
     *
     * @tags agents
     * @name ChatApiChatPost
     * @summary Chat
     * @request POST:/api/chat
     */
    chatApiChatPost: (
      data: AgentRequest,
      query?: {
        /**
         * Skip Memory
         * @default false
         */
        skip_memory?: boolean;
        /**
         * Conversation Id
         * @default "default"
         */
        conversation_id?: string | null;
        /**
         * Use Rag
         * @default true
         */
        use_rag?: boolean;
        /**
         * Rag Collection
         * @default "default"
         */
        rag_collection?: string;
        /**
         * Rag Num Results
         * @default 3
         */
        rag_num_results?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<AgentResponse, HTTPValidationError>({
        path: `/api/chat`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Health Check Endpoint Checks: - Application status - Version Info - System resources - Connected services status
     *
     * @tags health
     * @name HealthCheckApiHealthGet
     * @summary Health Check
     * @request GET:/api/health
     */
    healthCheckApiHealthGet: (params: RequestParams = {}) =>
      this.request<HealthResponse, any>({
        path: `/api/health`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Upload a document for processing and indexing.
     *
     * @tags rag
     * @name UploadDocumentsApiRagDocumentsUploadPost
     * @summary Upload Documents
     * @request POST:/api/rag/documents/upload
     */
    uploadDocumentsApiRagDocumentsUploadPost: (data: DocumentUploadRequest, params: RequestParams = {}) =>
      this.request<string[], HTTPValidationError>({
        path: `/api/rag/documents/upload`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Upload a file (PDF, TXT, etc) for processing and indexing
     *
     * @tags rag
     * @name UploadFileApiRagDocumentsUploadFilePost
     * @summary Upload File
     * @request POST:/api/rag/documents/upload-file
     */
    uploadFileApiRagDocumentsUploadFilePost: (
      data: BodyUploadFileApiRagDocumentsUploadFilePost,
      params: RequestParams = {},
    ) =>
      this.request<string[], HTTPValidationError>({
        path: `/api/rag/documents/upload-file`,
        method: "POST",
        body: data,
        type: ContentType.FormData,
        format: "json",
        ...params,
      }),

    /**
     * @description Retrieve a specific document by ID
     *
     * @tags rag
     * @name GetDocumentApiRagDocumentsDocumentIdGet
     * @summary Get Document
     * @request GET:/api/rag/documents/{document_id}
     */
    getDocumentApiRagDocumentsDocumentIdGet: (documentId: string, params: RequestParams = {}) =>
      this.request<DocumentChunk, HTTPValidationError>({
        path: `/api/rag/documents/${documentId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Delete a specific document by ID
     *
     * @tags rag
     * @name DeleteDocumentApiRagDocumentsDocumentIdDelete
     * @summary Delete Document
     * @request DELETE:/api/rag/documents/{document_id}
     */
    deleteDocumentApiRagDocumentsDocumentIdDelete: (documentId: string, params: RequestParams = {}) =>
      this.request<boolean, HTTPValidationError>({
        path: `/api/rag/documents/${documentId}`,
        method: "DELETE",
        format: "json",
        ...params,
      }),

    /**
     * @description List all documents in the system
     *
     * @tags rag
     * @name ListDocumentsApiRagDocumentsGet
     * @summary List Documents
     * @request GET:/api/rag/documents
     */
    listDocumentsApiRagDocumentsGet: (params: RequestParams = {}) =>
      this.request<DocumentChunk[], any>({
        path: `/api/rag/documents`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Query documents using RAG to generate an answer.
     *
     * @tags rag
     * @name QueryDocumentsApiRagQueryPost
     * @summary Query Documents
     * @request POST:/api/rag/query
     */
    queryDocumentsApiRagQueryPost: (data: RAGRequest, params: RequestParams = {}) =>
      this.request<RAGResponse, HTTPValidationError>({
        path: `/api/rag/query`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Retrieve documents from a specific collection based on a query
     *
     * @tags rag
     * @name RetrieveDocumentsFromCollectionApiRagCollectionsCollectionNameDocumentsGet
     * @summary Retrieve Documents From Collection
     * @request GET:/api/rag/collections/{collection_name}/documents
     */
    retrieveDocumentsFromCollectionApiRagCollectionsCollectionNameDocumentsGet: (
      collectionName: string,
      query: {
        /**
         * Query
         * Search query
         */
        query: string;
        /**
         * Top K
         * Number of top documents to retrieve
         * @default 3
         */
        top_k?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<DocumentChunk[], HTTPValidationError>({
        path: `/api/rag/collections/${collectionName}/documents`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * @description Delete a collection of documents
     *
     * @tags rag
     * @name DeleteCollectionApiRagCollectionsCollectionNameDelete
     * @summary Delete Collection
     * @request DELETE:/api/rag/collections/{collection_name}
     */
    deleteCollectionApiRagCollectionsCollectionNameDelete: (collectionName: string, params: RequestParams = {}) =>
      this.request<boolean, HTTPValidationError>({
        path: `/api/rag/collections/${collectionName}`,
        method: "DELETE",
        format: "json",
        ...params,
      }),

    /**
     * @description List all available collections
     *
     * @tags rag
     * @name ListCollectionsApiRagCollectionsGet
     * @summary List Collections
     * @request GET:/api/rag/collections
     */
    listCollectionsApiRagCollectionsGet: (params: RequestParams = {}) =>
      this.request<string[], any>({
        path: `/api/rag/collections`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Fetch all available models from Ollama
     *
     * @tags models
     * @name ListAvailableModelsApiModelsGet
     * @summary List Available Models
     * @request GET:/api/models/
     */
    listAvailableModelsApiModelsGet: (params: RequestParams = {}) =>
      this.request<object[], any>({
        path: `/api/models/`,
        method: "GET",
        format: "json",
        ...params,
      }),
  };
}
