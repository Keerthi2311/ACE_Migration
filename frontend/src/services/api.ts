/**
 * API Service for IBM ACE Migration Estimator
 */

import axios, { AxiosInstance } from 'axios';
import type {
  Questionnaire,
  LiveEstimate,
  EstimationReport,
  SimilarProject,
  RiskAssessment,
  ValidationResponse,
  TextAnalysisResponse,
  InsightCard,
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Questionnaire endpoints
  async validateQuestion(
    questionId: string,
    answer: any,
    context: Record<string, any> = {}
  ): Promise<ValidationResponse> {
    const response = await this.client.post('/api/questionnaire/validate', {
      question_id: questionId,
      answer,
      context,
    });
    return response.data;
  }

  async analyzeText(
    field: string,
    text: string,
    context: Record<string, any> = {}
  ): Promise<TextAnalysisResponse> {
    const response = await this.client.post('/api/questionnaire/analyze-text', {
      field,
      text,
      context,
    });
    return response.data;
  }

  // Estimation endpoints
  async calculateLiveEstimate(
    questionnaireData: Partial<Questionnaire>
  ): Promise<LiveEstimate> {
    const response = await this.client.post(
      '/api/estimation/live-calculate',
      questionnaireData
    );
    return response.data;
  }

  async generateReport(questionnaire: Questionnaire): Promise<EstimationReport> {
    const response = await this.client.post(
      '/api/estimation/generate-report',
      questionnaire
    );
    return response.data;
  }

  async quickEstimate(params: {
    flow_count: number;
    env_count: number;
    infrastructure: string;
    has_mq: boolean;
    source_version?: string;
    host_platform?: string;
  }): Promise<any> {
    const response = await this.client.get('/api/estimation/quick-estimate', {
      params,
    });
    return response.data;
  }

  // Insights endpoints
  async getSimilarProjects(params: {
    source_version: string;
    target_version: string;
    flow_count: number;
    infrastructure: string;
  }): Promise<SimilarProject[]> {
    const response = await this.client.get('/api/insights/similar-projects', {
      params,
    });
    return response.data;
  }

  async assessRisks(
    questionnaireData: Partial<Questionnaire>
  ): Promise<RiskAssessment> {
    const response = await this.client.post(
      '/api/insights/risk-assessment',
      questionnaireData
    );
    return response.data;
  }

  async getInsights(params: {
    flow_count: number;
    has_custom_plugins: boolean;
  }): Promise<InsightCard[]> {
    const response = await this.client.get('/api/insights/insights', { params });
    return response.data;
  }

  async getCollectionStats(): Promise<any> {
    const response = await this.client.get('/api/insights/collection-stats');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiService = new APIService();
export default apiService;
