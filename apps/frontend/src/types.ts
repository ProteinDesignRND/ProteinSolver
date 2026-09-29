export interface HealthData {
  status: string;
  version: string;
  python_version: string;
  torch_version: string;
  cuda_available: boolean;
  device: string;
  model_loaded: boolean;
  parameter_count: number;
}

export interface ModelData {
  model_name: string;
  architecture: string;
  parameter_count: number;
  input_node_features: number;
  input_edge_features: number;
  hidden_size: number;
  output_size: number;
  checkpoint_sha256: string;
  checkpoint_loaded: boolean;
}

export interface ChainInfo {
  chain_id: string;
  residue_count: number;
  first_res_id: number;
  last_res_id: number;
}

export interface ExampleStructure {
  id: string;
  name: string;
  filename: string;
  chain_id: string;
  residue_count: number;
  description: string;
}

export interface DesignResult {
  sequence: string;
  length: number;
  confidences: number[];
  mean_confidence: number;
  runtime_seconds: number;
  strategy: string;
  temperature: number;
  seed?: number;
  device: string;
  mode: string;
}

export interface DiagnosticResult {
  design: DesignResult;
  native_sequence: string;
  matches: number;
  total_residues: number;
  recovery_percentage: number;
  disclaimer: string;
}
