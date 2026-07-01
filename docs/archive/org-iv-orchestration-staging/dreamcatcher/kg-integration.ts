/**
 * Knowledge Graph Integration for Dreamcatcher Agents
 *
 * Objective: Enable agents to learn from past work and share knowledge
 * across all projects in the metasystem.
 */

import { spawn } from 'child_process';
import path from 'path';

export interface DecisionContext {
  decision: string;
  rationale: string;
  category: 'architecture' | 'design' | 'implementation' | 'testing' | 'deployment';
  project: string;
  tags?: string[];
}

export interface KGQueryResult {
  entities: any[];
  relationships: any[];
}

export interface SimilarWorkResult {
  project: string;
  decision: string;
  rationale: string;
  relevance_score: number;
}

export class KnowledgeGraphIntegration {
  private kgPath: string;
  private pythonPath: string;

  constructor(kgDbPath: string = '~/.metasystem/metastore.db') {
    this.kgPath = kgDbPath;
    this.pythonPath = '~/Workspace/metasystem-core/.venv/bin/python3';
  }

  /**
   * Query knowledge graph for past decisions related to a topic
   * This helps agents avoid re-inventing solutions
   */
  async findPastDecisions(query: string, projectName?: string): Promise<any[]> {
    const args = ['search', '--query', query];
    if (projectName) {
      args.push('--project', projectName);
    }

    const result = await this.callKG('knowledge_graph.py', args);

    if (result.entities) {
      return result.entities
        .filter((e: any) => e.type === 'decision')
        .map((e: any) => ({
          decision: e.metadata?.decision || e.name,
          rationale: e.metadata?.rationale || '',
          category: e.metadata?.category || 'general',
          project: e.metadata?.project || 'unknown',
          created_at: e.created_at
        }));
    }

    return [];
  }

  /**
   * Find files recently modified in a project
   * Helps agents understand what's been worked on
   */
  async findRecentFileChanges(projectName: string, hours: number = 24): Promise<any[]> {
    const result = await this.callKG('knowledge_graph.py', [
      'query',
      '--type', 'file',
      '--project', projectName
    ]);

    if (result.entities) {
      const now = new Date().getTime();
      const cutoff = now - (hours * 60 * 60 * 1000);

      return result.entities
        .filter((e: any) => {
          const modified = new Date(e.modified_at || e.created_at).getTime();
          return modified > cutoff;
        })
        .map((e: any) => ({
          path: e.path,
          operation: e.metadata?.operation || 'unknown',
          modified_at: e.modified_at || e.created_at
        }));
    }

    return [];
  }

  /**
   * Find similar work done in other projects
   * Enables cross-project learning and pattern reuse
   */
  async findSimilarWork(description: string, currentProject: string): Promise<SimilarWorkResult[]> {
    // Search for decisions/entities with similar keywords
    const result = await this.callKG('knowledge_graph.py', [
      'search',
      '--query', description
    ]);

    if (!result.entities) return [];

    return result.entities
      .filter((e: any) => e.type === 'decision' && e.metadata?.project !== currentProject)
      .map((e: any): SimilarWorkResult => ({
        project: e.metadata?.project || 'unknown',
        decision: e.metadata?.decision || e.name,
        rationale: e.metadata?.rationale || '',
        relevance_score: e.relevance_score || 0
      }))
      .sort((a: SimilarWorkResult, b: SimilarWorkResult) => b.relevance_score - a.relevance_score)
      .slice(0, 5); // Top 5 most relevant
  }

  /**
   * Log a decision made by an agent
   * Creates a decision entity in the knowledge graph
   */
  async logDecision(context: DecisionContext): Promise<string> {
    const result = await this.callKG('knowledge_graph.py', [
      'insert',
      '--type', 'decision',
      '--name', context.decision,
      '--metadata', JSON.stringify({
        decision: context.decision,
        rationale: context.rationale,
        category: context.category,
        project: context.project,
        tags: context.tags || [],
        created_by: 'dreamcatcher-agent'
      })
    ]);

    return result.entity_id || 'unknown';
  }

  /**
   * Log a file change made by an agent
   * Tracks what files were modified during autonomous work
   */
  async logFileChange(filePath: string, operation: 'read' | 'write' | 'edit' | 'delete', projectName: string): Promise<void> {
    await this.callKG('knowledge_graph.py', [
      'insert',
      '--type', 'file',
      '--path', filePath,
      '--metadata', JSON.stringify({
        operation,
        project: projectName,
        modified_by: 'dreamcatcher-agent',
        timestamp: new Date().toISOString()
      })
    ]);
  }

  /**
   * Get all projects managed by omni
   * Returns list of projects with seed.yaml files
   */
  async getAllProjects(): Promise<any[]> {
    const result = await this.callKG('discovery_engine.py', ['discover']);

    if (result.projects) {
      return result.projects.map((p: any) => ({
        name: p.name,
        path: p.path,
        tech_stack: p.metadata?.tech_stack || {},
        description: p.metadata?.description || ''
      }));
    }

    return [];
  }

  /**
   * Generate documentation from knowledge graph data
   * Creates markdown docs from entities and relationships
   */
  async generateDocumentation(projectName?: string): Promise<string> {
    const args = ['generate-docs'];
    if (projectName) {
      args.push('--project', projectName);
    }

    const result = await this.callKG('knowledge_graph.py', args);
    return result.documentation || '';
  }

  /**
   * Get context summary for a project
   * Returns recent decisions, file changes, and key entities
   */
  async getProjectContext(projectName: string, hours: number = 168): Promise<any> {
    const [decisions, files, entities] = await Promise.all([
      this.findPastDecisions('', projectName),
      this.findRecentFileChanges(projectName, hours),
      this.callKG('knowledge_graph.py', [
        'query',
        '--type', 'project',
        '--name', projectName
      ])
    ]);

    return {
      project: projectName,
      recent_decisions: decisions.slice(0, 10), // Last 10 decisions
      recent_files: files.slice(0, 20),         // Last 20 file changes
      metadata: entities.entities?.[0]?.metadata || {}
    };
  }

  /**
   * Call knowledge graph Python scripts
   * Private helper method
   */
  private async callKG(scriptName: string, args: string[]): Promise<any> {
    return new Promise((resolve, reject) => {
      const scriptPath = path.join('~/Workspace/metasystem-core', scriptName);
      const proc = spawn(this.pythonPath, [scriptPath, ...args]);

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      proc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      proc.on('close', (code) => {
        if (code !== 0) {
          console.warn(`[KG Integration] Warning: ${scriptName} exited with code ${code}`);
          console.warn(`stderr: ${stderr}`);
          resolve({}); // Return empty result on error, don't block agent work
          return;
        }

        try {
          // Try to parse JSON output
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          // If not JSON, return raw output
          resolve({ output: stdout });
        }
      });

      proc.on('error', (error) => {
        console.error(`[KG Integration] Error calling ${scriptName}:`, error);
        resolve({}); // Return empty result on error
      });
    });
  }
}
