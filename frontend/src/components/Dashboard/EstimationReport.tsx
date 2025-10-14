import {
  Button,
  Tile,
  Grid,
  Column,
  Tag,
  Accordion,
  AccordionItem,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListBody,
  StructuredListRow,
  StructuredListCell,
} from '@carbon/react';
import {
  DocumentDownload,
  ArrowLeft,
  CheckmarkFilled,
  WarningFilled,
  ErrorFilled,
} from '@carbon/icons-react';
import type { EstimationReport as EstimationReportType } from '../../services/types';
import './EstimationReport.scss';

interface EstimationReportProps {
  report: EstimationReportType;
  onBack: () => void;
}

export default function EstimationReport({ report, onBack }: EstimationReportProps) {
  const getRiskTagType = (level: string): 'red' | 'warm-gray' | 'green' | 'gray' => {
    switch (level) {
      case 'HIGH':
        return 'red';
      case 'MEDIUM':
        return 'warm-gray'; // Changed from 'yellow' to 'warm-gray'
      case 'LOW':
        return 'green';
      default:
        return 'gray';
    }
  };

  const getConfidenceTagType = (level: string): 'green' | 'warm-gray' | 'red' | 'gray' => {
    switch (level) {
      case 'HIGH':
        return 'green';
      case 'MEDIUM':
        return 'warm-gray'; // Changed from 'yellow' to 'warm-gray'
      case 'LOW':
        return 'red';
      default:
        return 'gray';
    }
  };

  const getRiskIcon = (level: string) => {
    switch (level) {
      case 'HIGH':
        return <ErrorFilled size={20} />;
      case 'MEDIUM':
        return <WarningFilled size={20} />;
      case 'LOW':
        return <CheckmarkFilled size={20} />;
      default:
        return null;
    }
  };

  return (
    <div className="estimation-report">
      {/* Header */}
      <div className="report-header">
        <div className="header-content">
          <h2>Migration Estimation Report</h2>
          <p className="project-name">{report.project_name || 'ACE Migration Project'}</p>
        </div>
        <div className="header-actions">
          <Button
            kind="secondary"
            renderIcon={ArrowLeft}
            onClick={onBack}
          >
            Back to Questionnaire
          </Button>
          <Button
            kind="primary"
            renderIcon={DocumentDownload}
          >
            Export Report
          </Button>
        </div>
      </div>

      {/* Executive Summary */}
      <Tile className="executive-summary">
        <h3>Executive Summary</h3>
        <Grid fullWidth narrow>
          <Column sm={4} md={2} lg={4}>
            <div className="metric-card">
              <div className="metric-value">{Math.round(report.total_days)}</div>
              <div className="metric-label">Total Days</div>
            </div>
          </Column>
          <Column sm={4} md={2} lg={4}>
            <div className="metric-card">
              <div className="metric-value">{report.total_weeks.toFixed(1)}</div>
              <div className="metric-label">Weeks</div>
            </div>
          </Column>
          <Column sm={4} md={2} lg={4}>
            <div className="metric-card">
              <div className="metric-value">{report.total_months.toFixed(1)}</div>
              <div className="metric-label">Months</div>
            </div>
          </Column>
          <Column sm={4} md={2} lg={4}>
            <div className="metric-card">
              <Tag type={getConfidenceTagType(report.confidence_level)} size="md">
                {report.confidence_level} Confidence
              </Tag>
            </div>
          </Column>
        </Grid>
      </Tile>

      {/* Phase Breakdown */}
      {report.breakdown && report.breakdown.length > 0 && (
        <Tile className="section-tile">
          <h3>Phase-wise Breakdown</h3>
          <StructuredListWrapper>
            <StructuredListHead>
              <StructuredListRow head>
                <StructuredListCell head>Phase</StructuredListCell>
                <StructuredListCell head>Days</StructuredListCell>
                <StructuredListCell head>Weeks</StructuredListCell>
                <StructuredListCell head>Description</StructuredListCell>
              </StructuredListRow>
            </StructuredListHead>
            <StructuredListBody>
              {report.breakdown.map((phase, index) => (
                <StructuredListRow key={index}>
                  <StructuredListCell>{phase.phase}</StructuredListCell>
                  <StructuredListCell>{Math.round(phase.days)}</StructuredListCell>
                  <StructuredListCell>{phase.weeks.toFixed(1)}</StructuredListCell>
                  <StructuredListCell>{phase.description}</StructuredListCell>
                </StructuredListRow>
              ))}
            </StructuredListBody>
          </StructuredListWrapper>
        </Tile>
      )}

      {/* Risk Assessment */}
      {report.risks && report.risks.length > 0 && (
        <Tile className="section-tile">
          <h3>Risk Assessment</h3>
          <div className="risks-container">
            {report.risks.map((risk, index) => (
              <div key={index} className={`risk-item risk-${getRiskTagType(risk.level)}`}>
                <div className="risk-header">
                  {getRiskIcon(risk.level)}
                  <Tag type={getRiskTagType(risk.level)} size="md">
                    {risk.level}
                  </Tag>
                  <span className="risk-name">{risk.risk_name}</span>
                </div>
                <p className="risk-description">{risk.description}</p>
                {risk.mitigation && (
                  <div className="risk-mitigation">
                    <strong>Mitigation:</strong> {risk.mitigation}
                  </div>
                )}
              </div>
            ))}
          </div>
        </Tile>
      )}

      {/* Similar Projects */}
      {report.similar_projects && report.similar_projects.length > 0 && (
        <Tile className="section-tile">
          <h3>Similar Historical Projects</h3>
          <p className="section-description">
            Based on historical data, here are similar projects that can provide insights:
          </p>
          <Accordion>
            {report.similar_projects.map((project, index) => (
              <AccordionItem
                key={index}
                title={`${project.project_name || project.project_id} (${(project.similarity_score * 100).toFixed(0)}% match)`}
              >
                <Grid fullWidth narrow>
                  <Column sm={4} md={4} lg={8}>
                    <div className="project-detail">
                      <strong>Source:</strong> {project.source_version}
                    </div>
                    <div className="project-detail">
                      <strong>Target:</strong> {project.target_version}
                    </div>
                    <div className="project-detail">
                      <strong>Flows:</strong> {project.flow_count}
                    </div>
                  </Column>
                  <Column sm={4} md={4} lg={8}>
                    {project.infrastructure && (
                      <div className="project-detail">
                        <strong>Infrastructure:</strong> {project.infrastructure}
                      </div>
                    )}
                    <div className="project-detail">
                      <strong>Actual Duration:</strong> {project.actual_duration_days || project.actual_days} days
                    </div>
                    <div className="project-detail">
                      <strong>Variance:</strong>{' '}
                      <Tag type={project.variance_percentage > 10 ? 'red' : 'green'}>
                        {project.variance_percentage > 0 ? '+' : ''}
                        {project.variance_percentage}%
                      </Tag>
                    </div>
                  </Column>
                </Grid>
                {project.lessons_learned && (
                  <div className="lessons-learned">
                    <strong>Lessons Learned:</strong>
                    <p>{project.lessons_learned}</p>
                  </div>
                )}
              </AccordionItem>
            ))}
          </Accordion>
        </Tile>
      )}

      {/* Recommendations */}
      {report.recommendations && report.recommendations.length > 0 && (
        <Tile className="section-tile">
          <h3>AI-Generated Recommendations</h3>
          <ul className="recommendations-list">
            {report.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </Tile>
      )}

      {/* Assumptions & Exclusions */}
      <Grid fullWidth narrow>
        {report.assumptions && report.assumptions.length > 0 && (
          <Column sm={4} md={4} lg={8}>
            <Tile className="section-tile">
              <h4>Assumptions</h4>
              <ul className="assumptions-list">
                {report.assumptions.map((assumption, index) => (
                  <li key={index}>{assumption}</li>
                ))}
              </ul>
            </Tile>
          </Column>
        )}
        {report.exclusions && report.exclusions.length > 0 && (
          <Column sm={4} md={4} lg={8}>
            <Tile className="section-tile">
              <h4>Exclusions</h4>
              <ul className="exclusions-list">
                {report.exclusions.map((exclusion, index) => (
                  <li key={index}>{exclusion}</li>
                ))}
              </ul>
            </Tile>
          </Column>
        )}
      </Grid>
    </div>
  );
}
