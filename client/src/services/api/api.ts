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
   * Use Customizable Chain
   * Use custom chain or not
   */
  use_customizable_chain?: boolean | null;
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
 * ChainConfiguration
 * Configuration for a customizable model chains.
 */
export interface ChainConfiguration {
  /** System Message */
  system_message?: string | null;
  /** Parameters */
  parameters?: object;
  /** Name */
  name?: string | null;
  /** Enabled */
  enabled?: boolean | null;
}

/**
 * ChainConfigurationResponse
 * Response after updating a chain configuration
 */
export interface ChainConfigurationResponse {
  /** Name */
  name: string;
  /** System Message */
  system_message: string;
  /** Parameters */
  parameters: object;
  /** Enabled */
  enabled?: boolean | null;
  /**
   * Message
   * @default "Chain configuration updated successfully"
   */
  message?: string;
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

/**
 * DocumentUploadResponse
 * Response for document upload operations.
 */
export interface DocumentUploadResponse {
  /**
   * Document Ids
   * IDs of the uploaded document chunks
   */
  document_ids: string[];
  /**
   * Document Count
   * Number of document chunks created
   */
  document_count: number;
  /**
   * Collection Name
   * Collection where documents were stored
   */
  collection_name: string;
  /**
   * Success
   * Indicates if the upload was successful
   * @default true
   */
  success?: boolean;
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
 * OllamaModel
 * Schema for Ollama model information
 */
export interface OllamaModel {
  /**
   * Id
   * Model identifier(format: ollama:{model_name})
   */
  id: string;
  /**
   * Name
   * Model name
   */
  name: string;
  /**
   * Size
   * Model size in bytes
   */
  size: any;
  /**
   * Modified At
   * Last modified date of the model
   */
  modified_at?: string | null;
  /**
   * Description
   * Description of the model
   */
  description?: string | null;
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

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
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
      this.request<DocumentUploadResponse, HTTPValidationError>({
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
      this.request<DocumentUploadResponse, HTTPValidationError>({
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
     * @name ListAvailableModelsApiOllamaModelsGet
     * @summary List Available Models
     * @request GET:/api/ollama/models/
     */
    listAvailableModelsApiOllamaModelsGet: (params: RequestParams = {}) =>
      this.request<OllamaModel[], any>({
        path: `/api/ollama/models/`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * @description Configure a customizable chain with a system message and parameters This gives the user the power to set a custom chain for instructions and parameters for the model.
     *
     * @tags chains
     * @name ConfigureChainApiChainsConfigurePost
     * @summary Configure Chain
     * @request POST:/api/chains/configure
     */
    configureChainApiChainsConfigurePost: (data: ChainConfiguration, params: RequestParams = {}) =>
      this.request<ChainConfigurationResponse, HTTPValidationError>({
        path: `/api/chains/configure`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),
  };
}
