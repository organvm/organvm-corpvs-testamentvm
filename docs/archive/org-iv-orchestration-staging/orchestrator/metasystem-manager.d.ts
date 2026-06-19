import type { TaskDispatcher } from '../orchestrator-agents/dispatcher.js';
import type { WorkspaceHealth } from '../orchestrator-agents/metasystem-manager.js';

export class MetasystemManager {
  dispatcher: TaskDispatcher;

  constructor(manifestPath: string);

  getUniverseHealth(): Promise<WorkspaceHealth[]>;
}
