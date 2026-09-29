import React, { useState, useEffect } from 'react';
import type { HealthData, ChainInfo, DesignResult, DiagnosticResult } from './types';
import { fetchHealth, runDesign, runDiagnostic } from './api';
import { Header } from './components/Header';
import { StructureInput } from './components/StructureInput';
import { DesignControls } from './components/DesignControls';
import { SequenceViewer } from './components/SequenceViewer';
import { DiagnosticViewer } from './components/DiagnosticViewer';
import { ProvenanceModal } from './components/ProvenanceModal';

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [pdbContent, setPdbContent] = useState<string>('');
  const [targetName, setTargetName] = useState<string>('');
  const [chains, setChains] = useState<ChainInfo[]>([]);
  const [selectedChain, setSelectedChain] = useState<string>('A');

  const [mode, setMode] = useState<'DESIGN' | 'DIAGNOSTIC'>('DESIGN');
  const [strategy, setStrategy] = useState<'map' | 'multinomial'>('map');
  const [temperature, setTemperature] = useState<number>(1.0);
  const [seed, setSeed] = useState<string>('42');

  const [loading, setLoading] = useState(false);
  const [designResult, setDesignResult] = useState<DesignResult | null>(null);
  const [diagnosticResult, setDiagnosticResult] = useState<DiagnosticResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showProvenance, setShowProvenance] = useState(false);

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch((err) => console.error('Health check failed', err));
  }, []);

  const handleRun = async () => {
    if (!pdbContent) return;
    setError(null);
    setLoading(true);

    try {
      const parsedSeed = seed.trim() ? parseInt(seed.trim(), 10) : undefined;
      const parsedTemp = strategy === 'multinomial' ? temperature : 1.0;

      if (mode === 'DESIGN') {
        const res = await runDesign(pdbContent, selectedChain, strategy, parsedTemp, parsedSeed);
        setDesignResult(res);
        setDiagnosticResult(null);
      } else {
        const diag = await runDiagnostic(pdbContent, selectedChain, strategy, parsedTemp, parsedSeed);
        setDiagnosticResult(diag);
        setDesignResult(diag.design);
      }
    } catch (err: any) {
      setError(err.message || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header health={health} onOpenProvenance={() => setShowProvenance(true)} />

      <main style={{ maxWidth: '1280px', width: '100%', margin: '0 auto', padding: '32px 24px', flex: 1 }}>
        {/* Hero Section */}
        <div style={{ marginBottom: '28px', textAlign: 'center' }}>
          <h2 style={{ fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.03em', color: 'var(--text-primary)', marginBottom: '8px' }}>
            Inverse Protein Sequence Design
          </h2>
          <p style={{ fontSize: '1rem', color: 'var(--text-secondary)', maxWidth: '680px', margin: '0 auto' }}>
            Run Alexey Strokach's 4-block EdgeConv Graph Neural Network on modern PyTorch 2.6.
            Predict amino acid sequences for novel protein structures using constraint satisfaction.
          </p>
        </div>

        {error && (
          <div style={{ marginBottom: '20px', padding: '14px 18px', borderRadius: '10px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fca5a5', fontSize: '0.9rem' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '32px' }}>
          <StructureInput
            pdbContent={pdbContent}
            setPdbContent={setPdbContent}
            selectedChain={selectedChain}
            setSelectedChain={setSelectedChain}
            chains={chains}
            setChains={setChains}
            targetName={targetName}
            setTargetName={setTargetName}
          />

          <DesignControls
            mode={mode}
            setMode={setMode}
            strategy={strategy}
            setStrategy={setStrategy}
            temperature={temperature}
            setTemperature={setTemperature}
            seed={seed}
            setSeed={setSeed}
            onRun={handleRun}
            loading={loading}
            disabled={!pdbContent || chains.length === 0}
          />
        </div>

        {/* Results Section */}
        {diagnosticResult ? (
          <DiagnosticViewer diagnostic={diagnosticResult} targetName={targetName} />
        ) : designResult ? (
          <SequenceViewer result={designResult} targetName={targetName} />
        ) : null}
      </main>

      <footer style={{ borderTop: '1px solid var(--border-subtle)', padding: '20px 24px', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
        ProteinDesignRND — ProteinSolver Milestone 1 Reproduction Suite
      </footer>

      {showProvenance && <ProvenanceModal onClose={() => setShowProvenance(false)} />}
    </div>
  );
};

export default App;
