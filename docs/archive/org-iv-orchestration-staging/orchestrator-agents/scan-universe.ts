/**
 * Scan Universe Utility
 * 
 * Objective: Run a full metasystem health scan from the CLI.
 */

import path from 'path';
import { fileURLToPath } from 'url';
import { MetasystemManager } from './metasystem-manager.js';

const __filename = fileURLToPath(import.meta.url);
const entryFile = process.argv[1];

if (entryFile === __filename) {
  const MANIFEST_PATH = path.resolve(process.cwd(), 'omni-dromenon-machina/[user]-metasystem.yaml');
  
  (async () => {
    console.log(`🌌 Initializing Metasystem Scan from ${MANIFEST_PATH}...`);
    const manager = new MetasystemManager(MANIFEST_PATH);
    const results = await manager.getUniverseHealth();
    
    console.log('\n📊 UNIVERSE HEALTH REPORT');
    console.log('=========================');
    results.forEach(r => {
        const icon = r.status === 'healthy' ? '✅' : r.status === 'drifted' ? '⚠️' : '❌';
        console.log(`${icon} ${r.name.padEnd(30)} | Stack: [${r.techStack.join(', ')}]`);
        if (r.status === 'drifted' && (r as any).missing_modules) {
           console.log(`   Missing: ${(r as any).missing_modules.join(', ')}`);
        }
    });
    console.log('=========================');
  })();
}

