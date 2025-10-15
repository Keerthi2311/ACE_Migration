/**
 * Type definitions for IBM ACE Migration Estimator
 */

// Environment Configuration
export interface EnvironmentConfig {
  name: string;
  integration_nodes: number;
  integration_servers_per_node: number;
}

// MQ Details
export interface MQDetails {
  queue_managers_per_node: number;
  queue_managers_in_scope: boolean;
  topology_diagram_url?: string;
}

// Source Environment
export interface SourceEnvironment {
  product_version: string;
  host_platform: string;
  host_platform_os: string;
  platform?: string; // Added for form compatibility
  infrastructure?: string; // Added for form compatibility
  environments: EnvironmentConfig[] | string[]; // Support both formats
  has_mq: boolean;
  mq_details?: MQDetails;
  external_systems: string[];
  integration_protocols: string[];
  additional_systems?: string;
  devops_pipeline?: string;
  total_flows: number;
  has_custom_plugins: boolean;
  custom_plugin_details?: string;
  configurable_services: number;
}

// Target Environment
export interface TargetEnvironment {
  product_version: string;
  host_platform: string;
  host_platform_os: string;
  platform?: string; // Added for form compatibility
  infrastructure?: string; // Added for form compatibility
  target_env_status?: string; // Added for form compatibility
  migration_type: 'parallel' | 'in_place';
  product_installation_needed: boolean;
  infrastructure_migration: boolean;
  like_to_like_migration: boolean;
  environments: EnvironmentConfig[] | string[]; // Support both formats
  keep_custom_plugins: boolean;
  target_topology?: string;
  applications_in_scope: number;
  external_systems_in_scope: string[];
  integration_protocols: string[];
  monitoring_requirements?: string;
  database_requirements?: string;
  reporting_requirements?: string;
  logging_requirements?: string;
}

// General Information
export interface GeneralInfo {
  migration_drivers: string[];
  timeline?: Date;
  current_issues?: string;
  remote_access_available: boolean;
  internal_support_teams: boolean;
  customer_performs_testing: boolean;
  testing_approach: string[];
  ibm_assistance_needed: string[];
}

// Complete Questionnaire
export interface Questionnaire {
  source_environment: SourceEnvironment;
  target_environment: TargetEnvironment;
  general_info: GeneralInfo;
  project_name?: string;
  project_id?: string;
  created_at?: string;
  updated_at?: string;
}

// Live Estimate
export interface LiveEstimate {
  total_days: number;
  total_weeks: number;
  total_months: number;
  confidence: number;
  confidence_level: 'HIGH' | 'MEDIUM' | 'LOW';
  breakdown: Record<string, number>;
  warnings: string[];
  is_complete: boolean;
  missing_fields: string[];
}

// Risk Item
export interface RiskItem {
  item: string;
  impact_days_range: string;
  reason: string;
  recommendation: string;
  similar_cases: string[];
  confidence_impact: number;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
}

// Risk Assessment
export interface RiskAssessment {
  high_priority_risks: RiskItem[];
  medium_priority_risks: RiskItem[];
  low_priority_risks: RiskItem[];
  overall_risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  manual_review_percentage: number;
  confidence_score: number;
  total_risk_items: number;
}

// Similar Project
export interface SimilarProject {
  project_id: string;
  project_name?: string; // Added
  source_version: string;
  target_version: string;
  flow_count: number;
  infrastructure?: string; // Added
  estimated_days: number;
  actual_days: number;
  actual_duration_days?: number; // Added (alias for actual_days)
  variance_percentage: number;
  similarity_score: number;
  issues_encountered: string[];
  lessons_learned?: string;
  complexity_score: number;
}

// Phase Breakdown (Added)
export interface BreakdownPhase {
  phase: string;
  days: number;
  weeks: number;
  description: string;
}

// Risk Detail (Added)
export interface RiskDetail {
  risk_name: string;
  level: 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  mitigation?: string;
}

// Estimation Report
export interface EstimationReport {
  project_id: string;
  project_name?: string;
  generated_at: string;
  executive_summary: string;
  base_days: number;
  complexity_adjustment: number;
  total_days: number;
  total_weeks: number;
  total_months: number;
  breakdown?: BreakdownPhase[]; // Added
  risks?: RiskDetail[]; // Added
  flow_migration: any;
  environment_setup: any;
  target_setup: any;
  migration_execution: any;
  fixed_components: Record<string, number>;
  complexity: any;
  risk_assessment: RiskAssessment;
  similar_projects: SimilarProject[];
  overall_confidence: number;
  confidence_level: 'HIGH' | 'MEDIUM' | 'LOW';
  confidence_by_component: Record<string, number>;
  recommendations: string[];
  assumptions: string[];
  exclusions: string[];
  questionnaire_completeness: number;
  similar_projects_count: number;
}

// Insight Card
export interface InsightCard {
  title: string;
  message: string;
  severity: 'info' | 'warning' | 'error';
  icon?: string;
  action?: string;
  details_url?: string;
  related_projects?: string[];
}

// Text Analysis Response
export interface TextAnalysisResponse {
  entities: string[];
  technologies: string[];
  complexity_indicators: string[];
  potential_risks: string[];
  custom_code_mentioned: boolean;
  estimated_complexity: string;
  recommendations: string[];
  confidence: number;
}

// Validation Response
export interface ValidationResponse {
  is_valid: boolean;
  suggestions: string[];
  warnings: string[];
  insights?: string;
  confidence: number;
}
