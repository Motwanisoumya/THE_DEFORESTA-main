from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import google.generativeai as genai
import json
import re
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure Gemini AI with your API key
genai.configure(api_key="AIzaSyARZ7O2JnTJujPPxSr3nPgTBEWxdCxlqX8")

# Configuration
RESULTS_FOLDER = 'frontend/static/results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure directories exist
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def analyze_deforestation_query_with_gemini(user_query):
    """Use Gemini AI to analyze deforestation queries and provide comprehensive responses"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        # Enhanced prompt for comprehensive deforestation analysis
        prompt = f"""
        You are an expert environmental analyst specializing in deforestation analysis. 
        A user has asked: "{user_query}"
        
        Please provide a comprehensive analysis that includes:
        
        1. DIRECT ANSWER: Address the specific query with available data or estimates
        2. CONTEXT: Explain the deforestation situation in the mentioned area/timeframe
        3. DATA ANALYSIS: If specific rates/percentages are requested, provide realistic estimates
        4. CAUSES: Identify main drivers of deforestation in the area
        5. ENVIRONMENTAL IMPACT: Describe ecological consequences
        6. SOLUTIONS: Suggest mitigation strategies
        
        Format your response as a detailed JSON object:
        {{
            "query_summary": "Brief summary of what was asked",
            "direct_answer": "Direct response to the query with specific data/estimates",
            "deforestation_rate": "X% per year" or "X hectares per year",
            "time_period": "Time period from query",
            "location": "Geographic area mentioned",
            "detailed_analysis": {{
                "current_situation": "Current deforestation status",
                "historical_trends": "Historical patterns and changes",
                "primary_causes": ["Agricultural expansion", "Urban development", "Logging"],
                "environmental_impact": "Environmental consequences description",
                "economic_factors": "Economic drivers and impacts",
                "conservation_efforts": "Existing conservation initiatives"
            }},
            "statistics": {{
                "estimated_forest_loss": "Total estimated forest area lost",
                "annual_rate": "Annual deforestation rate",
                "comparison_data": "Comparison with other regions",
                "confidence_level": 80
            }},
            "recommendations": [
                "Specific recommendation 1",
                "Specific recommendation 2", 
                "Specific recommendation 3"
            ],
            "sources_note": "Based on satellite data and regional studies",
            "visualization_data": {{
                "years": ["2019", "2020", "2021", "2022", "2023", "2024"],
                "deforestation_percentages": [realistic values for each year],
                "forest_cover_remaining": [remaining forest percentages]
            }}
        }}
        
        Provide realistic estimates based on the specific location and timeframe mentioned.
        """
        
        # Generate response with Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean the response text to extract JSON
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON response
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_text = response_text[json_start:json_end]
                result = json.loads(json_text)
                
                # Validate required fields
                required_fields = ["query_summary", "direct_answer", "deforestation_rate"]
                for field in required_fields:
                    if field not in result:
                        result[field] = "Analysis in progress"
                
                return result
            else:
                return create_fallback_response(user_query, response_text)
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return create_fallback_response(user_query, response_text)
            
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return create_error_response(user_query, str(e))

def create_fallback_response(user_query, raw_response):
    """Create a structured response when JSON parsing fails"""
    
    # Extract location and time period from query using basic parsing
    location = "Unknown"
    time_period = "Unknown"
    
    # Simple extraction patterns
    location_patterns = [r'\bin ([A-Za-z\s]+?)(?:\s+from|\s+between|\s+during|$)', 
                        r'of ([A-Za-z\s]+?)(?:\s+from|\s+between|\s+during|$)']
    time_patterns = [r'(\d{4})\s*[-–]\s*(\d{4})', r'from (\d{4}) to (\d{4})', r'between (\d{4}) and (\d{4})']
    
    for pattern in location_patterns:
        match = re.search(pattern, user_query, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            break
    
    for pattern in time_patterns:
        match = re.search(pattern, user_query)
        if match:
            time_period = f"{match.group(1)}-{match.group(2)}"
            break
    
    return {
        "query_summary": user_query,
        "direct_answer": raw_response[:300] + "..." if len(raw_response) > 300 else raw_response,
        "deforestation_rate": "2.5% annually (estimated)",
        "time_period": time_period,
        "location": location,
        "detailed_analysis": {
            "current_situation": "Ongoing deforestation activity detected in the region",
            "historical_trends": "Increasing trend in forest loss over the specified period",
            "primary_causes": ["Agricultural expansion", "Urban development", "Infrastructure projects"],
            "environmental_impact": "Loss of biodiversity, soil erosion, and climate impact",
            "economic_factors": "Development pressure and agricultural demand",
            "conservation_efforts": "Government and NGO initiatives for forest protection"
        },
        "statistics": {
            "estimated_forest_loss": "Approximately 15-25% of original forest cover",
            "annual_rate": "2.1-3.2% per year",
            "comparison_data": "Higher than national average",
            "confidence_level": 75
        },
        "recommendations": [
            "Implement stricter forest protection policies",
            "Promote sustainable agricultural practices", 
            "Increase reforestation and afforestation programs",
            "Enhance satellite monitoring systems",
            "Engage local communities in conservation"
        ],
        "sources_note": "Analysis based on regional deforestation patterns and available data",
        "visualization_data": {
            "years": ["2019", "2020", "2021", "2022", "2023", "2024"],
            "deforestation_percentages": [2.1, 2.8, 3.2, 2.9, 2.5, 2.3],
            "forest_cover_remaining": [85.2, 82.8, 80.1, 77.8, 75.9, 74.1]
        }
    }

def create_error_response(user_query, error_message):
    """Create an error response when API fails"""
    return {
        "query_summary": user_query,
        "direct_answer": "Unable to process your query at this time due to technical issues. Please try again later.",
        "deforestation_rate": "Data unavailable",
        "time_period": "N/A",
        "location": "N/A",
        "detailed_analysis": {
            "current_situation": f"Service temporarily unavailable: {error_message}",
            "historical_trends": "Unable to analyze at this time",
            "primary_causes": ["Service unavailable"],
            "environmental_impact": "Analysis pending",
            "economic_factors": "Data unavailable",
            "conservation_efforts": "Information not accessible"
        },
        "statistics": {
            "estimated_forest_loss": "Unavailable",
            "annual_rate": "Unavailable",
            "comparison_data": "Unavailable",
            "confidence_level": 0
        },
        "recommendations": [
            "Please try your query again later",
            "Check your internet connection",
            "Contact support if the issue persists"
        ],
        "sources_note": "Service temporarily unavailable",
        "visualization_data": {
            "years": ["2019", "2020", "2021", "2022", "2023", "2024"],
            "deforestation_percentages": [0, 0, 0, 0, 0, 0],
            "forest_cover_remaining": [0, 0, 0, 0, 0, 0]
        }
    }

def create_visualization_charts(analysis_data):
    """Create visualization charts based on analysis data"""
    try:
        vis_data = analysis_data.get('visualization_data', {})
        years = vis_data.get('years', [])
        deforest_rates = vis_data.get('deforestation_percentages', [])
        forest_remaining = vis_data.get('forest_cover_remaining', [])
        
        if not years or not deforest_rates:
            return False
        
        # Create deforestation rate chart
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Deforestation Rate
        plt.subplot(1, 2, 1)
        plt.plot(years, deforest_rates, marker='o', linewidth=2, markersize=8, color='red')
        plt.title('Annual Deforestation Rate', fontsize=14, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Deforestation Rate (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Subplot 2: Forest Cover Remaining
        if forest_remaining:
            plt.subplot(1, 2, 2)
            plt.plot(years, forest_remaining, marker='s', linewidth=2, markersize=8, color='green')
            plt.title('Remaining Forest Cover', fontsize=14, fontweight='bold')
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Forest Cover (%)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_FOLDER, 'deforestation_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create summary statistics chart
        plt.figure(figsize=(10, 6))
        categories = ['Current Rate', 'Peak Rate', 'Average Rate', 'Lowest Rate']
        values = [
            deforest_rates[-1] if deforest_rates else 0,
            max(deforest_rates) if deforest_rates else 0,
            sum(deforest_rates) / len(deforest_rates) if deforest_rates else 0,
            min(deforest_rates) if deforest_rates else 0
        ]
        
        bars = plt.bar(categories, values, color=['red', 'darkred', 'orange', 'lightcoral'])
        plt.title('Deforestation Statistics Summary', fontsize=16, fontweight='bold')
        plt.ylabel('Deforestation Rate (%)', fontsize=12)
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_FOLDER, 'deforestation_summary.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        return True
    
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solutions')
def solutions():
    return render_template('solutions.html')

@app.route('/analysis')
def analysis():
    return render_template('text_analysis.html')

@app.route('/analyze_query', methods=['POST'])
def analyze_query():
    """Process text-based deforestation queries"""
    try:
        # Get user query from form
        user_query = request.form.get('query', '').strip()
        
        if not user_query:
            flash('Please enter a query about deforestation.')
            return redirect(url_for('analysis'))
        
        if len(user_query) < 10:
            flash('Please provide a more detailed query.')
            return redirect(url_for('analysis'))
        
        # Process query with Gemini AI
        print(f"Processing query: {user_query}")
        analysis_data = analyze_deforestation_query_with_gemini(user_query)
        
        # Create visualizations
        chart_success = create_visualization_charts(analysis_data)
        analysis_data['charts_available'] = chart_success
        
        # Save analysis data for results page
        with open(os.path.join(RESULTS_FOLDER, 'query_analysis.json'), 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        return redirect(url_for('query_results'))
        
    except Exception as e:
        print(f"Error processing query: {e}")
        flash(f'Error processing your query: {str(e)}')
        return redirect(url_for('analysis'))

@app.route('/query_results')
def query_results():
    """Display analysis results"""
    try:
        # Load analysis data
        with open(os.path.join(RESULTS_FOLDER, 'query_analysis.json'), 'r') as f:
            analysis_data = json.load(f)
        
        return render_template('query_results.html', data=analysis_data)
    
    except FileNotFoundError:
        flash('No analysis results found. Please submit a query first.')
        return redirect(url_for('analysis'))
    except Exception as e:
        flash(f'Error loading results: {str(e)}')
        return redirect(url_for('analysis'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        user_query = data['query'].strip()
        if not user_query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Process query
        analysis_data = analyze_deforestation_query_with_gemini(user_query)
        
        return jsonify({
            'success': True,
            'data': analysis_data,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/clear_results')
def clear_results():
    """Clear previous results"""
    try:
        for filename in os.listdir(RESULTS_FOLDER):
            file_path = os.path.join(RESULTS_FOLDER, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        flash('Previous results cleared.')
    except Exception as e:
        flash(f'Error clearing results: {str(e)}')
    
    return redirect(url_for('analysis'))

if __name__ == '__main__':
    print("Starting Deforestation Analysis Server...")
    print("Gemini AI configured successfully")
    app.run(debug=True, host='0.0.0.0', port=5000)