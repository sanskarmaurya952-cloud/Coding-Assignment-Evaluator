# main_evaluator.py
import ast
import subprocess
import tempfile
import os
import json
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import requests
from github import Github
import openai
from datetime import datetime

@dataclass
class EvaluationResult:
    overall_score: float
    correctness_score: float
    quality_score: float
    efficiency_score: float
    readability_score: float
    edge_cases_score: float
    feedback: Dict[str, List[str]]
    suggestions: List[str]
    strengths: List[str]

class Language(Enum):
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    JAVASCRIPT = "javascript"

class CodingEvaluator:
    def __init__(self, openai_api_key: str = None, github_token: str = None):
        self.openai_api_key = openai_api_key
        self.github_token = github_token
        if openai_api_key:
            openai.api_key = openai_api_key
        
    def evaluate_submission(self, code_input: str, problem_description: str = "", 
                          test_cases: List[Dict] = None, language: Language = Language.PYTHON) -> EvaluationResult:
        """Main evaluation function"""
        
        # Determine if input is URL or direct code
        if self._is_github_url(code_input):
            code = self._fetch_github_code(code_input)
        elif os.path.isfile(code_input):
            with open(code_input, 'r') as f:
                code = f.read()
        else:
            code = code_input
        
        # Run all evaluation components
        correctness_score = self._evaluate_correctness(code, test_cases, language)
        quality_score = self._evaluate_code_quality(code, language)
        efficiency_score = self._evaluate_efficiency(code, language)
        readability_score = self._evaluate_readability(code, language)
        edge_cases_score = self._evaluate_edge_cases(code, test_cases, language)
        
        # Generate AI feedback
        feedback, suggestions, strengths = self._generate_ai_feedback(
            code, problem_description, correctness_score, quality_score, 
            efficiency_score, readability_score, edge_cases_score
        )
        
        # Calculate overall score (weighted)
        overall_score = (
            correctness_score * 0.3 +
            quality_score * 0.25 +
            efficiency_score * 0.2 +
            readability_score * 0.15 +
            edge_cases_score * 0.1
        )
        
        return EvaluationResult(
            overall_score=round(overall_score, 1),
            correctness_score=correctness_score,
            quality_score=quality_score,
            efficiency_score=efficiency_score,
            readability_score=readability_score,
            edge_cases_score=edge_cases_score,
            feedback=feedback,
            suggestions=suggestions,
            strengths=strengths
        )
    
    def _is_github_url(self, url: str) -> bool:
        return "github.com" in url
    
    def _fetch_github_code(self, url: str) -> str:
        """Fetch code from GitHub URL"""
        try:
            if self.github_token:
                g = Github(self.github_token)
            
            # Parse GitHub URL to get repo and file path
            parts = url.split('/')
            owner = parts[3]
            repo_name = parts[4]
            file_path = '/'.join(parts[7:])  # Remove 'blob/branch' part
            
            repo = g.get_repo(f"{owner}/{repo_name}")
            file_content = repo.get_contents(file_path)
            return file_content.decoded_content.decode('utf-8')
        except Exception as e:
            raise Exception(f"Error fetching GitHub code: {str(e)}")
    
    def _evaluate_correctness(self, code: str, test_cases: List[Dict], language: Language) -> float:
        """Evaluate correctness by running test cases"""
        if not test_cases:
            return 85.0  # Default score if no test cases
        
        passed = 0
        total = len(test_cases)
        
        try:
            if language == Language.PYTHON:
                passed = self._run_python_tests(code, test_cases)
            # Add other language support here
            
            return (passed / total) * 100
        except Exception:
            return 0.0
    
    def _run_python_tests(self, code: str, test_cases: List[Dict]) -> int:
        """Run Python test cases"""
        passed = 0
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.write("\n\n# Test cases\n")
            for i, test in enumerate(test_cases):
                f.write(f"try:\n")
                f.write(f"    result = {test['function_call']}\n")
                f.write(f"    expected = {test['expected']}\n")
                f.write(f"    print(f'Test {i+1}: {{result == expected}}')\n")
                f.write(f"except Exception as e:\n")
                f.write(f"    print(f'Test {i+1}: False - {{e}}')\n")
            
            temp_file = f.name
        
        try:
            result = subprocess.run(['python', temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            for line in result.stdout.split('\n'):
                if 'True' in line:
                    passed += 1
        finally:
            os.unlink(temp_file)
        
        return passed
    
    def _evaluate_code_quality(self, code: str, language: Language) -> float:
        """Evaluate code quality using static analysis"""
        score = 100.0
        
        if language == Language.PYTHON:
            try:
                tree = ast.parse(code)
                
                # Check for code smells
                analyzer = CodeQualityAnalyzer()
                issues = analyzer.analyze(tree, code)
                
                # Deduct points for issues
                score -= len(issues) * 5
                
            except SyntaxError:
                score = 0.0
        
        return max(0.0, min(100.0, score))
    
    def _evaluate_efficiency(self, code: str, language: Language) -> float:
        """Evaluate algorithmic efficiency"""
        efficiency_analyzer = EfficiencyAnalyzer()
        return efficiency_analyzer.analyze(code, language)
    
    def _evaluate_readability(self, code: str, language: Language) -> float:
        """Evaluate code readability"""
        readability_analyzer = ReadabilityAnalyzer()
        return readability_analyzer.analyze(code, language)
    
    def _evaluate_edge_cases(self, code: str, test_cases: List[Dict], language: Language) -> float:
        """Evaluate edge case handling"""
        edge_case_analyzer = EdgeCaseAnalyzer()
        return edge_case_analyzer.analyze(code, test_cases, language)
    
    def _generate_ai_feedback(self, code: str, problem_description: str, 
                            correctness: float, quality: float, efficiency: float, 
                            readability: float, edge_cases: float) -> Tuple[Dict, List[str], List[str]]:
        """Generate detailed feedback using AI"""
        
        if not self.openai_api_key:
            return self._generate_basic_feedback(correctness, quality, efficiency, readability, edge_cases)
        
        prompt = f"""
        Analyze this code submission and provide detailed feedback:
        
        Problem Description: {problem_description}
        
        Code:
        ```
        {code}
        ```
        
        Current Scores:
        - Correctness: {correctness}/100
        - Quality: {quality}/100
        - Efficiency: {efficiency}/100
        - Readability: {readability}/100
        - Edge Cases: {edge_cases}/100
        
        Provide:
        1. Specific feedback for each category
        2. Actionable suggestions for improvement
        3. Strengths of the current solution
        
        Format as JSON with keys: feedback, suggestions, strengths
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('feedback', {}), result.get('suggestions', []), result.get('strengths', [])
        except:
            return self._generate_basic_feedback(correctness, quality, efficiency, readability, edge_cases)
    
    def _generate_basic_feedback(self, correctness: float, quality: float, 
                               efficiency: float, readability: float, edge_cases: float) -> Tuple[Dict, List[str], List[str]]:
        """Generate basic feedback without AI"""
        feedback = {
            "correctness": ["Code passes most test cases"] if correctness > 70 else ["Code fails several test cases"],
            "quality": ["Good code structure"] if quality > 70 else ["Code quality needs improvement"],
            "efficiency": ["Acceptable performance"] if efficiency > 70 else ["Algorithm could be more efficient"],
            "readability": ["Code is readable"] if readability > 70 else ["Code readability could be improved"],
            "edge_cases": ["Handles edge cases well"] if edge_cases > 70 else ["Edge case handling needs work"]
        }
        
        suggestions = [
            "Add more comments to explain complex logic",
            "Consider using more descriptive variable names",
            "Review algorithm complexity for optimization opportunities"
        ]
        
        strengths = [
            "Code compiles and runs successfully",
            "Basic functionality is implemented"
        ]
        
        return feedback, suggestions, strengths

class CodeQualityAnalyzer:
    def analyze(self, tree: ast.AST, code: str) -> List[str]:
        """Analyze code quality issues"""
        issues = []
        
        # Check for long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.end_lineno - node.lineno > 50:
                    issues.append(f"Function '{node.name}' is too long ({node.end_lineno - node.lineno} lines)")
        
        # Check for magic numbers
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in [0, 1, -1] and node.value > 10:
                    issues.append("Magic number found - consider using named constants")
        
        # Check for deep nesting
        max_depth = self._calculate_max_depth(tree)
        if max_depth > 4:
            issues.append(f"Code has deep nesting (depth: {max_depth})")
        
        return issues
    
    def _calculate_max_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth"""
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            current_depth += 1
        
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            child_depth = self._calculate_max_depth(child, current_depth)
            max_depth = max(max_depth, child_depth)
        
        return max_depth

class EfficiencyAnalyzer:
    def analyze(self, code: str, language: Language) -> float:
        """Analyze algorithmic efficiency"""
        score = 85.0  # Base score
        
        # Check for common inefficient patterns
        if language == Language.PYTHON:
            # Nested loops
            nested_loops = code.count('for ') * code.count('while ')
            if nested_loops > 2:
                score -= 15
            
            # Inefficient string concatenation
            if '+=' in code and 'str' in code:
                score -= 10
            
            # List operations in loops
            if 'append' in code and 'for ' in code:
                lines = code.split('\n')
                for i, line in enumerate(lines):
                    if 'for ' in line:
                        for j in range(i+1, min(i+10, len(lines))):
                            if 'append' in lines[j]:
                                score -= 5
                                break
        
        return max(0.0, min(100.0, score))

class ReadabilityAnalyzer:
    def analyze(self, code: str, language: Language) -> float:
        """Analyze code readability"""
        score = 100.0
        lines = code.split('\n')
        
        # Check line length
        long_lines = sum(1 for line in lines if len(line) > 100)
        score -= long_lines * 2
        
        # Check for comments
        comment_ratio = sum(1 for line in lines if line.strip().startswith('#')) / max(len(lines), 1)
        if comment_ratio < 0.1:
            score -= 10
        
        # Check variable naming
        if language == Language.PYTHON:
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        if len(node.id) == 1 and node.id not in ['i', 'j', 'k', 'x', 'y', 'z']:
                            score -= 2
            except:
                pass
        
        return max(0.0, min(100.0, score))

class EdgeCaseAnalyzer:
    def analyze(self, code: str, test_cases: List[Dict], language: Language) -> float:
        """Analyze edge case handling"""
        score = 75.0  # Base score
        
        # Check for input validation
        if 'if ' in code and any(keyword in code for keyword in ['None', 'null', 'empty', 'len(']):
            score += 15
        
        # Check for exception handling
        if 'try' in code and 'except' in code:
            score += 10
        
        # Check boundary conditions
        if any(op in code for op in ['>=', '<=', '==', '!=']):
            score += 5
        
        return min(100.0, score)

# Web Interface (Flask)
from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_code():
    try:
        data = request.get_json()
        
        evaluator = CodingEvaluator(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            github_token=os.getenv('GITHUB_TOKEN')
        )
        
        result = evaluator.evaluate_submission(
            code_input=data['code'],
            problem_description=data.get('problem_description', ''),
            test_cases=data.get('test_cases', []),
            language=Language(data.get('language', 'python'))
        )
        
        return jsonify({
            'success': True,
            'result': {
                'overall_score': result.overall_score,
                'correctness_score': result.correctness_score,
                'quality_score': result.quality_score,
                'efficiency_score': result.efficiency_score,
                'readability_score': result.readability_score,
                'edge_cases_score': result.edge_cases_score,
                'feedback': result.feedback,
                'suggestions': result.suggestions,
                'strengths': result.strengths
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    temp_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(temp_path)
    
    try:
        with open(temp_path, 'r') as f:
            code = f.read()
        
        return jsonify({
            'success': True,
            'code': code,
            'filename': file.filename
        })
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True)
