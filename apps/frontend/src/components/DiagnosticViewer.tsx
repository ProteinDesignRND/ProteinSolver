import React from 'react';
import type { DiagnosticResult } from '../types';
import { SequenceViewer } from './SequenceViewer';

interface DiagnosticViewerProps {
  diagnostic: DiagnosticResult;
  targetName: string;
}

export const DiagnosticViewer: React.FC<DiagnosticViewerProps> = ({ diagnostic, targetName }) => {
  return (
    <div>
      {/* Diagnostic Metric Banner */}
      <div className="glass-card" style={{ padding: '20px', marginBottom: '20px', borderColor: 'rgba(245, 158, 11, 0.4)', background: 'rgba(245, 158, 11, 0.05)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-amber)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              📊 Diagnostic Recovery Analysis
            </span>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '2px' }}>
              {diagnostic.recovery_percentage}% Native Sequence Identity ({diagnostic.matches}/{diagnostic.total_residues})
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
              {diagnostic.disclaimer}
            </p>
          </div>
          <div style={{ padding: '8px 14px', borderRadius: '8px', background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(255,255,255,0.08)', fontSize: '0.82rem', fontFamily: 'var(--font-mono)' }}>
            MAP Greedy Search: 41.30% Target Check
          </div>
        </div>

        {/* Alignment Comparison */}
        <div style={{ marginTop: '16px', background: 'rgba(0,0,0,0.4)', padding: '14px', borderRadius: '8px', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', overflowX: 'auto' }}>
          <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>Native:   {diagnostic.native_sequence}</div>
          <div style={{ color: 'var(--accent-cyan)', marginBottom: '4px' }}>Designed: {diagnostic.design.sequence}</div>
          <div style={{ color: 'var(--accent-emerald)' }}>
            Match:    {diagnostic.native_sequence.split('').map((c, i) => (c === diagnostic.design.sequence[i] ? '|' : ' ')).join('')}
          </div>
        </div>
      </div>

      <SequenceViewer result={diagnostic.design} targetName={targetName} />
    </div>
  );
};
