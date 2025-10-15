import { useFormContext } from 'react-hook-form';
import {
  Checkbox,
  FormLabel,
  Stack,
} from '@carbon/react';
import type { Questionnaire } from '../../services/types';
import './GeneralInfo.scss';

export default function GeneralInfo() {
  const { register } = useFormContext<Questionnaire>();

  return (
    <div className="general-info-form">
      <h3>General Information</h3>
      <p className="form-description">
        Tell us about your migration approach and requirements
      </p>

      <Stack gap={6}>
        {/* Migration Drivers */}
        <div className="checkbox-group">
          <FormLabel>Migration Drivers (Select all that apply)</FormLabel>
          <Checkbox
            id="driver-version-upgrade"
            labelText="Version Upgrade"
            {...register('general_info.migration_drivers')}
            value="version_upgrade"
          />
          <Checkbox
            id="driver-containerization"
            labelText="Containerization/Modernization"
            {...register('general_info.migration_drivers')}
            value="containerization"
          />
          <Checkbox
            id="driver-cloud-migration"
            labelText="Cloud Migration"
            {...register('general_info.migration_drivers')}
            value="cloud_migration"
          />
          <Checkbox
            id="driver-cost-optimization"
            labelText="Cost Optimization"
            {...register('general_info.migration_drivers')}
            value="cost_optimization"
          />
          <Checkbox
            id="driver-eol"
            labelText="End of Life (EOL) Support"
            {...register('general_info.migration_drivers')}
            value="eol_support"
          />
          <Checkbox
            id="driver-performance"
            labelText="Performance Improvement"
            {...register('general_info.migration_drivers')}
            value="performance"
          />
        </div>

        {/* Testing Approach */}
        <div className="checkbox-group">
          <FormLabel>Testing Approach (Select all that apply)</FormLabel>
          <Checkbox
            id="test-unit"
            labelText="Unit Testing"
            {...register('general_info.testing_approach')}
            value="unit_testing"
          />
          <Checkbox
            id="test-integration"
            labelText="Integration Testing"
            {...register('general_info.testing_approach')}
            value="integration_testing"
          />
          <Checkbox
            id="test-system"
            labelText="System Testing"
            {...register('general_info.testing_approach')}
            value="system_testing"
          />
          <Checkbox
            id="test-uat"
            labelText="UAT (User Acceptance Testing)"
            {...register('general_info.testing_approach')}
            value="uat"
          />
          <Checkbox
            id="test-performance"
            labelText="Performance Testing"
            {...register('general_info.testing_approach')}
            value="performance_testing"
          />
          <Checkbox
            id="test-automated"
            labelText="Automated Testing"
            {...register('general_info.testing_approach')}
            value="automated_testing"
          />
        </div>

        {/* IBM Assistance Needed */}
        <div className="checkbox-group">
          <FormLabel>IBM Assistance Needed For (Select all that apply)</FormLabel>
          <Checkbox
            id="assist-architecture"
            labelText="Architecture Design"
            {...register('general_info.ibm_assistance_needed')}
            value="architecture_design"
          />
          <Checkbox
            id="assist-migration"
            labelText="Migration Execution"
            {...register('general_info.ibm_assistance_needed')}
            value="migration_execution"
          />
          <Checkbox
            id="assist-testing"
            labelText="Testing Support"
            {...register('general_info.ibm_assistance_needed')}
            value="testing_support"
          />
          <Checkbox
            id="assist-training"
            labelText="Training & Knowledge Transfer"
            {...register('general_info.ibm_assistance_needed')}
            value="training"
          />
          <Checkbox
            id="assist-go-live"
            labelText="Go-Live Support"
            {...register('general_info.ibm_assistance_needed')}
            value="go_live_support"
          />
          <Checkbox
            id="assist-none"
            labelText="No IBM Assistance Needed"
            {...register('general_info.ibm_assistance_needed')}
            value="none"
          />
        </div>

        {/* Additional Options */}
        <div className="checkbox-group">
          <FormLabel>Additional Information</FormLabel>
          <Checkbox
            id="remote-access"
            labelText="Is remote access to systems available?"
            {...register('general_info.remote_access_available')}
          />
          <Checkbox
            id="internal-support"
            labelText="Are internal support teams available?"
            {...register('general_info.internal_support_teams')}
          />
          <Checkbox
            id="customer-testing"
            labelText="Will customer perform testing?"
            {...register('general_info.customer_performs_testing')}
          />
        </div>
      </Stack>
    </div>
  );
}
