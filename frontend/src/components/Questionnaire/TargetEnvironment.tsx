import { useFormContext } from 'react-hook-form';
import {
  Select,
  SelectItem,
  Checkbox,
  NumberInput,
  FormLabel,
  Stack,
} from '@carbon/react';
import type { Questionnaire } from '../../services/types';
import './TargetEnvironment.scss';

export default function TargetEnvironment() {
  const { register, setValue, watch } = useFormContext<Questionnaire>();
  const formData = watch();

  return (
    <div className="target-environment-form">
      <h3>Target Environment Details</h3>
      <p className="form-description">
        Define your target IBM App Connect Enterprise environment
      </p>

      <Stack gap={6}>
        {/* Target Product Version */}
        <Select
          id="target-product-version"
          labelText="Target ACE Version"
          {...register('target_environment.product_version')}
          defaultValue={formData.target_environment?.product_version || ''}
        >
          <SelectItem value="" text="Select target version" />
          <SelectItem value="ACE_v11" text="App Connect Enterprise v11" />
          <SelectItem value="ACE_v12" text="App Connect Enterprise v12" />
        </Select>

        {/* Target Platform */}
        <Select
          id="target-platform"
          labelText="Target Platform"
          {...register('target_environment.platform')}
          defaultValue={formData.target_environment?.platform || ''}
        >
          <SelectItem value="" text="Select platform" />
          <SelectItem value="on_premise" text="On-Premise" />
          <SelectItem value="cloud" text="Cloud (AWS/Azure/IBM Cloud)" />
          <SelectItem value="container" text="Container/Kubernetes" />
        </Select>

        {/* Migration Type */}
        <Select
          id="migration-type"
          labelText="Migration Type"
          {...register('target_environment.migration_type')}
          defaultValue={formData.target_environment?.migration_type || 'parallel'}
        >
          <SelectItem value="parallel" text="Parallel (Old and new run simultaneously)" />
          <SelectItem value="cutover" text="Big Bang Cutover (Direct switch)" />
          <SelectItem value="phased" text="Phased Migration (Gradual transition)" />
        </Select>

        {/* Target Environment Status */}
        <Select
          id="target-env-status"
          labelText="Target Environment Status"
          {...register('target_environment.target_env_status')}
          defaultValue={formData.target_environment?.target_env_status || ''}
        >
          <SelectItem value="" text="Select status" />
          <SelectItem value="new" text="New Setup Required" />
          <SelectItem value="configured" text="Already Configured" />
          <SelectItem value="partial" text="Partially Configured" />
        </Select>

        {/* Applications in Scope */}
        <NumberInput
          id="applications-in-scope"
          label="Number of Applications in Scope"
          helperText="Total applications to be migrated"
          min={0}
          value={formData.target_environment?.applications_in_scope || 0}
          onChange={(_e, { value }) => setValue('target_environment.applications_in_scope', Number(value))}
        />

        {/* Target Environments */}
        <div className="checkbox-group">
          <FormLabel>Target Environments (Select all that apply)</FormLabel>
          <Checkbox
            id="target-env-dev"
            labelText="Development (DEV)"
            {...register('target_environment.environments')}
            value="DEV"
          />
          <Checkbox
            id="target-env-qa"
            labelText="Quality Assurance (QA)"
            {...register('target_environment.environments')}
            value="QA"
          />
          <Checkbox
            id="target-env-uat"
            labelText="User Acceptance Testing (UAT)"
            {...register('target_environment.environments')}
            value="UAT"
          />
          <Checkbox
            id="target-env-preprod"
            labelText="Pre-Production (PreProd)"
            {...register('target_environment.environments')}
            value="PreProd"
          />
          <Checkbox
            id="target-env-prod"
            labelText="Production (PROD)"
            {...register('target_environment.environments')}
            value="PROD"
          />
        </div>

        {/* Infrastructure */}
        <Select
          id="target-infrastructure"
          labelText="Target Infrastructure Type"
          {...register('target_environment.infrastructure')}
          defaultValue={formData.target_environment?.infrastructure || ''}
        >
          <SelectItem value="" text="Select infrastructure" />
          <SelectItem value="ace_only" text="ACE Only" />
          <SelectItem value="mq" text="ACE with MQ" />
          <SelectItem value="container" text="Container-based" />
        </Select>

        {/* Product Installation Needed */}
        <Checkbox
          id="product-installation-needed"
          labelText="Is product installation needed?"
          {...register('target_environment.product_installation_needed')}
        />

        {/* Infrastructure Migration */}
        <Checkbox
          id="infrastructure-migration"
          labelText="Is infrastructure migration involved? (e.g., VM to Container)"
          {...register('target_environment.infrastructure_migration')}
        />

        {/* Like-to-Like Migration */}
        <Checkbox
          id="like-to-like"
          labelText="Is this a like-to-like migration?"
          {...register('target_environment.like_to_like_migration')}
        />

        {/* Keep Custom Plugins */}
        <Checkbox
          id="keep-custom-plugins"
          labelText="Keep existing custom plugins?"
          {...register('target_environment.keep_custom_plugins')}
        />

        {/* External Systems */}
        <div className="checkbox-group">
          <FormLabel>External Systems in Scope</FormLabel>
          <Checkbox
            id="target-ext-databases"
            labelText="Databases"
            {...register('target_environment.external_systems_in_scope')}
            value="databases"
          />
          <Checkbox
            id="target-ext-file-systems"
            labelText="File Systems"
            {...register('target_environment.external_systems_in_scope')}
            value="file_systems"
          />
          <Checkbox
            id="target-ext-rest-apis"
            labelText="REST APIs"
            {...register('target_environment.external_systems_in_scope')}
            value="rest_apis"
          />
          <Checkbox
            id="target-ext-soap-services"
            labelText="SOAP Services"
            {...register('target_environment.external_systems_in_scope')}
            value="soap_services"
          />
          <Checkbox
            id="target-ext-sap"
            labelText="SAP Systems"
            {...register('target_environment.external_systems_in_scope')}
            value="sap"
          />
        </div>

        {/* Integration Protocols */}
        <div className="checkbox-group">
          <FormLabel>Integration Protocols Required</FormLabel>
          <Checkbox
            id="target-proto-http"
            labelText="HTTP/HTTPS"
            {...register('target_environment.integration_protocols')}
            value="http"
          />
          <Checkbox
            id="target-proto-mq"
            labelText="MQ"
            {...register('target_environment.integration_protocols')}
            value="mq"
          />
          <Checkbox
            id="target-proto-soap"
            labelText="SOAP"
            {...register('target_environment.integration_protocols')}
            value="soap"
          />
          <Checkbox
            id="target-proto-rest"
            labelText="REST"
            {...register('target_environment.integration_protocols')}
            value="rest"
          />
          <Checkbox
            id="target-proto-jms"
            labelText="JMS"
            {...register('target_environment.integration_protocols')}
            value="jms"
          />
          <Checkbox
            id="target-proto-file"
            labelText="File"
            {...register('target_environment.integration_protocols')}
            value="file"
          />
        </div>
      </Stack>
    </div>
  );
}
