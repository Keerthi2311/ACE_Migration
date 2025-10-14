"""
LLM Service for AI-powered text analysis and generation.

Supports both OpenAI and IBM watsonx.ai as LLM providers.
"""

import json
import re
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
import asyncio

from app.core.config import settings, PromptTemplates


class LLMService:
    """
    Service for interacting with Large Language Models.
    
    Supports:
    - OpenAI GPT models
    - IBM watsonx.ai models
    """
    
    def __init__(self):
        """Initialize LLM service based on configured provider"""
        self.provider = settings.LLM_PROVIDER
        
        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key not configured")
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        elif self.provider == "watsonx":
            if not settings.WATSONX_API_KEY:
                raise ValueError("watsonx.ai API key not configured")
            # Initialize watsonx client
            # Note: Implementation depends on watsonx SDK
            self.model = settings.WATSONX_MODEL
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def parse_free_text(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Parse free text input to extract structured information.
        
        Args:
            text: User's free text input
            context: Additional context for parsing
            
        Returns:
            Structured data extracted from text
        """
        prompt = PromptTemplates.TEXT_PARSING_PROMPT.format(user_text=text)
        
        try:
            response = await self._call_llm(prompt, temperature=0.1)
            parsed_data = self._extract_json_from_response(response)
            return parsed_data
        except Exception as e:
            # Fallback to basic parsing
            return {
                "entities": [],
                "technologies": [],
                "complexity_indicators": [],
                "potential_risks": [],
                "custom_code_mentioned": False,
                "estimated_complexity": "medium",
                "error": str(e)
            }
    
    async def assess_risks(
        self,
        project_context: Dict[str, Any],
        similar_projects: List[Dict[str, Any]],
        documentation: str = ""
    ) -> Dict[str, Any]:
        """
        Assess project risks using AI analysis.
        
        Args:
            project_context: Current project information
            similar_projects: List of similar historical projects
            documentation: Relevant documentation snippets
            
        Returns:
            Risk assessment with categorized risks
        """
        prompt = PromptTemplates.RISK_ASSESSMENT_PROMPT.format(
            source_version=project_context.get("source_version", "Unknown"),
            target_version=project_context.get("target_version", "Unknown"),
            flow_count=project_context.get("flow_count", 0),
            custom_components=project_context.get("custom_components", "None"),
            infrastructure=project_context.get("infrastructure", "Unknown"),
            retrieved_similar_projects=json.dumps(similar_projects, indent=2),
            retrieved_documentation=documentation
        )
        
        try:
            response = await self._call_llm(prompt, temperature=0.2)
            risk_data = self._extract_json_from_response(response)
            return risk_data
        except Exception as e:
            # Fallback risk assessment
            return {
                "high_priority_risks": [],
                "medium_priority_risks": [],
                "overall_risk_level": "MEDIUM",
                "manual_review_percentage": 20,
                "confidence_score": 0.7,
                "error": str(e)
            }
    
    async def adjust_estimate(
        self,
        base_estimate: Dict[str, Any],
        variance_data: List[Dict[str, Any]],
        project_profile: Dict[str, Any],
        risks: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use AI to adjust base estimate based on historical data.
        
        Args:
            base_estimate: Base calculation from rules engine
            variance_data: Historical variance data
            project_profile: Current project characteristics
            risks: Identified risks
            
        Returns:
            Adjusted estimate with reasoning
        """
        prompt = PromptTemplates.ESTIMATE_ADJUSTMENT_PROMPT.format(
            base_estimate=json.dumps(base_estimate, indent=2),
            variance_data=json.dumps(variance_data, indent=2),
            project_profile=json.dumps(project_profile, indent=2),
            risks=json.dumps(risks, indent=2)
        )
        
        try:
            response = await self._call_llm(prompt, temperature=0.15)
            adjustment = self._extract_json_from_response(response)
            
            # Validate adjustment is within ±20%
            base_days = base_estimate.get("total_days", 0)
            final_days = adjustment.get("final_days", base_days)
            max_adjustment = base_days * settings.MAX_ESTIMATE_ADJUSTMENT
            
            if abs(final_days - base_days) > max_adjustment:
                # Cap the adjustment
                if final_days > base_days:
                    adjustment["final_days"] = base_days + max_adjustment
                else:
                    adjustment["final_days"] = base_days - max_adjustment
                adjustment["adjustment_capped"] = True
            
            return adjustment
        except Exception as e:
            # No adjustment
            return {
                "final_days": base_estimate.get("total_days", 0),
                "adjustment_from_base": 0,
                "adjustment_reason": "Unable to calculate adjustment",
                "confidence_level": 0.7,
                "breakdown": base_estimate,
                "similar_projects_referenced": [],
                "error": str(e)
            }
    
    async def generate_report_content(
        self,
        questionnaire: Dict[str, Any],
        estimation_results: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        similar_projects: List[Dict[str, Any]]
    ) -> str:
        """
        Generate comprehensive estimation report in markdown.
        
        Args:
            questionnaire: Complete questionnaire data
            estimation_results: Calculation results
            risk_assessment: Risk assessment data
            similar_projects: Similar historical projects
            
        Returns:
            Markdown formatted report
        """
        prompt = PromptTemplates.REPORT_GENERATION_PROMPT.format(
            complete_questionnaire=json.dumps(questionnaire, indent=2),
            estimation_results=json.dumps(estimation_results, indent=2),
            risk_assessment=json.dumps(risk_assessment, indent=2),
            similar_projects=json.dumps(similar_projects, indent=2)
        )
        
        try:
            response = await self._call_llm(prompt, temperature=0.3, max_tokens=3000)
            return response
        except Exception as e:
            return f"# Estimation Report\n\nError generating report: {str(e)}"
    
    async def _call_llm(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 2000
    ) -> str:
        """
        Call the configured LLM provider.
        
        Args:
            prompt: Prompt to send to LLM
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            
        Returns:
            LLM response text
        """
        if self.provider == "openai":
            return await self._call_openai(prompt, temperature, max_tokens)
        elif self.provider == "watsonx":
            return await self._call_watsonx(prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def _call_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call OpenAI API"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert IBM ACE migration consultant with deep knowledge of WMB, IIB, and ACE migrations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _call_watsonx(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Call IBM watsonx.ai API
        
        Note: Implementation depends on watsonx SDK
        """
        # Placeholder for watsonx implementation
        # from ibm_watson_machine_learning.foundation_models import Model
        # model = Model(...)
        # response = model.generate(prompt, parameters={...})
        
        raise NotImplementedError("watsonx.ai integration not yet implemented")
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response.
        
        Handles cases where LLM includes extra text around JSON.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed JSON data
        """
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try parsing the entire response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Return empty structure if parsing fails
            return {}


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
