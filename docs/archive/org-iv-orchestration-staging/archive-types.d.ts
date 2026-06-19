declare const process: {
  argv: string[];
  cwd(): string;
  env: Record<string, string | undefined>;
};

declare const Buffer: {
  byteLength(value: string): number;
};

declare module 'child_process' {
  interface StreamLike {
    on(event: 'data', listener: (data: { toString(): string }) => void): void;
  }

  interface ChildProcessLike {
    stdout: StreamLike;
    stderr: StreamLike;
    on(event: 'close', listener: (code: number | null) => void): void;
    on(event: 'error', listener: (error: Error) => void): void;
  }

  export function spawn(command: string, args?: string[]): ChildProcessLike;
  export function exec(
    command: string,
    options: { cwd: string },
    callback: (
      error: (Error & { stderr?: string; stdout?: string }) | null,
      stdout: string,
      stderr: string
    ) => void
  ): void;
}

declare module 'fs/promises' {
  export function access(path: string): Promise<void>;
  export function mkdir(path: string, options?: { recursive?: boolean }): Promise<string | undefined>;
  export function readFile(path: string, encoding: BufferEncoding): Promise<string>;
  export function writeFile(path: string, data: string, encoding?: BufferEncoding): Promise<void>;
}

declare module 'https' {
  interface IncomingMessageLike {
    statusCode?: number;
    on(event: 'data', listener: (chunk: { toString(): string }) => void): void;
    on(event: 'end', listener: () => void): void;
  }

  interface ClientRequestLike {
    end(): void;
    on(event: 'error', listener: (error: Error) => void): void;
    write(data: string): void;
  }

  export function request(
    options: {
      headers: Record<string, string>;
      hostname: string;
      method: 'POST';
      path: string;
    },
    callback: (res: IncomingMessageLike) => void
  ): ClientRequestLike;

  const https: {
    request: typeof request;
  };

  export default https;
}

declare module 'js-yaml' {
  export function load(content: string): unknown;

  const yaml: {
    load: typeof load;
  };

  export default yaml;
}

declare module 'path' {
  export function dirname(path: string): string;
  export function join(...paths: string[]): string;
  export function resolve(...paths: string[]): string;

  const path: {
    dirname: typeof dirname;
    join: typeof join;
    resolve: typeof resolve;
  };

  export default path;
}

declare module 'url' {
  export function fileURLToPath(url: string | { toString(): string }): string;
}

declare module 'util' {
  export function promisify(fn: (...args: any[]) => void): any;
}

declare module '@langchain/community/vectorstores/chroma' {
  export class Chroma {
    constructor(embeddings: unknown, config: Record<string, unknown>);
    addDocuments(documents: unknown[]): Promise<void>;
    similaritySearch(
      query: string,
      limit: number
    ): Promise<Array<{ metadata: Record<string, unknown>; pageContent: string }>>;
  }
}

declare module '@langchain/core/documents' {
  export class Document {
    constructor(config: { metadata: Record<string, unknown>; pageContent: string });
  }
}

declare module '@langchain/google-genai' {
  export class ChatGoogleGenerativeAI {
    constructor(config: Record<string, unknown>);
    invoke(prompt: string): Promise<{ content: { toString(): string } | string }>;
  }

  export class GoogleGenerativeAIEmbeddings {
    constructor(config: Record<string, unknown>);
  }
}

type BufferEncoding = 'utf-8' | 'utf8';
