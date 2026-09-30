import React from 'react';

interface ProvenanceModalProps {
  onClose: () => void;
}

export const ProvenanceModal: React.FC<ProvenanceModalProps> = ({ onClose }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(8px)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div className="glass-card" style={{ maxWidth: '720px', width: '100%', maxHeight: '85vh', overflowY: 'auto', padding: '32px', background: '#0f172a', border: '1px solid rgba(255,255,255,0.15)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--text-primary)' }}>Upstream Provenance & Historical Integrity</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '1.5rem', cursor: 'pointer' }}>x</button>
        </div>

        <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '16px', marginBottom: '6px' }}>1. GitHub Fork of Upstream</h3>
          <p>This repository is a GitHub fork of <code>ostrokach/proteinsolver</code>, preserving the complete original commit history from author Alexey Strokach starting from baseline commit <code>69ef0965a3fc3bf191804035b539720a06e58ba6</code>.</p>

          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '16px', marginBottom: '6px' }}>2. MIT License & Attribution</h3>
          <p>ProteinSolver is distributed under the MIT License. Published in <em>Cell Systems</em> (2020) by Strokach et al., "Fast and Flexible Protein Design Using Deep Graph Neural Networks" (DOI: 10.1016/j.cels.2020.08.016).</p>

          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '16px', marginBottom: '6px' }}>3. Compatibility Innovations (compat/)</h3>
          <ul style={{ paddingLeft: '20px', marginTop: '6px' }}>
            <li><strong>Windows POSIX fcntl stub:</strong> Allows execution on Windows systems without compilation failures.</li>
            <li><strong>Obsolete kmtools isolation:</strong> Replaced with cleanroom BioPython structure parsing.</li>
            <li><strong>PyG 2.x scatter_ shim:</strong> Transparently translates removed PyG in-place scatter operators.</li>
            <li><strong>Checkpoint key translation:</strong> Maps module list prefixes (<code>graph_conv_0</code>) to packaged layer names (<code>graph_conv_1</code>).</li>
          </ul>

          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '16px', marginBottom: '6px' }}>4. Methodology & Design Invariants</h3>
          <p>In <strong>Design Mode</strong>, all residues are initialized strictly to the mask token (20) and ground-truth sequences are completely stripped. Design-path input invariant enforced by the compatibility/application layer and protected by regression tests.</p>
        </div>

        <button onClick={onClose} className="btn btn-primary" style={{ width: '100%', marginTop: '24px' }}>
          Close Provenance Overview
        </button>
      </div>
    </div>
  );
};