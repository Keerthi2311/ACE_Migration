import { useEffect, useState } from 'react';
import {
  Tile,
  Tag,
  ProgressBar,
  Loading,
  InlineNotification,
} from '@carbon/react';
import { ChartLineData } from '@carbon/icons-react';
import apiService from '../../services/api';
import type { LiveEstimate, Questionnaire } from '../../services/types';
import './LiveEstimateWidget.scss';

interface LiveEstimateWidgetProps {
  questionnaireData: Partial<Questionnaire>;
}

export default function LiveEstimateWidget({ questionnaireData }: LiveEstimateWidgetProps) {
  const [estimate, setEstimate] = useState<LiveEstimate | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchEstimate = async () => {
      // Only fetch if we have minimal data
      const hasMinimalData =
        questionnaireData.source_environment?.total_flows &&
        questionnaireData.general_info?.team_band;

      if (!hasMinimalData) {
        return;
      }

      setLoading(true);
      try {
        const result = await apiService.calculateLiveEstimate(questionnaireData);
        setEstimate(result);
      } catch (error) {
        console.error('Error fetching live estimate:', error);
      } finally {
        setLoading(false);
      }
    };

    // Debounce the API call
    const timeoutId = setTimeout(fetchEstimate, 500);
    return () => clearTimeout(timeoutId);
  }, [questionnaireData]);

  const getConfidenceTagType = (level: string): 'green' | 'warm-gray' | 'red' | 'gray' => {
    switch (level) {
      case 'HIGH':
        return 'green';
      case 'MEDIUM':
        return 'warm-gray'; // Changed from 'yellow'
      case 'LOW':
        return 'red';
      default:
        return 'gray';
    }
  };

  return (
    <Tile className="live-estimate-widget">
      <div className="widget-header">
        <ChartLineData size={20} />
        <h4>Live Estimate</h4>
      </div>

      {loading ? (
        <div className="loading-container">
          <Loading small withOverlay={false} />
        </div>
      ) : estimate && estimate.is_complete ? (
        <>
          <div className="estimate-main">
            <div className="estimate-value">{Math.round(estimate.total_days)}</div>
            <div className="estimate-label">Days</div>
          </div>

          <div className="estimate-secondary">
            <div className="secondary-item">
              <span className="secondary-label">Weeks:</span>
              <span className="secondary-value">{estimate.total_weeks.toFixed(1)}</span>
            </div>
            <div className="secondary-item">
              <span className="secondary-label">Months:</span>
              <span className="secondary-value">{estimate.total_months.toFixed(1)}</span>
            </div>
          </div>

          <div className="confidence-section">
            <div className="confidence-header">
              <span>Confidence</span>
              <Tag type={getConfidenceTagType(estimate.confidence_level)} size="sm">
                {estimate.confidence_level}
              </Tag>
            </div>
            <ProgressBar
              label="Confidence level"
              hideLabel
              value={estimate.confidence * 100}
              max={100}
            />
            <div className="confidence-percentage">
              {(estimate.confidence * 100).toFixed(0)}%
            </div>
          </div>

          {estimate.breakdown && Object.keys(estimate.breakdown).length > 0 && (
            <div className="breakdown-section">
              <h5>Breakdown Preview</h5>
              <div className="breakdown-items">
                {Object.entries(estimate.breakdown).map(([key, value]) => (
                  <div key={key} className="breakdown-item">
                    <span className="breakdown-key">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                    </span>
                    <span className="breakdown-value">
                      {typeof value === 'number' ? Math.round(value) : value}d
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {estimate.warnings && estimate.warnings.length > 0 && (
            <div className="warnings-section">
              {estimate.warnings.map((warning, index) => (
                <InlineNotification
                  key={index}
                  kind="warning"
                  title="Note"
                  subtitle={warning}
                  hideCloseButton
                  lowContrast
                />
              ))}
            </div>
          )}

          {estimate.missing_fields && estimate.missing_fields.length > 0 && (
            <div className="missing-fields">
              <InlineNotification
                kind="info"
                title="Missing Data"
                subtitle={`Complete ${estimate.missing_fields.length} more field(s) for higher accuracy`}
                hideCloseButton
                lowContrast
              />
            </div>
          )}
        </>
      ) : (
        <div className="empty-state">
          <p>Fill out the questionnaire to see live estimate</p>
        </div>
      )}
    </Tile>
  );
}
