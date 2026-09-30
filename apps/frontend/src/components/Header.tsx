import React from 'react';
import type { HealthData } from '../types';

interface HeaderProps {
  health: HealthData | null;
  onOpenProvenance: () => void;
}

export const Header: React.FC<HeaderProps> = ({ health, onOpenProvenance }) => {
  return (
    <header style={{ borderBottom: '1px solid var(--border-subtle)', background: 'rgba(10, 14, 23, 0.8)', backdropFilter: 'blur(12px)', position: 'sticky', top: 0, zIndex: 100 }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: 'linear-gradient(135deg, #06b6d4, #3b82f6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', boxShadow: '0 4px 12px rgba(6, 182, 212, 0.3)' }}>
            🧬
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h1 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em', color: 'var(--text-primary)' }}>ProteinSolver</h1>
              <span style={{ fontSize: '0.75rem', fontWeight: 600, padding: '2px 8px', borderRadius: '6px', background: 'rgba(6, 182, 212, 0.15)', color: 'var(--accent-cyan)', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                Milestone 1 Demo
              </span>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Graph Neural Network Inverse Protein Design (Cell Systems 2020)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button onClick={onOpenProvenance} className="btn btn-secondary" style={{ fontSize: '0.85rem', padding: '6px 14px' }}>
            📖 Upstream Provenance
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '6px 14px', borderRadius: '10px', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)', fontSize: '0.82rem' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: health?.model_loaded ? 'var(--accent-emerald)' : 'var(--accent-rose)', boxShadow: health?.model_loaded ? '0 0 8px var(--accent-emerald)' : '0 0 8px var(--accent-rose)' }} />
            <span style={{ color: 'var(--text-secondary)' }}>
              {health?.model_loaded ? `Model Ready (${health.parameter_count.toLocaleString()} params)` : 'Model Offline'}
            </span>
            <span style={{ color: 'var(--text-muted)' }}>|</span>
            <span style={{ color: 'var(--text-secondary)', textTransform: 'uppercase', fontSize: '0.75rem', fontWeight: 600 }}>
              {health?.device || 'CPU'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
