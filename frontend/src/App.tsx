import { useState } from 'react';
import {
  Content,
  Header,
  HeaderName,
  HeaderGlobalBar,
  HeaderGlobalAction,
  Grid,
  Column,
  Theme,
} from '@carbon/react';
import { Information } from '@carbon/icons-react';
import QuestionnaireForm from './components/Questionnaire/QuestionnaireForm';
import EstimationReport from './components/Dashboard/EstimationReport';
import type { EstimationReport as EstimationReportType } from './services/types';
import './App.scss';

function App() {
  const [currentStep, setCurrentStep] = useState<'questionnaire' | 'report'>('questionnaire');
  const [estimationReport, setEstimationReport] = useState<EstimationReportType | null>(null);

  const handleQuestionnaireComplete = (report: EstimationReportType) => {
    setEstimationReport(report);
    setCurrentStep('report');
  };

  const handleBackToQuestionnaire = () => {
    setCurrentStep('questionnaire');
  };

  return (
    <Theme theme="g10">
      <div className="app-container">
        {/* Carbon Header */}
        <Header aria-label="IBM ACE Migration Estimator">
          <HeaderName prefix="IBM">
            ACE Migration Estimator
          </HeaderName>
          <HeaderGlobalBar>
            <HeaderGlobalAction 
              aria-label="About"
              tooltipAlignment="end"
            >
              <Information size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
        </Header>

        {/* Main Content */}
        <Content>
          <Grid fullWidth>
            <Column lg={16} md={8} sm={4}>
              <div className="content-wrapper">
                {currentStep === 'questionnaire' ? (
                  <QuestionnaireForm onComplete={handleQuestionnaireComplete} />
                ) : (
                  <EstimationReport
                    report={estimationReport!}
                    onBack={handleBackToQuestionnaire}
                  />
                )}
              </div>
            </Column>
          </Grid>
        </Content>

        {/* Footer */}
        <footer className="app-footer">
          <Grid fullWidth>
            <Column lg={16} md={8} sm={4}>
              <p className="footer-text">
                © 2025 IBM Corporation. All rights reserved. | Powered by AI & RAG
              </p>
            </Column>
          </Grid>
        </footer>
      </div>
    </Theme>
  );
}

export default App;
