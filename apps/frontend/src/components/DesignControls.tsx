import React from 'react';

interface DesignControlsProps {
  mode: 'DESIGN' | 'DIAGNOSTIC';
  setMode: (mode: 'DESIGN' | 'DIAGNOSTIC') => void;
  strategy: 'map' | 'multinomial';
  setStrategy: (strategy: 'map' | 'multinomial') => void;
  temperature: number;
  setTemperature: (t: number) => void;
  seed: string;
  setSeed: (s: string) => void;
  onRun: () => void;
  loading: boolean;
  disabled: boolean;
}

export const DesignControls: React.FC<DesignControlsProps> = ({
  mode,
  setMode,
  strategy,
  setStrategy,
  temperature,
  setTemperature,
  seed,
  setSeed,
  onRun,
  loading,
  disabled,
}) => {
  return (
    <div className="glass-card" style={{ padding: '24px' }}>
      <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>2. Design Configuration</h2>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>Configure inference mode and stochastic sampling hyperparameters</p>

      {/* Mode Selector */}
      <div style={{ marginBottom: '18px' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'block', marginBottom: '8px' }}>
          Execution Mode:
        </span>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
          <button
            onClick={() => setMode('DESIGN')}
            style={{
              padding: '10px 14px',
              borderRadius: '8px',
              background: mode === 'DESIGN' ? 'rgba(6, 182, 212, 0.15)' : 'rgba(255,255,255,0.03)',
              border: `1px solid ${mode === 'DESIGN' ? 'var(--accent-cyan)' : 'var(--border-subtle)'}`,
              color: mode === 'DESIGN' ? 'var(--accent-cyan)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '0.85rem',
              textAlign: 'left',
            }}
          >
            <div>✨ Inverse Folding Design</div>
            <div style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-muted)', marginTop: '2px' }}>Pure all-masked generation (0 native leakage)</div>
          </button>

          <button
            onClick={() => setMode('DIAGNOSTIC')}
            style={{
              padding: '10px 14px',
              borderRadius: '8px',
              background: mode === 'DIAGNOSTIC' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(255,255,255,0.03)',
              border: `1px solid ${mode === 'DIAGNOSTIC' ? 'var(--accent-amber)' : 'var(--border-subtle)'}`,
              color: mode === 'DIAGNOSTIC' ? 'var(--accent-amber)' : 'var(--text-secondary)',
              cursor: 'pointer',
              fontWeight: 600,
              fontSize: '0.85rem',
              textAlign: 'left',
            }}
          >
            <div>📊 Diagnostic Evaluation</div>
            <div style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-muted)', marginTop: '2px' }}>Compares against native sequence identity</div>
          </button>
        </div>
      </div>

      {/* Strategy and Parameters */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '14px', marginBottom: '20px' }}>
        <div>
          <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Sampling Strategy</label>
          <select
            value={strategy}
            onChange={(e) => setStrategy(e.target.value as any)}
            style={{ width: '100%', padding: '8px 10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-subtle)', borderRadius: '6px', color: 'var(--text-primary)', fontSize: '0.85rem', outline: 'none' }}
          >
            <option value="map" style={{ background: '#111827' }}>Argmax (Greedy MAP)</option>
            <option value="multinomial" style={{ background: '#111827' }}>Multinomial Sampling</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
            Temperature {strategy === 'map' ? '(N/A for MAP)' : `(T=${temperature})`}
          </label>
          <input
            type="number"
            step="0.05"
            min="0.01"
            max="2.0"
            disabled={strategy === 'map'}
            value={temperature}
            onChange={(e) => setTemperature(parseFloat(e.target.value))}
            style={{ width: '100%', padding: '8px 10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-subtle)', borderRadius: '6px', color: 'var(--text-primary)', fontSize: '0.85rem', outline: 'none', opacity: strategy === 'map' ? 0.5 : 1 }}
          />
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Random Seed (Optional)</label>
          <input
            type="text"
            placeholder="e.g. 42"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            style={{ width: '100%', padding: '8px 10px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-subtle)', borderRadius: '6px', color: 'var(--text-primary)', fontSize: '0.85rem', outline: 'none' }}
          />
        </div>
      </div>

      <button
        onClick={onRun}
        disabled={disabled || loading}
        className="btn btn-primary"
        style={{ width: '100%', padding: '12px', fontSize: '1rem' }}
      >
        {loading ? (
          <>
            <span style={{ display: 'inline-block', width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
            Running ProteinSolver Inference...
          </>
        ) : (
          `🚀 Run ProteinSolver ${mode === 'DESIGN' ? 'Design' : 'Diagnostic'}`
        )}
      </button>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};
