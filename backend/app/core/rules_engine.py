"""
IBM ACE Migration Estimation Rules Engine

This module implements the exact calculation rules for estimating
IBM ACE migration time from WMB/IIB to ACE.

All formulas are based on validated business rules and must be
implemented exactly as specified.

CRITICAL: Team band has been REMOVED from all calculations.
Estimation is based purely on flow count, environment configuration,
infrastructure complexity, and project-specific factors.
"""

from typing import Dict, List, Optional
from enum import Enum


class Infrastructure(str, Enum):
    """Infrastructure type for target environment"""
    CONTAINER = "container"
    ON_PREMISE = "on_premise"
    CLOUD = "cloud"


class SetupStatus(str, Enum):
    """Target environment setup status"""
    NEW = "new"
    CONFIGURED = "configured"


class RulesEngine:
    """
    Core rules engine for IBM ACE migration estimation.
    
    Implements exact business rules for:
    - Flow migration time calculation
    - Environment setup time
    - Target configuration time
    - Migration execution time
    - Fixed component times
    """
    
    # Fixed component times (in days)
    FIXED_COMPONENTS = {
        "uat_support": 10,      # 2 weeks
        "golive_support": 5,     # 1 week
        "knowledge_transfer": 5  # 1 week
    }
    
    @staticmethod
    def calculate_migration_execution_time(flow_count: int) -> Dict[str, float]:
        """
        Calculate migration execution time (migration + testing).
        
        Universal rate: 5 flows per 2 days
        NO team band adjustment
        
        Day 1: Deploy 5 flows, initial testing
        Day 2: Integration testing, fix issues, documentation
        
        Args:
            flow_count: Total number of flows
            
        Returns:
            Dictionary with execution time and breakdown
        """
        # Universal rate: 5 flows per 2 days = 0.4 days per flow
        time = (flow_count / 5.0) * 2.0
        
        return {
            "total": round(time, 2),
            "flows": flow_count,
            "flows_per_batch": 5,
            "days_per_batch": 2,
            "rate_description": "Universal rate: 5 flows per 2 days"
        }
    
    @staticmethod
    def calculate_environment_setup_time(
        env_count: int,
        infrastructure: str,
        has_mq: bool
    ) -> Dict[str, float]:
        """
        Calculate environment setup time.
        
        Rules:
        - Container-based: 3 days per environment
        - With MQ: 1.5 days per environment
        - ACE only: 1 day per environment
        
        Args:
            env_count: Number of environments to set up
            infrastructure: Infrastructure type (container, on_premise, cloud, etc.)
            has_mq: Whether MQ is required
            
        Returns:
            Dictionary with time_per_env and total
        """
        # Determine time per environment
        if infrastructure == Infrastructure.CONTAINER:
            time_per_env = 3
        elif has_mq:
            time_per_env = 1.5
        else:
            time_per_env = 1
        
        total = env_count * time_per_env
        
        return {
            "time_per_env": time_per_env,
            "env_count": env_count,
            "total": round(total, 2),
            "infrastructure": infrastructure,
            "has_mq": has_mq
        }
    
    @staticmethod
    def calculate_target_setup_time(setup_status: str) -> Dict[str, float]:
        """
        Calculate target configuration time.
        
        Rules:
        - New setup: 5 days
        - Already configured: 2.5 days
        
        Args:
            setup_status: Whether target is new or already configured
            
        Returns:
            Dictionary with setup time
        """
        if setup_status == SetupStatus.NEW:
            time = 5
        else:
            time = 2.5
        
        return {
            "total": time,
            "setup_status": setup_status
        }
    
    @staticmethod
    def calculate_migration_execution_time(flow_count: int) -> Dict[str, float]:
        """
        Calculate migration execution time (migration + testing).
        
        Universal rate: 5 flows per 2 days
        NO team band adjustment
        
        Day 1: Deploy 5 flows, initial testing
        Day 2: Integration testing, fix issues, documentation
        
        Args:
            flow_count: Total number of flows
            
        Returns:
            Dictionary with execution time and breakdown
        """
        # Universal rate: 5 flows per 2 days = 0.4 days per flow
        time = (flow_count / 5.0) * 2.0
        
        return {
            "total": round(time, 2),
            "flows": flow_count,
            "flows_per_batch": 5,
            "days_per_batch": 2,
            "rate_description": "Universal rate: 5 flows per 2 days"
        }
    
    @staticmethod
    def calculate_buffer(
        flow_count: int,
        has_custom_plugins: bool = False,
        legacy_source: bool = False,
        mainframe_source: bool = False,
        many_external_systems: bool = False
    ) -> Dict[str, float]:
        """
        Calculate project buffer based on size and complexity.
        NO team band consideration.
        
        Base buffer scales with project size:
        - < 50 flows: 5 days
        - < 150 flows: 6 days
        - < 300 flows: 7 days
        - >= 300 flows: 8 days
        
        Complexity multiplier (1.0 to 1.5):
        - Custom plugins: +0.1
        - Legacy source (WMB v6/v7): +0.15
        - Mainframe: +0.2
        - Many external systems (>5): +0.1
        
        Args:
            flow_count: Total number of flows
            has_custom_plugins: Whether custom plugins exist
            legacy_source: Whether source is WMB v6/v7
            mainframe_source: Whether source is mainframe
            many_external_systems: Whether >5 external systems
            
        Returns:
            Dictionary with buffer calculation
        """
        # Base buffer by project size
        if flow_count < 50:
            base_buffer = 5
        elif flow_count < 150:
            base_buffer = 6
        elif flow_count < 300:
            base_buffer = 7
        else:
            base_buffer = 8
        
        # Complexity multiplier
        complexity_multiplier = 1.0
        complexity_factors = []
        
        if has_custom_plugins:
            complexity_multiplier += 0.1
            complexity_factors.append("Custom plugins: +10%")
        
        if legacy_source:
            complexity_multiplier += 0.15
            complexity_factors.append("Legacy source (WMB v6/v7): +15%")
        
        if mainframe_source:
            complexity_multiplier += 0.2
            complexity_factors.append("Mainframe source: +20%")
        
        if many_external_systems:
            complexity_multiplier += 0.1
            complexity_factors.append("Many external systems (>5): +10%")
        
        # Cap at 1.5x
        complexity_multiplier = min(complexity_multiplier, 1.5)
        
        total_buffer = base_buffer * complexity_multiplier
        
        return {
            "base_buffer": base_buffer,
            "complexity_multiplier": round(complexity_multiplier, 2),
            "total": round(total_buffer, 2),
            "complexity_factors": complexity_factors
        }
    
    @staticmethod
    def get_fixed_components() -> Dict[str, float]:
        """
        Get fixed component times.
        NO team band factor.
        
        UAT Support: 10 days (2 weeks)
        Go-live Support: 5 days (1 week)
        Knowledge Transfer: 5 days (1 week)
        Total: 20 days
        
        Returns:
            Dictionary with UAT support, go-live support, and KT times
        """
        return RulesEngine.FIXED_COMPONENTS.copy()
    
    @staticmethod
    def calculate_complexity_multiplier(
        has_custom_plugins: bool,
        custom_plugin_count: int = 0,
        integration_protocol_count: int = 0,
        external_system_count: int = 0
    ) -> Dict[str, float]:
        """
        Calculate complexity multiplier for additional factors.
        NO team band consideration.
        
        Args:
            has_custom_plugins: Whether custom plugins exist
            custom_plugin_count: Number of custom plugins
            integration_protocol_count: Number of different protocols
            external_system_count: Number of external systems
            
        Returns:
            Dictionary with complexity analysis and multiplier
        """
        multiplier = 1.0
        factors = []
        
        if has_custom_plugins:
            plugin_factor = min(custom_plugin_count * 0.05, 0.3)  # Max 30%
            multiplier += plugin_factor
            factors.append(f"Custom plugins: +{plugin_factor*100:.0f}%")
        
        if integration_protocol_count > 3:
            protocol_factor = (integration_protocol_count - 3) * 0.03  # 3% per additional protocol
            multiplier += protocol_factor
            factors.append(f"Multiple protocols: +{protocol_factor*100:.0f}%")
        
        if external_system_count > 5:
            system_factor = (external_system_count - 5) * 0.02  # 2% per additional system
            multiplier += system_factor
            factors.append(f"Multiple systems: +{system_factor*100:.0f}%")
        
        return {
            "multiplier": round(multiplier, 3),
            "factors": factors,
            "base": 1.0,
            "additional": round(multiplier - 1.0, 3)
        }
    
    @staticmethod
    def calculate_total_estimate(
        flow_count: int,
        env_count: int,
        infrastructure: str,
        has_mq: bool,
        setup_status: str,
        source_version: str = "",
        host_platform: str = "",
        has_custom_plugins: bool = False,
        custom_plugin_count: int = 0,
        integration_protocol_count: int = 0,
        external_system_count: int = 0
    ) -> Dict:
        """
        Master calculation combining all rules.
        
        NO TEAM BAND IN CALCULATION
        
        Total = Environment Setup + Target Config + Migration Execution + Buffer + Fixed(20)
        
        Args:
            flow_count: Total number of flows
            env_count: Number of environments
            infrastructure: Infrastructure type
            has_mq: Whether MQ is required
            setup_status: Target setup status
            source_version: Source product version (for legacy detection)
            host_platform: Source host platform (for mainframe detection)
            has_custom_plugins: Whether custom plugins exist
            custom_plugin_count: Number of custom plugins
            integration_protocol_count: Number of integration protocols
            external_system_count: Number of external systems
            
        Returns:
            Complete estimation breakdown with all components
        """
        # Calculate each component
        env_setup = RulesEngine.calculate_environment_setup_time(
            env_count, infrastructure, has_mq
        )
        
        target_setup = RulesEngine.calculate_target_setup_time(setup_status)
        
        migration_execution = RulesEngine.calculate_migration_execution_time(
            flow_count
        )
        
        # Detect complexity factors
        legacy_source = source_version in ['WMB_v6', 'WMB_v7']
        mainframe_source = host_platform == 'mainframe'
        many_external_systems = external_system_count > 5
        
        buffer = RulesEngine.calculate_buffer(
            flow_count,
            has_custom_plugins,
            legacy_source,
            mainframe_source,
            many_external_systems
        )
        
        fixed_components = RulesEngine.get_fixed_components()
        
        complexity = RulesEngine.calculate_complexity_multiplier(
            has_custom_plugins,
            custom_plugin_count,
            integration_protocol_count,
            external_system_count
        )
        
        # Calculate total
        total_days = (
            env_setup["total"] +
            target_setup["total"] +
            migration_execution["total"] +
            buffer["total"] +
            sum(fixed_components.values())
        )
        
        return {
            "breakdown": {
                "environment_setup": env_setup,
                "target_setup": target_setup,
                "migration_execution": migration_execution,
                "buffer": buffer,
                "fixed_components": fixed_components,
                "complexity": complexity
            },
            "totals": {
                "total_days": round(total_days, 2),
                "total_weeks": round(total_days / 5, 2),
                "total_months": round(total_days / 22, 2)
            },
            "summary": {
                "flow_count": flow_count,
                "environment_count": env_count,
                "infrastructure": infrastructure,
                "has_mq": has_mq,
                "complexity_multiplier": complexity["multiplier"]
            }
        }


# Example usage and validation
if __name__ == "__main__":
    # Test case: 150 flows, 4 environments, container, with MQ
    result = RulesEngine.calculate_total_estimate(
        flow_count=150,
        env_count=4,
        infrastructure="container",
        has_mq=True,
        setup_status="new",
        source_version="IIB_v10",
        host_platform="on_premise",
        has_custom_plugins=True,
        custom_plugin_count=3,
        integration_protocol_count=5,
        external_system_count=8
    )
    
    import json
    print(json.dumps(result, indent=2))
