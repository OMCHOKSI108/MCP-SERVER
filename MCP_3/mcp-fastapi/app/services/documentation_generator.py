"""AI-powered documentation and PRD generation service."""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.services.project_analyzer import ProjectMetadata, ProjectType
from app.services.config_service import config_service


class DocumentationGenerator:
    """Service for generating comprehensive project documentation using AI."""

    def __init__(self):
        self.templates = {
            "prd": self._get_prd_template(),
            "feature_list": self._get_feature_list_template(),
            "tech_summary": self._get_tech_summary_template(),
            "health_report": self._get_health_report_template(),
            "improvements": self._get_improvements_template(),
            "testing_plan": self._get_testing_plan_template()
        }

    async def generate_prd(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive Product Requirements Document.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            PRD document
        """
        # Get AI analysis (placeholder - would call actual AI service)
        ai_analysis = await self._get_ai_analysis(metadata, "prd", user_id)

        prd = {
            "title": f"Product Requirements Document - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "project_type": metadata.project_type.value,
            "overview": {
                "description": ai_analysis.get("description", "AI-powered project analysis"),
                "target_audience": ai_analysis.get("target_audience", "Developers and stakeholders"),
                "key_features": ai_analysis.get("key_features", []),
                "technologies": list(metadata.languages) + list(metadata.frameworks)
            },
            "functional_requirements": ai_analysis.get("functional_requirements", []),
            "non_functional_requirements": ai_analysis.get("non_functional_requirements", []),
            "user_stories": ai_analysis.get("user_stories", []),
            "acceptance_criteria": ai_analysis.get("acceptance_criteria", []),
            "dependencies": {
                "runtime": metadata.dependencies,
                "development": metadata.dev_dependencies
            },
            "deployment": {
                "commands": metadata.build_commands + metadata.start_commands,
                "indicators": metadata.deployment_indicators
            }
        }

        return prd

    async def generate_feature_list(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive feature list.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Feature list document
        """
        ai_analysis = await self._get_ai_analysis(metadata, "features", user_id)

        features = {
            "title": f"Feature Analysis - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "core_features": ai_analysis.get("core_features", []),
            "secondary_features": ai_analysis.get("secondary_features", []),
            "technical_features": ai_analysis.get("technical_features", []),
            "missing_features": ai_analysis.get("missing_features", []),
            "feature_complexity": ai_analysis.get("feature_complexity", "medium"),
            "estimated_effort": ai_analysis.get("estimated_effort", "medium")
        }

        return features

    async def generate_tech_summary(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a technical summary.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Technical summary document
        """
        tech_summary = {
            "title": f"Technical Summary - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "languages": list(metadata.languages),
            "frameworks": list(metadata.frameworks),
            "architecture": self._infer_architecture(metadata),
            "dependencies": {
                "count": len(metadata.dependencies) + len(metadata.dev_dependencies),
                "runtime": len(metadata.dependencies),
                "development": len(metadata.dev_dependencies)
            },
            "build_tools": metadata.package_managers,
            "test_coverage": "detected" if metadata.has_tests else "not detected",
            "deployment_ready": len(metadata.deployment_indicators) > 0,
            "entry_points": metadata.entry_points,
            "config_files": metadata.config_files
        }

        return tech_summary

    async def generate_health_report(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a project health report.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Health report document
        """
        ai_analysis = await self._get_ai_analysis(metadata, "health", user_id)

        health_report = {
            "title": f"Project Health Report - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "overall_score": metadata.health_score,
            "score_breakdown": {
                "testing": 100 if metadata.has_tests else 0,
                "documentation": 80 if metadata.config_files else 40,
                "deployment": 100 if metadata.deployment_indicators else 0,
                "security": 100 - (len(metadata.vulnerabilities) * 20)
            },
            "issues": ai_analysis.get("issues", []),
            "recommendations": ai_analysis.get("recommendations", []),
            "vulnerabilities": metadata.vulnerabilities,
            "strengths": ai_analysis.get("strengths", []),
            "risks": ai_analysis.get("risks", [])
        }

        return health_report

    async def generate_improvements(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate improvement recommendations.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Improvements document
        """
        ai_analysis = await self._get_ai_analysis(metadata, "improvements", user_id)

        improvements = {
            "title": f"Improvement Recommendations - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "code_quality": ai_analysis.get("code_quality_improvements", []),
            "security": ai_analysis.get("security_improvements", []),
            "performance": ai_analysis.get("performance_improvements", []),
            "testing": ai_analysis.get("testing_improvements", []),
            "documentation": ai_analysis.get("documentation_improvements", []),
            "folder_cleanup": self._generate_folder_cleanup_suggestions(metadata),
            "priority_order": ai_analysis.get("priority_order", ["high", "medium", "low"])
        }

        return improvements

    async def generate_testing_plan(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive testing plan.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Testing plan document
        """
        ai_analysis = await self._get_ai_analysis(metadata, "testing", user_id)

        testing_plan = {
            "title": f"Testing Plan - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "current_coverage": "detected" if metadata.has_tests else "none",
            "test_frameworks": list(metadata.test_frameworks),
            "recommended_tests": ai_analysis.get("recommended_tests", []),
            "unit_tests": ai_analysis.get("unit_tests", []),
            "integration_tests": ai_analysis.get("integration_tests", []),
            "e2e_tests": ai_analysis.get("e2e_tests", []),
            "test_commands": metadata.test_commands,
            "coverage_goals": ai_analysis.get("coverage_goals", "80%"),
            "ci_cd_integration": ai_analysis.get("ci_cd_integration", [])
        }

        return testing_plan

    async def generate_codebase_summary(self, metadata: ProjectMetadata, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive codebase summary.

        Args:
            metadata: Project metadata
            user_id: User ID for context

        Returns:
            Codebase summary document
        """
        ai_analysis = await self._get_ai_analysis(metadata, "codebase", user_id)

        summary = {
            "title": f"Codebase Summary - {metadata.project_type.value.title()} Project",
            "generated_at": datetime.now().isoformat(),
            "file_count": ai_analysis.get("file_count", 0),
            "line_count": ai_analysis.get("line_count", 0),
            "main_components": ai_analysis.get("main_components", []),
            "architecture_patterns": ai_analysis.get("architecture_patterns", []),
            "code_quality_metrics": ai_analysis.get("code_quality_metrics", {}),
            "folder_structure": metadata.folder_structure,
            "entry_points": metadata.entry_points,
            "external_dependencies": len(metadata.dependencies),
            "internal_modules": ai_analysis.get("internal_modules", [])
        }

        return summary

    async def _get_ai_analysis(self, metadata: ProjectMetadata, analysis_type: str, user_id: str) -> Dict[str, Any]:
        """
        Get AI-powered analysis for different aspects of the project.
        This is a placeholder that would call an actual AI service.
        """
        # Get provider config to determine if we can use AI
        provider_config = await config_service.get_provider_config(user_id)

        if not provider_config.has_api_key:
            # Return basic analysis without AI
            return self._get_basic_analysis(metadata, analysis_type)

        # TODO: Implement actual AI service calls here
        # For now, return structured placeholder data
        return self._get_mock_ai_analysis(metadata, analysis_type)

    def _get_basic_analysis(self, metadata: ProjectMetadata, analysis_type: str) -> Dict[str, Any]:
        """Provide basic analysis when AI is not available."""
        if analysis_type == "prd":
            return {
                "description": f"A {metadata.project_type.value} project with {len(metadata.languages)} programming languages",
                "target_audience": "Developers",
                "key_features": ["Basic functionality detected"],
                "functional_requirements": ["Core features implemented"],
                "non_functional_requirements": ["Performance", "Security"],
                "user_stories": ["As a user, I want to..."],
                "acceptance_criteria": ["Must work correctly"]
            }
        elif analysis_type == "features":
            return {
                "core_features": ["Basic functionality"],
                "secondary_features": [],
                "technical_features": list(metadata.frameworks),
                "missing_features": ["Advanced features"],
                "feature_complexity": "medium",
                "estimated_effort": "medium"
            }
        elif analysis_type == "health":
            return {
                "issues": ["Limited analysis without AI"],
                "recommendations": ["Enable AI analysis for better insights"],
                "strengths": ["Project structure detected"],
                "risks": ["Unknown issues without AI analysis"]
            }
        elif analysis_type == "improvements":
            return {
                "code_quality_improvements": ["Add documentation"],
                "security_improvements": ["Review dependencies"],
                "performance_improvements": ["Optimize code"],
                "testing_improvements": ["Add tests"],
                "documentation_improvements": ["Add README"],
                "priority_order": ["high", "medium", "low"]
            }
        elif analysis_type == "testing":
            return {
                "recommended_tests": ["Unit tests", "Integration tests"],
                "unit_tests": ["Test individual functions"],
                "integration_tests": ["Test component interactions"],
                "e2e_tests": ["Test user workflows"],
                "coverage_goals": "80%",
                "ci_cd_integration": ["GitHub Actions", "Jenkins"]
            }
        elif analysis_type == "codebase":
            return {
                "file_count": 0,
                "line_count": 0,
                "main_components": ["Main application"],
                "architecture_patterns": ["MVC", "API"],
                "code_quality_metrics": {"complexity": "medium"},
                "internal_modules": ["Core module"]
            }

        return {}

    def _get_mock_ai_analysis(self, metadata: ProjectMetadata, analysis_type: str) -> Dict[str, Any]:
        """Mock AI analysis for development - replace with actual AI calls."""
        # This would be replaced with actual AI service calls
        if analysis_type == "prd":
            return {
                "description": f"A modern {metadata.project_type.value} application built with {', '.join(metadata.languages)}",
                "target_audience": "End users and developers",
                "key_features": [
                    "User authentication and authorization",
                    "Data management and storage",
                    "API endpoints for client communication",
                    "Responsive user interface",
                    "Automated testing suite"
                ],
                "functional_requirements": [
                    "User registration and login",
                    "CRUD operations for main entities",
                    "Data validation and error handling",
                    "API documentation",
                    "Logging and monitoring"
                ],
                "non_functional_requirements": [
                    "Response time < 500ms for API calls",
                    "99.9% uptime",
                    "Mobile-responsive design",
                    "Security best practices",
                    "Scalable architecture"
                ],
                "user_stories": [
                    "As a user, I want to register an account so I can access the application",
                    "As a developer, I want API documentation so I can integrate with the system",
                    "As an admin, I want to manage users so I can control access"
                ],
                "acceptance_criteria": [
                    "All user stories implemented and tested",
                    "Code coverage > 80%",
                    "Performance benchmarks met",
                    "Security audit passed"
                ]
            }
        # Add other analysis types...
        return self._get_basic_analysis(metadata, analysis_type)

    def _infer_architecture(self, metadata: ProjectMetadata) -> str:
        """Infer the project architecture based on metadata."""
        if metadata.project_type in [ProjectType.NEXTJS, ProjectType.REACT, ProjectType.VITE]:
            return "Frontend Application (SPA/MPA)"
        elif metadata.project_type in [ProjectType.NODE]:
            return "Backend API Server"
        elif metadata.project_type in [ProjectType.FLASK, ProjectType.DJANGO]:
            return "Web Application (MVC)"
        elif metadata.project_type in [ProjectType.SPRING]:
            return "Enterprise Java Application"
        elif metadata.project_type in [ProjectType.GO]:
            return "Microservice/API Server"
        else:
            return "General Application"

    def _generate_folder_cleanup_suggestions(self, metadata: ProjectMetadata) -> List[str]:
        """Generate folder cleanup suggestions."""
        suggestions = []

        # Check for common issues
        structure = metadata.folder_structure

        # Look for empty directories, unused files, etc.
        # This is a simplified version
        suggestions.append("Remove unused dependency files")
        suggestions.append("Organize imports and exports")
        suggestions.append("Remove commented-out code")
        suggestions.append("Consolidate duplicate utilities")

        if not metadata.has_tests:
            suggestions.append("Create tests directory structure")

        return suggestions

    def _get_prd_template(self) -> str:
        """Get PRD generation template."""
        return """
Generate a comprehensive Product Requirements Document for this project.

Project Type: {project_type}
Languages: {languages}
Frameworks: {frameworks}
Dependencies: {dependencies}

Focus on:
1. Clear problem statement and solution
2. Target audience and user personas
3. Core features and functionality
4. Technical requirements and constraints
5. Success metrics and acceptance criteria
"""

    def _get_feature_list_template(self) -> str:
        """Get feature list generation template."""
        return """
Analyze the codebase and generate a comprehensive feature list.

Include:
1. Core features currently implemented
2. Secondary/missing features
3. Technical capabilities
4. Feature complexity assessment
5. Development effort estimation
"""

    def _get_tech_summary_template(self) -> str:
        """Get technical summary template."""
        return """
Create a technical summary covering:
1. Technology stack analysis
2. Architecture overview
3. Dependencies and libraries
4. Development tools and workflows
5. Deployment and infrastructure
"""

    def _get_health_report_template(self) -> str:
        """Get health report template."""
        return """
Generate a project health assessment including:
1. Code quality metrics
2. Security vulnerabilities
3. Performance considerations
4. Testing coverage
5. Maintenance recommendations
"""

    def _get_improvements_template(self) -> str:
        """Get improvements template."""
        return """
Suggest specific improvements for:
1. Code quality and maintainability
2. Security enhancements
3. Performance optimizations
4. Testing improvements
5. Documentation updates
"""

    def _get_testing_plan_template(self) -> str:
        """Get testing plan template."""
        return """
Create a comprehensive testing strategy including:
1. Unit testing approach
2. Integration testing
3. End-to-end testing
4. Test automation
5. CI/CD integration
"""


# Global documentation generator instance
documentation_generator = DocumentationGenerator()