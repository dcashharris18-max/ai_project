"""
Construction Module
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


class ConstructionManager:
    """
    Construction project management powered by AI
    """
    
    def __init__(self, config: Dict[str, Any], ai_model):
        """
        Initialize the construction manager
        
        Args:
            config: Configuration for construction
            ai_model: AI model instance
        """
        self.config = config
        self.ai_model = ai_model
        self.projects = []
        self.resources = []
        logger.info("Construction Manager initialized")
    
    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new construction project
        
        Args:
            project_data: Project details
            
        Returns:
            Created project
        """
        project = {
            'id': f"PROJ-{len(self.projects) + 1:05d}",
            'name': project_data.get('name'),
            'type': project_data.get('type', 'residential'),
            'location': project_data.get('location'),
            'budget': project_data.get('budget', 100000),
            'duration_days': project_data.get('duration_days', 180),
            'status': 'planning',
            'created_at': datetime.now().isoformat()
        }
        
        self.projects.append(project)
        logger.info(f"Project created: {project['id']}")
        return project
    
    def estimate_costs(self, project_type: str, size_sqft: float) -> Dict[str, Any]:
        """
        AI-powered cost estimation
        
        Args:
            project_type: Type of construction project
            size_sqft: Project size in square feet
            
        Returns:
            Cost estimation
        """
        # Base cost per square foot by type
        base_costs = {
            'residential': 150,
            'commercial': 200,
            'infrastructure': 250
        }
        
        base_cost_per_sqft = base_costs.get(project_type, 150)
        
        estimate = {
            'project_type': project_type,
            'size_sqft': size_sqft,
            'base_cost_per_sqft': base_cost_per_sqft,
            'materials_cost': size_sqft * base_cost_per_sqft * 0.4,
            'labor_cost': size_sqft * base_cost_per_sqft * 0.35,
            'equipment_cost': size_sqft * base_cost_per_sqft * 0.15,
            'overhead_cost': size_sqft * base_cost_per_sqft * 0.1,
            'timestamp': datetime.now().isoformat()
        }
        
        estimate['total_cost'] = (
            estimate['materials_cost'] +
            estimate['labor_cost'] +
            estimate['equipment_cost'] +
            estimate['overhead_cost']
        )
        
        # AI adjustment
        if self.ai_model.is_trained:
            features = np.array([[size_sqft, base_cost_per_sqft]])
            adjustment = self.ai_model.predict(features)
            estimate['ai_adjusted_cost'] = estimate['total_cost'] * (1 + adjustment[0][0] * 0.1)
            estimate['confidence'] = float(abs(adjustment[0][0]))
        else:
            estimate['ai_adjusted_cost'] = estimate['total_cost']
            estimate['confidence'] = 0.5
        
        return estimate
    
    def plan_resources(self, project_id: str) -> Dict[str, Any]:
        """
        Plan resources for a project
        
        Args:
            project_id: Project ID
            
        Returns:
            Resource planning
        """
        resource_plan = {
            'project_id': project_id,
            'workforce': {
                'engineers': np.random.randint(2, 10),
                'laborers': np.random.randint(10, 50),
                'supervisors': np.random.randint(1, 5),
                'specialists': np.random.randint(3, 15)
            },
            'equipment': {
                'excavators': np.random.randint(1, 5),
                'cranes': np.random.randint(1, 3),
                'trucks': np.random.randint(2, 10),
                'tools': np.random.randint(50, 200)
            },
            'materials': {
                'concrete_tons': np.random.randint(100, 1000),
                'steel_tons': np.random.randint(50, 500),
                'lumber_board_feet': np.random.randint(1000, 10000)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return resource_plan
    
    def track_progress(self, project_id: str) -> Dict[str, Any]:
        """
        Track construction project progress
        
        Args:
            project_id: Project ID
            
        Returns:
            Progress metrics
        """
        progress = {
            'project_id': project_id,
            'completion_percentage': np.random.uniform(0, 100),
            'days_elapsed': np.random.randint(0, 180),
            'budget_used_percentage': np.random.uniform(0, 100),
            'milestones': {
                'foundation': np.random.choice(['completed', 'in_progress', 'pending']),
                'framing': np.random.choice(['completed', 'in_progress', 'pending']),
                'systems': np.random.choice(['completed', 'in_progress', 'pending']),
                'finishing': np.random.choice(['completed', 'in_progress', 'pending'])
            },
            'status': 'on_track',
            'timestamp': datetime.now().isoformat()
        }
        
        # Determine overall status
        if progress['budget_used_percentage'] > progress['completion_percentage'] + 10:
            progress['status'] = 'over_budget'
        elif progress['completion_percentage'] < 50 and progress['days_elapsed'] > 90:
            progress['status'] = 'delayed'
        
        return progress
    
    def identify_risks(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Identify project risks using AI
        
        Args:
            project_id: Project ID
            
        Returns:
            List of identified risks
        """
        risk_types = [
            'weather_delays',
            'material_shortage',
            'labor_shortage',
            'budget_overrun',
            'regulatory_compliance'
        ]
        
        risks = []
        for risk_type in risk_types[:3]:  # Top 3 risks
            risk = {
                'project_id': project_id,
                'risk_type': risk_type,
                'probability': np.random.uniform(0.1, 0.8),
                'impact': np.random.choice(['low', 'medium', 'high']),
                'mitigation_strategy': f"Implement {risk_type} mitigation measures",
                'timestamp': datetime.now().isoformat()
            }
            risks.append(risk)
        
        return sorted(risks, key=lambda x: x['probability'], reverse=True)
    
    def optimize_schedule(self, project_id: str) -> Dict[str, Any]:
        """
        Optimize project schedule using AI
        
        Args:
            project_id: Project ID
            
        Returns:
            Optimized schedule
        """
        schedule = {
            'project_id': project_id,
            'phases': [
                {'name': 'Planning', 'duration_days': 14, 'status': 'completed'},
                {'name': 'Foundation', 'duration_days': 30, 'status': 'in_progress'},
                {'name': 'Construction', 'duration_days': 90, 'status': 'pending'},
                {'name': 'Finishing', 'duration_days': 30, 'status': 'pending'},
                {'name': 'Inspection', 'duration_days': 16, 'status': 'pending'}
            ],
            'critical_path': ['Foundation', 'Construction', 'Finishing'],
            'optimized': True,
            'timestamp': datetime.now().isoformat()
        }
        
        return schedule
    
    def get_project_summary(self) -> Dict[str, Any]:
        """
        Get construction projects summary
        
        Returns:
            Projects summary
        """
        return {
            'total_projects': len(self.projects),
            'active_projects': sum(1 for p in self.projects if p['status'] != 'completed'),
            'project_types': self.config.get('project_types', []),
            'timestamp': datetime.now().isoformat()
        }
