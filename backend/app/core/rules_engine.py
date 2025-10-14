"""
IBM ACE Migration Estimation Rules Engine

This module implements the exact calculation rules for estimating
IBM ACE migration time from WMB/IIB to ACE.

All formulas are based on validated business rules and must be
implemented exactly as specified.
"""

from typing import Dict, List, Optional
from enum import Enum


class TeamBand(str, Enum):
    """Team band classification affecting estimation"""
    BAND_6G = "6G"
    BAND_OTHER = "6B_8_9_10"


class Infrastructure(str, Enum):
    """Infrastructure type for target environment"""
    CONTAINER = "container"
    VMWARE = "vmware"
    BARE_METAL = "bare_metal"
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
    def calculate_flow_migration_time(
        flow_count: int,
        team_band: str
    ) -> Dict[str, float]:
        """
        Calculate flow migration time based on team band.
        
        Rules:
        - Band 6G: 10 days per 50 flows (0.2 days per flow)
        - Other bands: 5 days per 50 flows (0.1 days per flow)
        - Buffer: 6 days per 50 flows for unforeseen issues
        
        Args:
            flow_count: Total number of flows to migrate
            team_band: Team band classification (6G or other)
            
        Returns:
            Dictionary with base_time, buffer, and total
        """
        # Determine days per flow based on team band
        if team_band == TeamBand.BAND_6G:
            days_per_flow = 0.2
        else:
            days_per_flow = 0.1
        
        # Calculate base migration time
        base_time = flow_count * days_per_flow
        
        # Calculate buffer (6 days per 50 flows)
        buffer = (flow_count // 50) * 6
        if flow_count % 50 > 0:  # Add buffer for remaining flows
            buffer += 6
        
        total = base_time + buffer
        
        return {
            "base_time": round(base_time, 2),
            "buffer": round(buffer, 2),
            "total": round(total, 2),
            "flows": flow_count,
            "team_band": team_band
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
            infrastructure: Infrastructure type (container, vmware, etc.)
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
        
        Rules:
        - 5 flows per 2 days (includes migration + testing)
        
        Args:
            flow_count: Total number of flows
            
        Returns:
            Dictionary with execution time
        """
        # 5 flows per 2 days = 0.4 days per flow
        time = (flow_count / 5) * 2
        
        return {
            "total": round(time, 2),
            "flows": flow_count,
            "flows_per_batch": 5,
            "days_per_batch": 2
        }
    
    @staticmethod
    def get_fixed_components() -> Dict[str, float]:
        """
        Get fixed component times.
        
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
        team_band: str,
        env_count: int,
        infrastructure: str,
        has_mq: bool,
        setup_status: str,
        has_custom_plugins: bool = False,
        custom_plugin_count: int = 0,
        integration_protocol_count: int = 0,
        external_system_count: int = 0
    ) -> Dict:
        """
        Master calculation combining all rules.
        
        Args:
            flow_count: Total number of flows
            team_band: Team band classification
            env_count: Number of environments
            infrastructure: Infrastructure type
            has_mq: Whether MQ is required
            setup_status: Target setup status
            has_custom_plugins: Whether custom plugins exist
            custom_plugin_count: Number of custom plugins
            integration_protocol_count: Number of integration protocols
            external_system_count: Number of external systems
            
        Returns:
            Complete estimation breakdown with all components
        """
        # Calculate each component
        flow_migration = RulesEngine.calculate_flow_migration_time(
            flow_count, team_band
        )
        
        env_setup = RulesEngine.calculate_environment_setup_time(
            env_count, infrastructure, has_mq
        )
        
        target_setup = RulesEngine.calculate_target_setup_time(setup_status)
        
        migration_execution = RulesEngine.calculate_migration_execution_time(
            flow_count
        )
        
        fixed_components = RulesEngine.get_fixed_components()
        
        complexity = RulesEngine.calculate_complexity_multiplier(
            has_custom_plugins,
            custom_plugin_count,
            integration_protocol_count,
            external_system_count
        )
        
        # Calculate base total
        base_total = (
            flow_migration["total"] +
            env_setup["total"] +
            target_setup["total"] +
            migration_execution["total"] +
            sum(fixed_components.values())
        )
        
        # Apply complexity multiplier
        adjusted_total = base_total * complexity["multiplier"]
        
        return {
            "breakdown": {
                "flow_migration": flow_migration,
                "environment_setup": env_setup,
                "target_setup": target_setup,
                "migration_execution": migration_execution,
                "fixed_components": fixed_components,
                "complexity": complexity
            },
            "totals": {
                "base_days": round(base_total, 2),
                "complexity_adjustment": round(adjusted_total - base_total, 2),
                "total_days": round(adjusted_total, 2),
                "total_weeks": round(adjusted_total / 5, 2),
                "total_months": round(adjusted_total / 22, 2)
            },
            "summary": {
                "flow_count": flow_count,
                "team_band": team_band,
                "environment_count": env_count,
                "infrastructure": infrastructure,
                "has_mq": has_mq,
                "complexity_multiplier": complexity["multiplier"]
            }
        }


# Example usage and validation
if __name__ == "__main__":
    # Test case: 100 flows, Band 6G, 4 environments, container, with MQ
    result = RulesEngine.calculate_total_estimate(
        flow_count=100,
        team_band="6G",
        env_count=4,
        infrastructure="container",
        has_mq=True,
        setup_status="new",
        has_custom_plugins=True,
        custom_plugin_count=3,
        integration_protocol_count=5,
        external_system_count=8
    )
    
    import json
    print(json.dumps(result, indent=2))
