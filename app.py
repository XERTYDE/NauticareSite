from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import random
import json

app = Flask(__name__)

# Configuration pour servir les fichiers statiques du dossier features
@app.route('/features/<path:filename>')
def serve_feature(filename):
    return send_from_directory('features', filename)

@app.route('/random-bg')
def random_bg():
    bg_dir = os.path.join(app.root_path, 'features', 'bg')
    bg_files = [f for f in os.listdir(bg_dir) if f.startswith('bg') and f.endswith('.mp4')]
    if not bg_files:
        return jsonify({'error': 'No background videos found'}), 404
    random_bg = random.choice(bg_files)
    return jsonify({'video': random_bg})

COUNTER_FILE = 'click_counters.json'

def load_counters():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return json.load(f)
    return {'demarrage': 0, 'recharge': 0}

def save_counters(counters):
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counters, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/acheter_demarrage', methods=['POST'])
def acheter_demarrage():
    counters = load_counters()
    counters['demarrage'] += 1
    save_counters(counters)
    return jsonify({'compteur': counters['demarrage']})

@app.route('/acheter_recharge', methods=['POST'])
def acheter_recharge():
    counters = load_counters()
    data = request.get_json()
    selected_patches = data.get('patches', [])
    
    # Vérification que 3 patchs ont été sélectionnés
    if len(selected_patches) != 3:
        return jsonify({'error': 'Veuillez sélectionner exactement 3 patchs'}), 400
    
    counters['recharge'] += 1
    save_counters(counters)
    return jsonify({
        'compteur': counters['recharge'],
        'selected_patches': selected_patches
    })

@app.route('/compteur')
def compteur():
    counters = load_counters()
    return jsonify({'compteur': counters['demarrage'] + counters['recharge']})

@app.route('/mentions')
def mentions():
    return render_template('mentions.html')

@app.route('/produit')
def produit():
    return render_template('produit.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/get_counters')
def get_counters():
    return jsonify(load_counters())

@app.route('/increment_counter/<counter_type>')
def increment_counter(counter_type):
    counters = load_counters()
    if counter_type in counters:
        counters[counter_type] += 1
        save_counters(counters)
    return jsonify(counters)

if __name__ == '__main__':
    app.run(debug=True) 