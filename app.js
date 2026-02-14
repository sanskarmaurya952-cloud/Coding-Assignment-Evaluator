// static/app.js
let testCaseCount = 1;

document.getElementById('inputMethod').addEventListener('change', function() {
    const method = this.value;
    document.getElementById('directInput').style.display = method === 'direct' ? 'block' : 'none';
    document.getElementById('fileInput').style.display = method === 'file' ? 'block' : 'none';
    document.getElementById('githubInput').style.display = method === 'github' ? 'block' : 'none';
});

document.getElementById('codeFile').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('codeTextarea').value = data.code;
            } else {
                alert('Error uploading file: ' + data.error);
            }
        });
    }
});

function addTestCase() {
    const testCasesDiv = document.getElementById('testCases');
    const newTestCase = document.createElement('div');
    newTestCase.className = 'input-group mb-2';
    newTestCase.innerHTML = `
        <input type="text" class="form-control" placeholder="Function call" id="testCall${testCaseCount}">
        <input type="text" class="form-control" placeholder="Expected output" id="testExpected${testCaseCount}">
        <button type="button" class="btn btn-outline-danger" onclick="removeTestCase(this)">-</button>
    `;
    testCasesDiv.appendChild(newTestCase);
    testCaseCount++;
}

function removeTestCase(button) {
    button.parentElement.remove();
}

document.getElementById('evaluationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const method = document.getElementById('inputMethod').value;
    let code = '';
    
    if (method === 'direct') {
        code = document.getElementById('codeTextarea').value;
    } else if (method === 'github') {
        code = document.getElementById('githubUrl').value;
    } else if (method === 'file') {
        code = document.getElementById('codeTextarea').value; // Already loaded from file
    }
    
    if (!code.trim()) {
        alert('Please provide code to evaluate');
        return;
    }
    
    // Collect test cases
    const testCases = [];
    for (let i = 0; i < testCaseCount; i++) {
        const callElement = document.getElementById(`testCall${i}`);
        const expectedElement = document.getElementById(`testExpected${i}`);
        
        if (callElement && expectedElement && callElement.value && expectedElement.value) {
            testCases.push({
                function_call: callElement.value,
                expected: expectedElement.value
            });
        }
    }
    
    const data = {
        code: code,
        language: document.getElementById('language').value,
        problem_description: document.getElementById('problemDescription').value,
        test_cases: testCases
    };
    
    // Show loading
    document.getElementById('results').innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Evaluating...</span></div>';
    
    fetch('/api/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data.result);
        } else {
            document.getElementById('results').innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
        }
    })
    .catch(error => {
        document.getElementById('results').innerHTML = `<div class="alert alert-danger">Error: ${error}</div>`;
    });
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    
    resultsDiv.innerHTML = `
        <div class="mb-4">
            <h4>Overall Score: ${result.overall_score}/100</h4>
            <div class="progress mb-3">
                <div class="progress-bar ${getScoreColor(result.overall_score)}" style="width: ${result.overall_score}%"></div>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-6">
                <h6>Correctness: ${result.correctness_score}/100</h6>
                <div class="progress mb-2">
                    <div class="progress-bar ${getScoreColor(result.correctness_score)}" style="width: ${result.correctness_score}%"></div>
                </div>
            </div>
            <div class="col-6">
                <h6>Code Quality: ${result.quality_score}/100</h6>
                <div class="progress mb-2">
                    <div class="progress-bar ${getScoreColor(result.quality_score)}" style="width: ${result.quality_score}%"></div>
                </div>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-6">
                <h6>Efficiency: ${result.efficiency_score}/100</h6>
                <div class="progress mb-2">
                    <div class="progress-bar ${getScoreColor(result.efficiency_score)}" style="width: ${result.efficiency_score}%"></div>
                </div>
            </div>
            <div class="col-6">
                <h6>Readability: ${result.readability_score}/100</h6>
                <div class="progress mb-2">
                    <div class="progress-bar ${getScoreColor(result.readability_score)}" style="width: ${result.readability_score}%"></div>
                </div>
            </div>
        </div>
        
        <div class="mb-4">
            <h6>Edge Cases: ${result.edge_cases_score}/100</h6>
            <div class="progress mb-2">
                <div class="progress-bar ${getScoreColor(result.edge_cases_score)}" style="width: ${result.edge_cases_score}%"></div>
            </div>
        </div>
        
        <div class="accordion" id="feedbackAccordion">
            <div class="accordion-item">
                <h2 class="accordion-header" id="strengthsHeader">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#strengthsCollapse">
                        Strengths
                    </button>
                </h2>
                <div id="strengthsCollapse" class="accordion-collapse collapse show" data-bs-parent="#feedbackAccordion">
                    <div class="accordion-body">
                        <ul class="list-group list-group-flush">
                            ${result.strengths.map(strength => `<li class="list-group-item text-success">✓ ${strength}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="accordion-item">
                <h2 class="accordion-header" id="suggestionsHeader">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#suggestionsCollapse">
                        Suggestions for Improvement
                    </button>
                </h2>
                <div id="suggestionsCollapse" class="accordion-collapse collapse" data-bs-parent="#feedbackAccordion">
                    <div class="accordion-body">
                        <ul class="list-group list-group-flush">
                            ${result.suggestions.map(suggestion => `<li class="list-group-item text-warning">⚠ ${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="accordion-item">
                <h2 class="accordion-header" id="detailedHeader">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#detailedCollapse">
                        Detailed Feedback
                    </button>
                </h2>
                <div id="detailedCollapse" class="accordion-collapse collapse" data-bs-parent="#feedbackAccordion">
                    <div class="accordion-body">
                        ${Object.entries(result.feedback).map(([category, items]) => `
                            <h6 class="text-capitalize">${category}</h6>
                            <ul class="list-group list-group-flush mb-3">
                                ${items.map(item => `<li class="list-group-item">${item}</li>`).join('')}
                            </ul>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function getScoreColor(score) {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-warning';
    return 'bg-danger';
}
