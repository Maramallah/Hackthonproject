from flask import Flask, request, jsonify, render_template_string
import re
import json
from datetime import datetime
import math

app = Flask(__name__)

# Mock NLP model for symptom analysis
class SymptomAnalyzer:
    def __init__(self):
        # Keywords for different severity levels
        self.critical_keywords = [
            'fire', 'smoke', 'burning', 'explosion', 'electric shock', 'gas leak',
            'brake failure', 'steering failure', 'engine failure', 'overheating badly'
        ]
        
        self.professional_keywords = [
            'engine noise', 'transmission', 'electrical', 'wiring', 'motor replacement',
            'compressor', 'refrigerant', 'heating element', 'control board', 'pump failure'
        ]
        
        self.simple_keywords = [
            'clogged', 'dirty', 'filter', 'loose', 'minor leak', 'squeaking',
            'slow', 'stuck', 'calibration', 'reset needed'
        ]
    
    def analyze_symptoms(self, symptoms, machine_type):
        symptoms_lower = symptoms.lower()
        
        # Check for critical issues
        for keyword in self.critical_keywords:
            if keyword in symptoms_lower:
                return {
                    'severity': 'critical',
                    'needs_professional': True,
                    'urgency': 'immediate',
                    'confidence': 0.9
                }
        
        # Check for professional-level issues
        for keyword in self.professional_keywords:
            if keyword in symptoms_lower:
                return {
                    'severity': 'professional',
                    'needs_professional': True,
                    'urgency': 'within_24h',
                    'confidence': 0.8
                }
        
        # Check for simple issues
        for keyword in self.simple_keywords:
            if keyword in symptoms_lower:
                return {
                    'severity': 'simple',
                    'needs_professional': False,
                    'urgency': 'when_convenient',
                    'confidence': 0.7
                }
        
        # Default classification
        return {
            'severity': 'unknown',
            'needs_professional': True,
            'urgency': 'assessment_needed',
            'confidence': 0.5
        }

# Mock price prediction model
class PricePredictorML:
    def __init__(self):
        # Base prices for different machine types and severity levels
        self.price_matrix = {
            'car': {
                'simple': {'min': 50, 'max': 200},
                'professional': {'min': 200, 'max': 800},
                'critical': {'min': 500, 'max': 2000}
            },
            'washing_machine': {
                'simple': {'min': 30, 'max': 100},
                'professional': {'min': 100, 'max': 400},
                'critical': {'min': 300, 'max': 800}
            },
            'refrigerator': {
                'simple': {'min': 40, 'max': 120},
                'professional': {'min': 120, 'max': 500},
                'critical': {'min': 400, 'max': 1000}
            },
            'dishwasher': {
                'simple': {'min': 35, 'max': 110},
                'professional': {'min': 110, 'max': 350},
                'critical': {'min': 250, 'max': 700}
            }
        }
    
    def predict_price(self, machine_type, severity, symptoms):
        if machine_type not in self.price_matrix:
            machine_type = 'car'  # default
            
        if severity not in self.price_matrix[machine_type]:
            severity = 'professional'  # default
            
        price_range = self.price_matrix[machine_type][severity]
        
        # Add some variation based on symptoms length (more details = potentially more complex)
        complexity_factor = min(1.2, 0.8 + len(symptoms) / 500)
        
        min_price = int(price_range['min'] * complexity_factor)
        max_price = int(price_range['max'] * complexity_factor)
        
        return {
            'estimated_min': min_price,
            'estimated_max': max_price,
            'currency': 'USD'
        }

# Mock worker database
class WorkerDatabase:
    def __init__(self):
        self.workers = [
            {
                'id': 1, 'name': 'John Smith', 'specialties': ['car', 'motorcycle'],
                'rating': 4.8, 'reviews': 120, 'distance': 2.3,
                'phone': '+1-555-0101', 'available': True
            },
            {
                'id': 2, 'name': 'Sarah Johnson', 'specialties': ['washing_machine', 'dishwasher', 'refrigerator'],
                'rating': 4.9, 'reviews': 87, 'distance': 1.8,
                'phone': '+1-555-0102', 'available': True
            },
            {
                'id': 3, 'name': 'Mike Wilson', 'specialties': ['car', 'truck'],
                'rating': 4.6, 'reviews': 203, 'distance': 3.1,
                'phone': '+1-555-0103', 'available': True
            },
            {
                'id': 4, 'name': 'Lisa Brown', 'specialties': ['refrigerator', 'washing_machine', 'dryer'],
                'rating': 4.7, 'reviews': 95, 'distance': 2.7,
                'phone': '+1-555-0104', 'available': False
            },
            {
                'id': 5, 'name': 'David Garcia', 'specialties': ['car', 'washing_machine', 'dishwasher'],
                'rating': 4.5, 'reviews': 156, 'distance': 4.2,
                'phone': '+1-555-0105', 'available': True
            }
        ]
    
    def find_workers(self, machine_type, user_location, max_distance=10):
        suitable_workers = []
        
        for worker in self.workers:
            if (machine_type in worker['specialties'] and 
                worker['distance'] <= max_distance and 
                worker['available']):
                suitable_workers.append(worker)
        
        # Sort by rating (descending) then by distance (ascending)
        suitable_workers.sort(key=lambda x: (-x['rating'], x['distance']))
        
        return suitable_workers[:5]  # Return top 5 workers

# Initialize components
symptom_analyzer = SymptomAnalyzer()
price_predictor = PricePredictorML()
worker_db = WorkerDatabase()

# Solution recommendations
def get_solution_recommendations(severity, machine_type, symptoms):
    if severity == 'simple':
        solutions = {
            'car': [
                'Check and replace air filter if dirty',
                'Check fluid levels (oil, coolant, brake fluid)',
                'Inspect and clean battery terminals',
                'Check tire pressure and condition'
            ],
            'washing_machine': [
                'Clean the lint filter and drain hose',
                'Check if the machine is level',
                'Clean detergent dispenser',
                'Run a cleaning cycle with vinegar'
            ],
            'refrigerator': [
                'Clean condenser coils',
                'Check and adjust temperature settings',
                'Clean door seals and check for leaks',
                'Defrost if ice buildup is present'
            ],
            'dishwasher': [
                'Clean the filter at the bottom',
                'Check spray arms for clogs',
                'Run empty cycle with dishwasher cleaner',
                'Check door seals for debris'
            ]
        }
        return solutions.get(machine_type, ['Contact a professional for proper diagnosis'])
    else:
        return ['Professional diagnosis and repair recommended', 'Do not attempt DIY repairs for safety reasons']

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Repair Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6; color: #333; background: #f4f4f4;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input, select, textarea { 
            width: 100%; padding: 12px; border: 1px solid #ddd; 
            border-radius: 5px; font-size: 16px;
        }
        textarea { resize: vertical; min-height: 120px; }
        button { 
            background: #007bff; color: white; padding: 15px 30px; 
            border: none; border-radius: 5px; cursor: pointer; 
            font-size: 16px; width: 100%; margin-top: 10px;
        }
        button:hover { background: #0056b3; }
        .results { 
            margin-top: 30px; padding: 20px; background: white; 
            border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            display: none;
        }
        .severity { 
            padding: 10px; border-radius: 5px; margin-bottom: 15px; 
            font-weight: bold; text-align: center;
        }
        .critical { background: #ffebee; color: #c62828; }
        .professional { background: #fff3e0; color: #ef6c00; }
        .simple { background: #e8f5e8; color: #2e7d32; }
        .unknown { background: #f5f5f5; color: #666; }
        .worker { 
            border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; 
            border-radius: 5px; background: #fafafa;
        }
        .worker-rating { color: #ffa000; font-weight: bold; }
        .loading { text-align: center; color: #666; }
        ul { padding-left: 20px; }
        .price-estimate { 
            background: #e3f2fd; padding: 15px; border-radius: 5px; 
            margin: 15px 0; font-size: 18px; font-weight: bold; 
            text-align: center; color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Smart Repair Assistant</h1>
            <p>Describe your machine problems and get instant analysis, pricing, and repair recommendations</p>
        </div>
        
        <form id="symptomForm">
            <div class="form-group">
                <label for="machine_type">Machine Type:</label>
                <select id="machine_type" name="machine_type" required>
                    <option value="">Select machine type</option>
                    <option value="car">Car</option>
                    <option value="washing_machine">Washing Machine</option>
                    <option value="refrigerator">Refrigerator</option>
                    <option value="dishwasher">Dishwasher</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="symptoms">Describe the Problem:</label>
                <textarea id="symptoms" name="symptoms" 
                    placeholder="Describe what's wrong with your machine. Include details like sounds, smells, error messages, when the problem occurs, etc."
                    required></textarea>
            </div>
            
            <div class="form-group">
                <label for="location">Your Location (City, State):</label>
                <input type="text" id="location" name="location" 
                    placeholder="e.g., San Francisco, CA" required>
            </div>
            
            <button type="submit">Analyze Problem</button>
        </form>
        
        <div id="results" class="results">
            <div id="loading" class="loading">Analyzing your problem...</div>
            <div id="analysis-results" style="display: none;"></div>
        </div>
    </div>

    <script>
        document.getElementById('symptomForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const results = document.getElementById('results');
            const loading = document.getElementById('loading');
            const analysisResults = document.getElementById('analysis-results');
            
            results.style.display = 'block';
            loading.style.display = 'block';
            analysisResults.style.display = 'none';
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.style.display = 'none';
                analysisResults.style.display = 'block';
                analysisResults.innerHTML = formatResults(data);
                
            } catch (error) {
                loading.style.display = 'none';
                analysisResults.style.display = 'block';
                analysisResults.innerHTML = '<p style="color: red;">Error analyzing problem. Please try again.</p>';
            }
        });
        
        function formatResults(data) {
            let html = '';
            
            // Severity assessment
            html += `<div class="severity ${data.analysis.severity}">
                Severity Level: ${data.analysis.severity.toUpperCase()}
                ${data.analysis.needs_professional ? '(Professional Help Needed)' : '(DIY Possible)'}
                <br>Urgency: ${data.analysis.urgency.replace('_', ' ')}
                <br>Confidence: ${Math.round(data.analysis.confidence * 100)}%
            </div>`;
            
            // Price estimate
            if (data.price_estimate) {
                html += `<div class="price-estimate">
                    💰 Estimated Repair Cost: $${data.price_estimate.estimated_min} - $${data.price_estimate.estimated_max}
                </div>`;
            }
            
            // Solutions
            if (data.solutions && data.solutions.length > 0) {
                html += '<h3>🛠️ Recommended Solutions:</h3><ul>';
                data.solutions.forEach(solution => {
                    html += `<li>${solution}</li>`;
                });
                html += '</ul>';
            }
            
            // Workers
            if (data.workers && data.workers.length > 0) {
                html += '<h3>👨‍🔧 Recommended Repair Technicians Near You:</h3>';
                data.workers.forEach(worker => {
                    html += `<div class="worker">
                        <strong>${worker.name}</strong>
                        <span class="worker-rating">⭐ ${worker.rating} (${worker.reviews} reviews)</span>
                        <br>Specialties: ${worker.specialties.join(', ')}
                        <br>Distance: ${worker.distance} miles
                        <br>Phone: ${worker.phone}
                    </div>`;
                });
            } else if (data.analysis.needs_professional) {
                html += '<p>No local technicians found in our database. Please search for repair services in your area.</p>';
            }
            
            return html;
        }
    </script>
</body>
</html>
    ''')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    try:
        machine_type = request.form.get('machine_type', '').lower()
        symptoms = request.form.get('symptoms', '')
        location = request.form.get('location', '')
        
        if not all([machine_type, symptoms, location]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Analyze symptoms using NLP model
        analysis = symptom_analyzer.analyze_symptoms(symptoms, machine_type)
        
        # Predict price using ML model
        price_estimate = price_predictor.predict_price(machine_type, analysis['severity'], symptoms)
        
        # Get solution recommendations
        solutions = get_solution_recommendations(analysis['severity'], machine_type, symptoms)
        
        # Find nearby workers if professional help is needed
        workers = []
        if analysis['needs_professional']:
            workers = worker_db.find_workers(machine_type, location)
        
        response = {
            'analysis': analysis,
            'price_estimate': price_estimate,
            'solutions': solutions,
            'workers': workers,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/workers/<machine_type>')
def get_workers_by_type(machine_type):
    """API endpoint to get workers by machine type"""
    location = request.args.get('location', '')
    max_distance = float(request.args.get('max_distance', 10))
    
    workers = worker_db.find_workers(machine_type, location, max_distance)
    return jsonify(workers)

@app.route('/api/price-estimate')
def get_price_estimate():
    """API endpoint for price estimation"""
    machine_type = request.args.get('machine_type', '')
    severity = request.args.get('severity', 'professional')
    symptoms = request.args.get('symptoms', '')
    
    if not machine_type:
        return jsonify({'error': 'Machine type is required'}), 400
    
    estimate = price_predictor.predict_price(machine_type, severity, symptoms)
    return jsonify(estimate)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)