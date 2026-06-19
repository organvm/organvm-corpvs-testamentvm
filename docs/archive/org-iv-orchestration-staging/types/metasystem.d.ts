export interface MetasystemEvent {
  payload: {
    action: string;
    pull_request: {
      body?: string | null;
      number: number;
      title: string;
    };
    repository: {
      full_name: string;
    };
    [key: string]: unknown;
  };
  type: string;
}
