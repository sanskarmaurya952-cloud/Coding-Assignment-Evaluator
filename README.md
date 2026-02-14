# 🤖 AI-Powered Coding Assignment Evaluator

> **Automated. Fair. Explainable. Scalable.**  
> An intelligent system that evaluates code submissions beyond just correctness — assessing quality, efficiency, readability, and providing constructive, human-readable feedback at scale.

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Evaluation Dimensions](#-evaluation-dimensions)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Feedback Report Format](#-feedback-report-format)
- [Use Cases](#-use-cases)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚨 Problem Statement

The current state of coding assessments — in classrooms, bootcamps, and technical hiring — is fundamentally broken in five key ways:

| Problem | Impact |
|---|---|
| ⏳ **Delayed Feedback** | Manual evaluation slows learning and iteration cycles |
| 📊 **Surface-Level Scoring** | Most systems only check test case pass/fail, ignoring code quality and design |
| 🔍 **Lack of Explainability** | Candidates don't understand *why* their solution was weak or strong |
| 📈 **Scalability Issues** | Instructors and recruiters can't deeply review hundreds of submissions |
| ⚖️ **Unfair Evaluation** | Different evaluators apply inconsistent, subjective standards |

---

## 💡 Solution Overview

The **AI-Powered Coding Assignment Evaluator** is an intelligent evaluation pipeline that automatically analyzes code submissions along multiple quality dimensions — not just correctness — and generates clear, constructive, and consistent feedback for every learner, every time.

```
Student Submits Code
        │
        ▼
┌─────────────────────┐
│   Submission Layer   │  ← Accepts code via API, web UI, or LMS integration
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Static Analysis     │  ← Syntax, complexity, style checks (AST-based)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Dynamic Execution   │  ← Test case runner + edge case detection (sandboxed)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  AI Evaluation Layer │  ← LLM-powered deep analysis (quality, design, patterns)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Feedback Generator  │  ← Structured, human-readable, constructive report
└────────┬────────────┘
         │
         ▼
   Instructor Dashboard / Student Portal / LMS
```

---

## ✨ Key Features

### 🎯 Multi-Dimensional Evaluation
Goes far beyond pass/fail — evaluates code quality, algorithmic efficiency, readability, design patterns, and edge case handling.

### 🧠 AI-Powered Code Understanding
Uses large language models to understand *intent*, not just execution. Identifies anti-patterns, over-engineering, and missed opportunities — just like an experienced code reviewer would.

### 📝 Constructive Feedback Generation
Every submission receives a detailed, empathetic report explaining what was done well, what needs improvement, and *how* to improve it — with code snippets and suggestions.

### ⚖️ Consistent & Bias-Free Scoring
Rubric-based AI evaluation ensures every student or candidate is measured against the same objective standard — eliminating evaluator fatigue and subjective bias.

### ⚡ Real-Time Results
Feedback is returned in seconds, not hours — enabling tight learning loops and rapid skill iteration.

### 📊 Instructor Analytics Dashboard
Aggregate insights across all submissions: class-wide weak areas, plagiarism detection, grade distributions, and individual progress tracking.

### 🔌 LMS & API Integration
REST API-first design integrates with Canvas, Moodle, Google Classroom, Gradescope, and custom hiring platforms.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                            │
│   Web UI  │  Mobile App  │  LMS Plugin  │  REST API / CLI     │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│                      API GATEWAY                               │
│          Auth  │  Rate Limiting  │  Request Routing            │
└──────────────────────────┬─────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────────┐
        │                  │                       │
┌───────▼──────┐  ┌────────▼────────┐  ┌──────────▼──────────┐
│  Submission  │  │  Execution      │  │  AI Evaluation      │
│  Service     │  │  Sandbox        │  │  Service            │
│              │  │  (Docker/WASM)  │  │  (LLM + Rubrics)    │
│ • File parse │  │ • Test runner   │  │ • Code quality      │
│ • Language   │  │ • Memory limits │  │ • Pattern detect    │
│   detection  │  │ • Time limits   │  │ • Feedback gen      │
│ • Queue mgmt │  │ • I/O capture   │  │ • Score aggregation │
└───────┬──────┘  └────────┬────────┘  └──────────┬──────────┘
        │                  │                       │
┌───────▼──────────────────▼───────────────────────▼──────────┐
│                     DATA LAYER                               │
│     PostgreSQL  │  Redis Cache  │  S3 (submissions/reports)  │
└──────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│                  REPORTING & ANALYTICS                         │
│    Instructor Dashboard  │  Student Portal  │  Export (PDF/CSV) │
└────────────────────────────────────────────────────────────────┘
```

---

## 📐 Evaluation Dimensions

Each submission is scored across **6 core dimensions**, each weighted within a configurable rubric:

### 1. ✅ Correctness (0–25 pts)
- Unit test pass rate
- Expected vs. actual output comparison
- Return value and type correctness
- Error handling (does it crash gracefully?)

### 2. ⚙️ Efficiency & Algorithmic Performance (0–20 pts)
- **Time Complexity**: Is the algorithm optimal? (O(n²) when O(n log n) is possible?)
- **Space Complexity**: Unnecessary memory usage? Memory leaks?
- **Runtime benchmarks**: Execution time against large inputs
- Comparison against baseline optimal solution

### 3. 📖 Code Readability (0–15 pts)
- Naming conventions (variables, functions, classes)
- Code formatting and indentation consistency
- Comment quality (are complex sections explained?)
- Function length and single-responsibility adherence
- Avoidance of "magic numbers" and ambiguous identifiers

### 4. 🏗️ Code Quality & Design (0–20 pts)
- Modularity and separation of concerns
- DRY (Don't Repeat Yourself) principle adherence
- SOLID principles (for OOP submissions)
- Detection of anti-patterns (God objects, deep nesting, spaghetti code)
- Appropriate use of data structures
- Error handling and input validation design

### 5. 🧩 Edge Case Handling (0–10 pts)
- Empty inputs / null values
- Boundary values (min/max, zero, negative numbers)
- Large inputs (performance under stress)
- Unexpected types or malformed data
- AI-generated edge case probing (beyond instructor-defined tests)

### 6. 💬 Code Clarity & Communication (0–10 pts)
- Logical flow and reasoning clarity
- Documentation completeness
- Consistent coding style
- Self-explanatory structure without over-commenting

```
┌────────────────────────────────────────────┐
│         FINAL SCORE BREAKDOWN              │
├──────────────────────────┬─────────────────┤
│ Correctness              │   /25           │
│ Efficiency               │   /20           │
│ Code Quality & Design    │   /20           │
│ Readability              │   /15           │
│ Edge Case Handling       │   /10           │
│ Clarity & Communication  │   /10           │
├──────────────────────────┼─────────────────┤
│ TOTAL                    │   /100          │
└──────────────────────────┴─────────────────┘
```

> 💡 **Instructors can customize rubric weights** per assignment — a systems design problem might weight efficiency higher, while a beginner exercise might weight correctness and readability most.

---

## 🔄 How It Works

### Step 1 — Submission Ingestion
Student submits code via the web UI, API, or LMS integration. The system auto-detects language (Python, JavaScript, Java, C++, Go, and more) and queues it for evaluation.

### Step 2 — Static Analysis
An AST (Abstract Syntax Tree) parser runs language-specific linting and complexity analysis without executing the code. Tools like ESLint, Pylint, Checkstyle, and Radon are used depending on the language.

### Step 3 — Sandboxed Execution
The code runs inside an isolated Docker container or WebAssembly sandbox with strict CPU, memory, and time limits. All instructor-defined test cases run, and additional AI-generated edge cases are automatically probed.

### Step 4 — AI Deep Analysis
The cleaned and anonymized code is sent to the AI evaluation layer. The LLM analyzes it against the rubric, identifies patterns, compares it to reference solutions (if provided), and generates nuanced observations about quality and design.

### Step 5 — Feedback Report Generation
A structured, detailed feedback report is assembled combining static analysis results, test outcomes, and AI observations into clear, actionable language tailored to the learner's level.

### Step 6 — Delivery & Storage
The report is delivered instantly to the student portal, logged in the instructor dashboard, and stored for longitudinal progress tracking.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend API** | Python (FastAPI) |
| **AI Evaluation** | Anthropic Claude API / OpenAI GPT-4 |
| **Static Analysis** | AST parsers, Pylint, ESLint, Radon, Checkstyle |
| **Code Execution** | Docker (sandboxed containers), Judge0 |
| **Database** | PostgreSQL (submissions, scores), Redis (queue/cache) |
| **File Storage** | AWS S3 / MinIO |
| **Frontend** | React + TypeScript |
| **Auth** | OAuth2 / JWT (with SSO support for LMS) |
| **Queue** | Celery + RabbitMQ |
| **Containerization** | Docker + Kubernetes |
| **Monitoring** | Prometheus + Grafana |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Node.js 18+
- An Anthropic or OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-code-evaluator.git
cd ai-code-evaluator
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# AI Provider
ANTHROPIC_API_KEY=your_api_key_here
AI_MODEL=claude-sonnet-4-5-20250929

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/evaluator_db
REDIS_URL=redis://localhost:6379

# Execution Sandbox
SANDBOX_TYPE=docker          # options: docker, wasm, judge0
JUDGE0_API_URL=              # only if using Judge0
MAX_EXECUTION_TIME_MS=10000
MAX_MEMORY_MB=256

# Storage
S3_BUCKET=code-submissions
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Security
SECRET_KEY=your_jwt_secret
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Launch with Docker Compose

```bash
docker-compose up --build
```

This starts:
- The FastAPI backend (`localhost:8000`)
- PostgreSQL database
- Redis instance
- Celery workers for async evaluation
- React frontend (`localhost:3000`)

### 4. Run Database Migrations

```bash
docker-compose exec api alembic upgrade head
```

### 5. Create Your First Assignment

```bash
curl -X POST http://localhost:8000/assignments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Two Sum Problem",
    "description": "Given an array of integers, return indices of two numbers that add to target.",
    "language": "python",
    "rubric": {
      "correctness_weight": 30,
      "efficiency_weight": 25,
      "quality_weight": 20,
      "readability_weight": 15,
      "edge_cases_weight": 10
    },
    "test_cases": [
      {"input": "[2, 7, 11, 15], 9", "expected_output": "[0, 1]"},
      {"input": "[3, 2, 4], 6", "expected_output": "[1, 2]"}
    ]
  }'
```

### 6. Submit Code for Evaluation

```bash
curl -X POST http://localhost:8000/submissions \
  -H "Authorization: Bearer STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignment_id": "asgn_123",
    "language": "python",
    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i"
  }'
```

---

## 📡 API Reference

### Authentication

All endpoints require a Bearer token obtained via `/auth/login`.

### Core Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Authenticate and get access token |
| `POST` | `/assignments` | Create a new assignment (instructor) |
| `GET` | `/assignments/{id}` | Get assignment details |
| `POST` | `/submissions` | Submit code for evaluation |
| `GET` | `/submissions/{id}` | Get submission + full feedback report |
| `GET` | `/submissions/{id}/status` | Poll evaluation status |
| `GET` | `/assignments/{id}/analytics` | Class-wide submission analytics |
| `GET` | `/students/{id}/progress` | Individual student progress over time |
| `POST` | `/assignments/{id}/rubric` | Update rubric weights |

### Example Response — Submission Feedback

```json
{
  "submission_id": "sub_abc123",
  "status": "completed",
  "evaluated_at": "2025-02-14T10:30:00Z",
  "scores": {
    "correctness": 24,
    "efficiency": 18,
    "code_quality": 16,
    "readability": 13,
    "edge_cases": 8,
    "clarity": 9,
    "total": 88
  },
  "grade": "B+",
  "test_results": {
    "passed": 9,
    "failed": 1,
    "total": 10,
    "failed_cases": [
      {
        "input": "[], 0",
        "expected": "[]",
        "actual": "IndexError: list index out of range"
      }
    ]
  },
  "feedback": {
    "summary": "Strong solution with an efficient hash map approach. Minor gaps in edge case handling and one naming convention issue.",
    "strengths": [
      "Excellent use of a hash map — O(n) time complexity is optimal for this problem.",
      "Clean, Pythonic code structure with good use of enumerate().",
      "Handles the core algorithm correctly across 9 out of 10 test cases."
    ],
    "improvements": [
      {
        "category": "Edge Cases",
        "severity": "medium",
        "description": "The function crashes on empty input lists. Add a guard clause at the top.",
        "suggestion": "if not nums: return []",
        "line_reference": 1
      },
      {
        "category": "Readability",
        "severity": "low",
        "description": "The variable name 'seen' is slightly ambiguous. Consider 'num_to_index' for clarity.",
        "suggestion": "num_to_index = {}  # Maps each number to its index",
        "line_reference": 2
      }
    ],
    "complexity_analysis": {
      "time": "O(n)",
      "space": "O(n)",
      "assessment": "Optimal. Well done for avoiding the O(n²) brute force approach."
    }
  }
}
```

---

## 📄 Feedback Report Format

Every student receives a report containing:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CODE EVALUATION REPORT
  Assignment: Two Sum Problem
  Submitted: Feb 14, 2025 at 10:30 AM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  OVERALL SCORE: 88 / 100   Grade: B+

  ┌────────────────────┬──────┬──────────┐
  │ Dimension          │Score │ Max      │
  ├────────────────────┼──────┼──────────┤
  │ Correctness        │  24  │   25     │
  │ Efficiency         │  18  │   20     │
  │ Code Quality       │  16  │   20     │
  │ Readability        │  13  │   15     │
  │ Edge Cases         │   8  │   10     │
  │ Clarity            │   9  │   10     │
  └────────────────────┴──────┴──────────┘

  TEST RESULTS: 9/10 passed

  ✅ WHAT YOU DID WELL
  ...

  📈 HOW TO IMPROVE
  ...

  🔍 COMPLEXITY ANALYSIS
  Time: O(n) — Optimal
  Space: O(n)

  💡 NEXT STEPS
  Try solving with the constraint of O(1) space.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎓 Use Cases

**University Courses**
Professors assign weekly coding problems and automatically receive graded submissions with AI-generated insights about common class-wide misconceptions.

**Coding Bootcamps**
Instructors track learner progress over time, identify students who need help, and deliver consistent feedback regardless of cohort size.

**Technical Recruitment**
Hiring teams evaluate hundreds of take-home coding challenges with consistent rubrics — removing evaluator fatigue and implicit bias from the process.

**Self-Directed Learning**
Learners submit personal practice problems and receive mentor-quality feedback at any time, without waiting for a human reviewer.

**Internal Developer Upskilling**
Engineering teams run internal coding challenges and assessments with fair, automated scoring to support career development programs.

---

## 🗺️ Roadmap

### Phase 1 — MVP (Current)
- [x] Multi-language submission support (Python, JavaScript, Java, C++)
- [x] Sandboxed code execution
- [x] AI-powered feedback generation
- [x] Instructor dashboard
- [x] REST API

### Phase 2 — Q2 2025
- [ ] Plagiarism and AI-written code detection
- [ ] GitHub / GitLab repository submission support
- [ ] Canvas and Moodle LMS plugins
- [ ] Customizable rubric templates
- [ ] Batch submission processing (ZIP upload)

### Phase 3 — Q3 2025
- [ ] Student learning path recommendations based on weak areas
- [ ] Multi-language support expansion (Go, Rust, Kotlin, Swift)
- [ ] Pair programming replay and annotation
- [ ] Real-time collaborative evaluation for panel reviews

### Phase 4 — Q4 2025
- [ ] Adaptive test case generation using AI
- [ ] Long-form project evaluation (multi-file submissions)
- [ ] Longitudinal skills analytics and competency tracking
- [ ] Enterprise SSO and audit trail compliance

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# Open a Pull Request
```

**Areas where we especially welcome help:**
- Adding support for new programming languages
- Improving rubric prompt engineering
- Writing test cases for the evaluator itself
- Accessibility improvements in the frontend
- Documentation and tutorials

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgements

- [Anthropic](https://anthropic.com) for the Claude API powering AI evaluation
- [Judge0](https://judge0.com) for the open-source code execution sandbox
- The open-source community behind AST parsing and static analysis tooling

---

<div align="center">

**Built to make learning faster, fairer, and more human — at any scale.**

[⭐ Star this repo](https://github.com/your-org/ai-code-evaluator) · [🐛 Report a Bug](https://github.com/your-org/ai-code-evaluator/issues) · [💡 Request a Feature](https://github.com/your-org/ai-code-evaluator/issues)

</div>
