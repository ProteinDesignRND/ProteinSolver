import React, { useState, useEffect } from 'react';
import type { ExampleStructure, ChainInfo } from '../types';
import { fetchExamples, fetchExamplePDB, validateStructure } from '../api';

interface StructureInputProps {
  pdbContent: string;
  setPdbContent: (content: string) => void;
  selectedChain: string;
  setSelectedChain: (chain: string) => void;
  chains: ChainInfo[];
  setChains: (chains: ChainInfo[]) => void;
  targetName: string;
  setTargetName: (name: string) => void;
}

export const StructureInput: React.FC<StructureInputProps> = ({
  pdbContent,
  setPdbContent,
  selectedChain,
  setSelectedChain,
  chains,
  setChains,
  targetName,
  setTargetName,
}) => {
  const [examples, setExamples] = useState<ExampleStructure[]>([]);
  const [loadingExample, setLoadingExample] = useState(false);
  const [validating, setValidating] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    fetchExamples().then(setExamples).catch(console.error);
  }, []);

  const handleSelectExample = async (ex: ExampleStructure) => {
    try {
      setLoadingExample(true);
      setValidationError(null);
      const content = await fetchExamplePDB(ex.id);
      setPdbContent(content);
      setTargetName(ex.name);
      setSelectedChain(ex.chain_id);
      
      const val = await validateStructure(content);
      if (val.valid) {
        setChains(val.chains);
      } else {
        setValidationError(val.error || 'Failed to parse structure');
      }
    } catch (err: any) {
      setValidationError(err.message);
    } finally {
      setLoadingExample(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setValidationError(null);
    setTargetName(file.name);
    const reader = new FileReader();
    reader.onload = async (event) => {
      const text = event.target?.result as string;
      setPdbContent(text);
      setValidating(true);
      try {
        const val = await validateStructure(text);
        if (val.valid) {
          setChains(val.chains);
          if (val.chains.length > 0) {
            setSelectedChain(val.chains[0].chain_id);
          }
        } else {
          setValidationError(val.error || 'Invalid structure file');
        }
      } catch (err: any) {
        setValidationError(err.message);
      } finally {
        setValidating(false);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="glass-card" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>1. Protein Structure Input</h2>
            {validating && <span style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>⏳ Validating...</span>}
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Upload a PDB structure or choose a verified benchmark fixture {pdbContent ? `(${Math.round(pdbContent.length / 1024)} KB)` : ''}
          </p>
        </div>
        <label className="btn btn-secondary" style={{ fontSize: '0.85rem', padding: '6px 14px', cursor: 'pointer' }}>
          📁 Upload Custom PDB
          <input type="file" accept=".pdb,.ent,.cif" onChange={handleFileUpload} style={{ display: 'none' }} />
        </label>
      </div>

      {/* Examples Bar */}
      <div style={{ marginBottom: '18px' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'block', marginBottom: '8px' }}>
          Verified 1-Click Fixtures:
        </span>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {examples.map((ex) => (
            <button
              key={ex.id}
              onClick={() => handleSelectExample(ex)}
              disabled={loadingExample}
              style={{
                background: targetName.includes(ex.id) ? 'rgba(6, 182, 212, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                border: `1px solid ${targetName.includes(ex.id) ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
                borderRadius: '8px',
                padding: '8px 14px',
                textAlign: 'left',
                cursor: 'pointer',
                color: 'var(--text-primary)',
                transition: 'all 0.15s ease',
              }}
            >
              <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{ex.id}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Chain {ex.chain_id} ({ex.residue_count} AA)</div>
            </button>
          ))}
        </div>
      </div>

      {/* Selected Target & Chain Info */}
      {chains.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', background: 'rgba(0,0,0,0.2)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Active Target</span>
            <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>{targetName || 'Custom Upload'}</div>
          </div>
          <div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Chain Selection</span>
            <select
              value={selectedChain}
              onChange={(e) => setSelectedChain(e.target.value)}
              style={{
                width: '100%',
                padding: '6px 10px',
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                fontSize: '0.85rem',
                outline: 'none',
              }}
            >
              {chains.map((c) => (
                <option key={c.chain_id} value={c.chain_id} style={{ background: '#111827' }}>
                  Chain {c.chain_id} — {c.residue_count} residues (Res #{c.first_res_id}..#{c.last_res_id})
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      {validationError && (
        <div style={{ marginTop: '12px', padding: '10px 14px', borderRadius: '8px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fca5a5', fontSize: '0.85rem' }}>
          ⚠️ {validationError}
        </div>
      )}
    </div>
  );
};
