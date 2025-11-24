"""Project analysis service for automatic project type detection and metadata extraction."""
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum


class ProjectType(Enum):
    NEXTJS = "nextjs"
    VITE = "vite"
    REACT = "react"
    NODE = "node"
    PYTHON = "python"
    FLASK = "flask"
    DJANGO = "django"
    SPRING = "spring"
    GO = "go"
    RUST = "rust"
    DOTNET = "dotnet"
    OTHER = "other"


@dataclass
class ProjectMetadata:
    """Metadata extracted from project analysis."""
    project_type: ProjectType
    languages: Set[str]
    frameworks: Set[str]
    dependencies: Dict[str, str]
    dev_dependencies: Dict[str, str]
    build_commands: List[str]
    start_commands: List[str]
    test_commands: List[str]
    has_tests: bool
    test_frameworks: Set[str]
    folder_structure: Dict[str, Any]
    config_files: List[str]
    entry_points: List[str]
    package_managers: Set[str]
    deployment_indicators: List[str]
    vulnerabilities: List[str]
    health_score: int  # 0-100


class ProjectAnalyzer:
    """Service for analyzing project structure and generating metadata."""

    def __init__(self):
        self.project_root: Optional[Path] = None

    def analyze_project(self, project_path: str) -> ProjectMetadata:
        """
        Analyze a project directory and extract comprehensive metadata.

        Args:
            project_path: Path to the project root directory

        Returns:
            ProjectMetadata object with all detected information
        """
        self.project_root = Path(project_path).resolve()

        if not self.project_root.exists() or not self.project_root.is_dir():
            raise ValueError(f"Project path does not exist or is not a directory: {project_path}")

        # Detect project type
        project_type = self._detect_project_type()

        # Extract metadata
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        dependencies, dev_dependencies = self._extract_dependencies()
        build_commands = self._detect_build_commands()
        start_commands = self._detect_start_commands()
        test_commands, has_tests, test_frameworks = self._detect_test_info()
        folder_structure = self._analyze_folder_structure()
        config_files = self._find_config_files()
        entry_points = self._find_entry_points()
        package_managers = self._detect_package_managers()
        deployment_indicators = self._detect_deployment_indicators()
        vulnerabilities = self._scan_vulnerabilities()
        health_score = self._calculate_health_score()

        return ProjectMetadata(
            project_type=project_type,
            languages=languages,
            frameworks=frameworks,
            dependencies=dependencies,
            dev_dependencies=dev_dependencies,
            build_commands=build_commands,
            start_commands=start_commands,
            test_commands=test_commands,
            has_tests=has_tests,
            test_frameworks=test_frameworks,
            folder_structure=folder_structure,
            config_files=config_files,
            entry_points=entry_points,
            package_managers=package_managers,
            deployment_indicators=deployment_indicators,
            vulnerabilities=vulnerabilities,
            health_score=health_score
        )

    def _detect_project_type(self) -> ProjectType:
        """Detect the main project type based on files and structure."""
        files = list(self.project_root.glob("*"))
        filenames = {f.name for f in files}

        # Next.js
        if "next.config.js" in filenames or "next.config.mjs" in filenames:
            return ProjectType.NEXTJS

        # Vite
        if "vite.config.js" in filenames or "vite.config.ts" in filenames:
            return ProjectType.VITE

        # React (check package.json)
        if "package.json" in filenames:
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    deps = package_data.get("dependencies", {})

                    if "next" in deps:
                        return ProjectType.NEXTJS
                    elif "vite" in deps:
                        return ProjectType.VITE
                    elif "react" in deps:
                        return ProjectType.REACT
                    elif "express" in deps or "fastify" in deps:
                        return ProjectType.NODE
            except:
                pass

        # Python frameworks
        if "requirements.txt" in filenames or "pyproject.toml" in filenames or "setup.py" in filenames:
            if "manage.py" in filenames:
                return ProjectType.DJANGO
            elif "app.py" in filenames or "main.py" in filenames:
                # Check for Flask imports
                try:
                    for py_file in self.project_root.glob("*.py"):
                        with open(py_file, "r", encoding="utf-8") as f:
                            content = f.read()
                            if "from flask import" in content or "import flask" in content:
                                return ProjectType.FLASK
                except:
                    pass
                return ProjectType.PYTHON

        # Java/Spring
        if "pom.xml" in filenames or "build.gradle" in filenames:
            try:
                for xml_file in self.project_root.glob("pom.xml"):
                    with open(xml_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "spring-boot" in content:
                            return ProjectType.SPRING
            except:
                pass
            return ProjectType.OTHER  # Generic Java

        # Go
        if "go.mod" in filenames:
            return ProjectType.GO

        # Rust
        if "Cargo.toml" in filenames:
            return ProjectType.RUST

        # .NET
        if any(f.endswith(".csproj") for f in filenames) or "Program.cs" in filenames:
            return ProjectType.DOTNET

        return ProjectType.OTHER

    def _detect_languages(self) -> Set[str]:
        """Detect programming languages used in the project."""
        languages = set()

        # Check file extensions
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in [".js", ".jsx", ".mjs", ".cjs"]:
                    languages.add("JavaScript")
                elif ext in [".ts", ".tsx"]:
                    languages.add("TypeScript")
                elif ext == ".py":
                    languages.add("Python")
                elif ext in [".java", ".kt", ".scala"]:
                    languages.add("Java")
                elif ext == ".go":
                    languages.add("Go")
                elif ext == ".rs":
                    languages.add("Rust")
                elif ext in [".cs", ".vb"]:
                    languages.add(".NET")
                elif ext in [".cpp", ".cc", ".cxx", ".c++"]:
                    languages.add("C++")
                elif ext == ".c":
                    languages.add("C")
                elif ext in [".php"]:
                    languages.add("PHP")
                elif ext in [".rb"]:
                    languages.add("Ruby")

        return languages

    def _detect_frameworks(self) -> Set[str]:
        """Detect frameworks and libraries used."""
        frameworks = set()

        # Check package.json for Node.js frameworks
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

                    if "next" in deps:
                        frameworks.add("Next.js")
                    if "vite" in deps:
                        frameworks.add("Vite")
                    if "react" in deps:
                        frameworks.add("React")
                    if "vue" in deps:
                        frameworks.add("Vue.js")
                    if "angular" in deps:
                        frameworks.add("Angular")
                    if "express" in deps:
                        frameworks.add("Express.js")
                    if "fastify" in deps:
                        frameworks.add("Fastify")
                    if "nestjs" in deps:
                        frameworks.add("NestJS")
            except:
                pass

        # Check Python frameworks
        for py_file in self.project_root.glob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "from flask import" in content or "import flask" in content:
                        frameworks.add("Flask")
                    if "from django" in content or "import django" in content:
                        frameworks.add("Django")
                    if "from fastapi import" in content:
                        frameworks.add("FastAPI")
            except:
                pass

        # Check Java/Spring
        if (self.project_root / "pom.xml").exists():
            try:
                with open(self.project_root / "pom.xml", "r", encoding="utf-8") as f:
                    content = f.read()
                    if "spring-boot" in content:
                        frameworks.add("Spring Boot")
            except:
                pass

        return frameworks

    def _extract_dependencies(self) -> tuple[Dict[str, str], Dict[str, str]]:
        """Extract dependencies from various package files."""
        dependencies = {}
        dev_dependencies = {}

        # Node.js
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    dependencies = package_data.get("dependencies", {})
                    dev_dependencies = package_data.get("devDependencies", {})
            except:
                pass

        # Python
        if (self.project_root / "requirements.txt").exists():
            try:
                with open(self.project_root / "requirements.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "==" in line:
                                name, version = line.split("==", 1)
                                dependencies[name] = version
                            else:
                                dependencies[line] = "latest"
            except:
                pass

        # Go
        if (self.project_root / "go.mod").exists():
            try:
                with open(self.project_root / "go.mod", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("require "):
                            # Parse require block
                            pass
                        elif line.startswith("\t"):
                            parts = line.split()
                            if len(parts) >= 2:
                                dependencies[parts[0]] = parts[1]
            except:
                pass

        return dependencies, dev_dependencies

    def _detect_build_commands(self) -> List[str]:
        """Detect build commands from package.json or other config files."""
        commands = []

        # Node.js
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    scripts = package_data.get("scripts", {})

                    if "build" in scripts:
                        commands.append(f"npm run build")
                    if "compile" in scripts:
                        commands.append(f"npm run compile")
            except:
                pass

        # Python
        if (self.project_root / "setup.py").exists():
            commands.append("python setup.py build")

        # Go
        if (self.project_root / "go.mod").exists():
            commands.append("go build")

        # Rust
        if (self.project_root / "Cargo.toml").exists():
            commands.append("cargo build")

        return commands

    def _detect_start_commands(self) -> List[str]:
        """Detect start/dev commands."""
        commands = []

        # Node.js
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    scripts = package_data.get("scripts", {})

                    if "start" in scripts:
                        commands.append(f"npm start")
                    if "dev" in scripts:
                        commands.append(f"npm run dev")
            except:
                pass

        # Python
        if any(self.project_root.glob("*.py")):
            commands.append("python main.py")  # Generic

        # Go
        if (self.project_root / "go.mod").exists():
            commands.append("go run .")

        return commands

    def _detect_test_info(self) -> tuple[List[str], bool, Set[str]]:
        """Detect test commands and frameworks."""
        commands = []
        has_tests = False
        frameworks = set()

        # Node.js
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    scripts = package_data.get("scripts", {})
                    deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

                    if "test" in scripts:
                        commands.append("npm test")
                        has_tests = True

                    if "jest" in deps:
                        frameworks.add("Jest")
                    if "mocha" in deps:
                        frameworks.add("Mocha")
                    if "vitest" in deps:
                        frameworks.add("Vitest")
            except:
                pass

        # Python
        if any(self.project_root.glob("test_*.py")) or any(self.project_root.glob("*_test.py")):
            has_tests = True
            commands.append("python -m pytest")
            frameworks.add("pytest")

        # Check for test directories
        test_dirs = ["test", "tests", "__tests__", "spec", "specs"]
        for test_dir in test_dirs:
            if (self.project_root / test_dir).exists():
                has_tests = True
                break

        return commands, has_tests, frameworks

    def _analyze_folder_structure(self) -> Dict[str, Any]:
        """Analyze and summarize folder structure."""
        structure = {}

        def analyze_dir(path: Path, max_depth=3, current_depth=0) -> Dict[str, Any]:
            if current_depth >= max_depth:
                return {"type": "directory", "truncated": True}

            result = {"type": "directory", "children": {}}

            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith("."):
                        continue  # Skip hidden files

                    if item.is_file():
                        result["children"][item.name] = {"type": "file"}
                    elif item.is_dir():
                        result["children"][item.name] = analyze_dir(item, max_depth, current_depth + 1)
            except PermissionError:
                result["error"] = "Permission denied"

            return result

        structure = analyze_dir(self.project_root)
        return structure

    def _find_config_files(self) -> List[str]:
        """Find configuration files."""
        config_files = []
        config_patterns = [
            "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg", "*.conf",
            "*.env*", ".env*", "*.properties", "*.xml", "*.gradle", "*.mk"
        ]

        for pattern in config_patterns:
            for file_path in self.project_root.glob(f"**/{pattern}"):
                if file_path.is_file():
                    config_files.append(str(file_path.relative_to(self.project_root)))

        return config_files

    def _find_entry_points(self) -> List[str]:
        """Find main entry points."""
        entry_points = []

        # Common entry point files
        common_entries = [
            "main.py", "app.py", "index.js", "index.ts", "server.js", "app.js",
            "main.go", "lib/main.dart", "src/main/java", "Program.cs", "main.rs"
        ]

        for entry in common_entries:
            if (self.project_root / entry).exists():
                entry_points.append(entry)

        # Check package.json main field
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    main = package_data.get("main")
                    if main and (self.project_root / main).exists():
                        entry_points.append(main)
            except:
                pass

        return entry_points

    def _detect_package_managers(self) -> Set[str]:
        """Detect package managers used."""
        managers = set()

        if (self.project_root / "package.json").exists():
            managers.add("npm")
            if (self.project_root / "yarn.lock").exists():
                managers.add("yarn")
            if (self.project_root / "pnpm-lock.yaml").exists():
                managers.add("pnpm")

        if (self.project_root / "requirements.txt").exists() or (self.project_root / "pyproject.toml").exists():
            managers.add("pip")

        if (self.project_root / "go.mod").exists():
            managers.add("go modules")

        if (self.project_root / "Cargo.toml").exists():
            managers.add("cargo")

        return managers

    def _detect_deployment_indicators(self) -> List[str]:
        """Detect deployment-related files and configurations."""
        indicators = []

        deployment_files = [
            "Dockerfile", "docker-compose.yml", ".dockerignore",
            "vercel.json", "netlify.toml", "heroku.yml",
            ".github/workflows", "Jenkinsfile", ".gitlab-ci.yml",
            "serverless.yml", "app.yaml", "Procfile"
        ]

        for file_pattern in deployment_files:
            if list(self.project_root.glob(f"**/{file_pattern}")):
                indicators.append(file_pattern)

        return indicators

    def _scan_vulnerabilities(self) -> List[str]:
        """Basic vulnerability scanning (placeholder for more advanced scanning)."""
        vulnerabilities = []

        # Check for common security issues
        if (self.project_root / "package.json").exists():
            try:
                with open(self.project_root / "package.json", "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

                    # Check for known vulnerable packages (simplified)
                    vulnerable_packages = ["left-pad"]  # Example
                    for vuln in vulnerable_packages:
                        if vuln in deps:
                            vulnerabilities.append(f"Potentially vulnerable package: {vuln}")
            except:
                pass

        # Check for exposed secrets
        secret_patterns = [".env", "secrets", "keys"]
        for pattern in secret_patterns:
            if list(self.project_root.glob(f"**/{pattern}*")):
                vulnerabilities.append(f"Potential secrets file: {pattern}")

        return vulnerabilities

    def _calculate_health_score(self) -> int:
        """Calculate a basic health score for the project."""
        score = 50  # Base score

        # Add points for good practices
        if self._detect_test_info()[1]:  # Has tests
            score += 20

        if self._find_config_files():  # Has config files
            score += 10

        if self._find_entry_points():  # Has clear entry points
            score += 10

        if self._detect_deployment_indicators():  # Has deployment config
            score += 10

        # Subtract points for issues
        if self._scan_vulnerabilities():
            score -= 20

        return max(0, min(100, score))


# Global analyzer instance
project_analyzer = ProjectAnalyzer()