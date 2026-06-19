import type { MetasystemEvent } from '../types/metasystem.js';

export const systemBus: {
  subscribe(handler: (event: MetasystemEvent) => Promise<void> | void): Promise<void> | void;
};
