import { useState } from 'react';
import {
  ProgressIndicator,
  ProgressStep,
  Button,
  Stack,
  InlineNotification,
  Grid,
  Column,
} from '@carbon/react';
import { useForm, FormProvider } from 'react-hook-form';
import SourceEnvironment from './SourceEnvironment';
import TargetEnvironment from './TargetEnvironment';
import GeneralInfo from './GeneralInfo';
import LiveEstimateWidget from '../Dashboard/LiveEstimateWidget';
import type { Questionnaire, EstimationReport } from '../../services/types';
import apiService from '../../services/api';
import './QuestionnaireForm.scss';

const steps = [
  { label: 'Source Environment', description: 'Current IBM environment details' },
  { label: 'Target Environment', description: 'Target ACE environment setup' },
  { label: 'General Information', description: 'Migration approach and team details' },
];

interface QuestionnaireFormProps {
  onComplete: (report: EstimationReport) => void;
}

export default function QuestionnaireForm({ onComplete }: QuestionnaireFormProps) {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const methods = useForm<Questionnaire>({
    mode: 'onChange',
    defaultValues: {
      source_environment: {
        environments: [],
        external_systems: [],
        integration_protocols: [],
        total_flows: 0,
        has_mq: false,
        has_custom_plugins: false,
        configurable_services: 0,
      },
      target_environment: {
        environments: [],
        migration_type: 'parallel',
        product_installation_needed: true,
        infrastructure_migration: false,
        like_to_like_migration: false,
        applications_in_scope: 0,
        external_systems_in_scope: [],
        integration_protocols: [],
        keep_custom_plugins: false,
      },
      general_info: {
        migration_drivers: [],
        remote_access_available: false,
        internal_support_teams: false,
        customer_performs_testing: false,
        testing_approach: [],
        ibm_assistance_needed: [],
      },
    },
  });

  const { handleSubmit, watch } = methods;
  const formData = watch();

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const onSubmit = async (data: Questionnaire) => {
    setLoading(true);
    setError(null);

    try {
      const report = await apiService.generateReport(data);
      onComplete(report);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 0:
        return <SourceEnvironment />;
      case 1:
        return <TargetEnvironment />;
      case 2:
        return <GeneralInfo />;
      default:
        return null;
    }
  };

  const isStepValid = () => {
    // Basic validation for each step
    switch (activeStep) {
      case 0:
        return (
          formData.source_environment?.product_version &&
          formData.source_environment?.total_flows > 0 &&
          formData.source_environment?.environments?.length > 0
        );
      case 1:
        return (
          formData.target_environment?.product_version &&
          formData.target_environment?.environments?.length > 0
        );
      case 2:
        return (
          formData.general_info?.migration_drivers?.length > 0
        );
      default:
        return false;
    }
  };

  return (
    <FormProvider {...methods}>
      <div className="questionnaire-form">
        <div className="questionnaire-header">
          <h2>ACE Migration Assessment Questionnaire</h2>
          <p className="helper-text">
            Complete this questionnaire to receive an AI-powered migration estimate based on historical data and intelligent analysis
          </p>
        </div>

        {error && (
          <InlineNotification
            kind="error"
            title="Error generating report"
            subtitle={error}
            onCloseButtonClick={() => setError(null)}
            lowContrast
          />
        )}

        {/* Progress Indicator */}
        <div className="progress-section">
          <ProgressIndicator currentIndex={activeStep} spaceEqually>
            {steps.map((step, index) => (
              <ProgressStep
                key={step.label}
                label={step.label}
                description={step.description}
                complete={activeStep > index}
                current={activeStep === index}
              />
            ))}
          </ProgressIndicator>
        </div>

        <Grid fullWidth narrow>
          <Column lg={12} md={6} sm={4}>
            {/* Main Form Content */}
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="form-content">
                {getStepContent(activeStep)}
              </div>

              {/* Navigation Buttons */}
              <Stack gap={5} orientation="horizontal" className="navigation-buttons">
                <Button
                  kind="secondary"
                  disabled={activeStep === 0}
                  onClick={handleBack}
                >
                  Back
                </Button>

                <div style={{ marginLeft: 'auto' }}>
                  {activeStep === steps.length - 1 ? (
                    <Button
                      kind="primary"
                      type="submit"
                      disabled={loading || !isStepValid()}
                    >
                      {loading ? 'Generating Report...' : 'Generate Report'}
                    </Button>
                  ) : (
                    <Button
                      kind="primary"
                      onClick={handleNext}
                      disabled={!isStepValid()}
                    >
                      Next
                    </Button>
                  )}
                </div>
              </Stack>
            </form>
          </Column>

          <Column lg={4} md={2} sm={4}>
            {/* Live Estimate Widget (Sticky) */}
            <div className="sticky-widget">
              <LiveEstimateWidget questionnaireData={formData} />
            </div>
          </Column>
        </Grid>
      </div>
    </FormProvider>
  );
}
