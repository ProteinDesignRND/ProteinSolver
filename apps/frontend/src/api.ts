import type { HealthData, ModelData, ExampleStructure, ChainInfo, DesignResult, DiagnosticResult } from './types';

const API_BASE = '/api';

export async function fetchHealth(): Promise<HealthData> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function fetchModelInfo(): Promise<ModelData> {
  const res = await fetch(`${API_BASE}/model`);
  if (!res.ok) throw new Error('Failed to fetch model info');
  return res.json();
}

export async function fetchExamples(): Promise<ExampleStructure[]> {
  const res = await fetch(`${API_BASE}/examples`);
  if (!res.ok) throw new Error('Failed to fetch example structures');
  return res.json();
}

export async function fetchExamplePDB(exampleId: string): Promise<string> {
  const res = await fetch(`${API_BASE}/examples/${exampleId}`);
  if (!res.ok) throw new Error('Failed to fetch example PDB text');
  const data = await res.json();
  return data.pdb_content;
}

export async function validateStructure(pdbContent: string): Promise<{ valid: boolean; chains: ChainInfo[]; error?: string }> {
  const res = await fetch(`${API_BASE}/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pdb_content: pdbContent }),
  });
  if (!res.ok) throw new Error('Validation failed');
  return res.json();
}

export async function runDesign(
  pdbContent: string,
  chainId: string,
  strategy: string,
  temperature?: number,
  seed?: number
): Promise<DesignResult> {
  const res = await fetch(`${API_BASE}/design`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      pdb_content: pdbContent,
      chain_id: chainId,
      strategy,
      temperature,
      seed,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Design failed' }));
    throw new Error(err.detail || 'Design failed');
  }
  return res.json();
}

export async function runDiagnostic(
  pdbContent: string,
  chainId: string,
  strategy: string,
  temperature?: number,
  seed?: number
): Promise<DiagnosticResult> {
  const res = await fetch(`${API_BASE}/diagnostic`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      pdb_content: pdbContent,
      chain_id: chainId,
      strategy,
      temperature,
      seed,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Diagnostic evaluation failed' }));
    throw new Error(err.detail || 'Diagnostic evaluation failed');
  }
  return res.json();
}
