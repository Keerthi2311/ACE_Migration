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
import './SourceEnvironment.scss';

export default function SourceEnvironment() {
  const { register, setValue, watch } = useFormContext<Questionnaire>();
  const formData = watch();

  return (
    <div className="source-environment-form">
      <h3>Source Environment Details</h3>
      <p className="form-description">
        Tell us about your current IBM Integration Bus/Message Broker environment
      </p>

      <Stack gap={6}>
        {/* Product Version */}
        <Select
          id="source-product-version"
          labelText="Current Product Version"
          {...register('source_environment.product_version')}
          defaultValue={formData.source_environment?.product_version || ''}
        >
          <SelectItem value="" text="Select product version" />
          <SelectItem value="WMB_v6" text="WebSphere Message Broker v6" />
          <SelectItem value="WMB_v7" text="WebSphere Message Broker v7" />
          <SelectItem value="WMB_v8" text="WebSphere Message Broker v8" />
          <SelectItem value="IIB_v9" text="IBM Integration Bus v9" />
          <SelectItem value="IIB_v10" text="IBM Integration Bus v10" />
          <SelectItem value="ACE_v11" text="App Connect Enterprise v11" />
          <SelectItem value="ACE_v12" text="App Connect Enterprise v12" />
        </Select>

        {/* Platform */}
        <Select
          id="source-platform"
          labelText="Current Platform"
          {...register('source_environment.platform')}
          defaultValue={formData.source_environment?.platform || ''}
        >
          <SelectItem value="" text="Select platform" />
          <SelectItem value="physical" text="Physical Server" />
          <SelectItem value="vmware" text="VMware" />
          <SelectItem value="cloud" text="Cloud (AWS/Azure/IBM Cloud)" />
          <SelectItem value="container" text="Container/Kubernetes" />
        </Select>

        {/* Total Flows */}
        <NumberInput
          id="total-flows"
          label="Total Number of Flows/Message Flows"
          helperText="Total count of message flows to be migrated"
          min={0}
          value={formData.source_environment?.total_flows || 0}
          onChange={(_e, { value }) => setValue('source_environment.total_flows', Number(value))}
        />

        {/* Configurable Services */}
        <NumberInput
          id="configurable-services"
          label="Number of Configurable Services"
          helperText="Count of configurable services used"
          min={0}
          value={formData.source_environment?.configurable_services || 0}
          onChange={(_e, { value }) => setValue('source_environment.configurable_services', Number(value))}
        />

        {/* Environments */}
        <div className="checkbox-group">
          <FormLabel>Environments (Select all that apply)</FormLabel>
          <Checkbox
            id="env-dev"
            labelText="Development (DEV)"
            {...register('source_environment.environments')}
            value="DEV"
          />
          <Checkbox
            id="env-qa"
            labelText="Quality Assurance (QA)"
            {...register('source_environment.environments')}
            value="QA"
          />
          <Checkbox
            id="env-uat"
            labelText="User Acceptance Testing (UAT)"
            {...register('source_environment.environments')}
            value="UAT"
          />
          <Checkbox
            id="env-preprod"
            labelText="Pre-Production (PreProd)"
            {...register('source_environment.environments')}
            value="PreProd"
          />
          <Checkbox
            id="env-prod"
            labelText="Production (PROD)"
            {...register('source_environment.environments')}
            value="PROD"
          />
        </div>

        {/* Infrastructure */}
        <Select
          id="source-infrastructure"
          labelText="Infrastructure Type"
          {...register('source_environment.infrastructure')}
          defaultValue={formData.source_environment?.infrastructure || ''}
        >
          <SelectItem value="" text="Select infrastructure" />
          <SelectItem value="ace_only" text="ACE Only" />
          <SelectItem value="mq" text="ACE with MQ" />
          <SelectItem value="container" text="Container-based" />
        </Select>

        {/* MQ Usage */}
        <Checkbox
          id="has-mq"
          labelText="Does the environment use IBM MQ?"
          {...register('source_environment.has_mq')}
        />

        {/* Custom Plugins */}
        <Checkbox
          id="has-custom-plugins"
          labelText="Are there custom Java plugins or nodes?"
          {...register('source_environment.has_custom_plugins')}
        />

        {/* External Systems */}
        <div className="checkbox-group">
          <FormLabel>External Systems Integration</FormLabel>
          <Checkbox
            id="ext-databases"
            labelText="Databases"
            {...register('source_environment.external_systems')}
            value="databases"
          />
          <Checkbox
            id="ext-file-systems"
            labelText="File Systems"
            {...register('source_environment.external_systems')}
            value="file_systems"
          />
          <Checkbox
            id="ext-rest-apis"
            labelText="REST APIs"
            {...register('source_environment.external_systems')}
            value="rest_apis"
          />
          <Checkbox
            id="ext-soap-services"
            labelText="SOAP Services"
            {...register('source_environment.external_systems')}
            value="soap_services"
          />
          <Checkbox
            id="ext-sap"
            labelText="SAP Systems"
            {...register('source_environment.external_systems')}
            value="sap"
          />
        </div>

        {/* Integration Protocols */}
        <div className="checkbox-group">
          <FormLabel>Integration Protocols Used</FormLabel>
          <Checkbox
            id="proto-http"
            labelText="HTTP/HTTPS"
            {...register('source_environment.integration_protocols')}
            value="http"
          />
          <Checkbox
            id="proto-mq"
            labelText="MQ"
            {...register('source_environment.integration_protocols')}
            value="mq"
          />
          <Checkbox
            id="proto-soap"
            labelText="SOAP"
            {...register('source_environment.integration_protocols')}
            value="soap"
          />
          <Checkbox
            id="proto-rest"
            labelText="REST"
            {...register('source_environment.integration_protocols')}
            value="rest"
          />
          <Checkbox
            id="proto-jms"
            labelText="JMS"
            {...register('source_environment.integration_protocols')}
            value="jms"
          />
          <Checkbox
            id="proto-file"
            labelText="File"
            {...register('source_environment.integration_protocols')}
            value="file"
          />
        </div>
      </Stack>
    </div>
  );
}
