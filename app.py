from flask import Flask, jsonify
import requests
import csv
from datetime import datetime
import io

app = Flask(__name__)

def get_characters():
    """Get and filter Rick and Morty characters"""
    api_url = "https://rickandmortyapi.com/api/character"
    all_characters = []
    current_page = api_url
    
    while current_page:
        response = requests.get(current_page)
        data = response.json()
        all_characters.extend(data['results'])
        current_page = data['info']['next']
    
    filtered_list = []
    for character in all_characters:
        if (character['species'] == 'Human' and 
            character['status'] == 'Alive' and
            'earth' in character['origin']['name'].lower()):
            
            filtered_list.append({
                'Name': character['name'],
                'Origin': character['origin']['name'],
                'Location': character['location']['name'],
                'Image': character['image']
            })
    
    return filtered_list

@app.route('/characters', methods=['GET'])
def get_character_data():
    """API endpoint to get filtered character data"""
    try:
        characters = get_characters()
        return jsonify({
            'status': 'success',
            'count': len(characters),
            'data': characters
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/characters/csv', methods=['GET'])
def get_character_csv():
    """API endpoint to get character data as CSV"""
    try:
        characters = get_characters()
        
        # Create CSV in memory
        output = io.StringIO()
        fieldnames = ['Name', 'Origin', 'Location', 'Image']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(characters)
        
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=characters_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Health check endpoint that verifies critical service components"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'checks': {
            'rick_and_morty_api': {
                'status': 'unknown',
                'latency_ms': 0
            }
        }
    }

    try:
        # Check Rick and Morty API connectivity
        start_time = datetime.now()
        response = requests.get('https://rickandmortyapi.com/api/character/1')
        latency = (datetime.now() - start_time).total_seconds() * 1000  # Convert to milliseconds
        
        health_status['checks']['rick_and_morty_api'] = {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'latency_ms': round(latency, 2),
            'status_code': response.status_code
        }

        # Determine overall health based on all checks
        if all(check['status'] == 'healthy' for check in health_status['checks'].values()):
            health_status['status'] = 'healthy'
        else:
            health_status['status'] = 'unhealthy'
            return jsonify(health_status), 500

        return jsonify(health_status)

    except requests.RequestException as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['rick_and_morty_api'] = {
            'status': 'unhealthy',
            'error': str(e),
            'latency_ms': 0
        }
        return jsonify(health_status), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)