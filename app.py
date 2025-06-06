import os
import base64
import io
import requests
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv
from translations import get_translations

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set in the .env file")

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Définir les maladies disponibles
DISEASES = [
    "alzheimers", 
    "parkinsons", 
    "diabetes", 
    "cancer", 
    "heart_disease",
    "covid19"
]

# Définir les langues disponibles
LANGUAGES = ["en", "fr", "ar"]

@app.before_request
def before_request():
    # Définir la langue par défaut si elle n'est pas déjà dans la session
    if 'language' not in session:
        session['language'] = 'en'

@app.route('/')
def index():
    current_lang = session.get('language', 'en')
    translations = get_translations(current_lang)
    return render_template('index.html', 
                          translations=translations,
                          diseases=DISEASES,
                          current_lang=current_lang)

@app.route('/change_language/<lang>')
def change_language(lang):
    if lang in LANGUAGES:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/disease/<disease_name>')
def disease(disease_name):
    if disease_name not in DISEASES:
        return redirect(url_for('index'))
    
    current_lang = session.get('language', 'en')
    translations = get_translations(current_lang)

    # Get the appropriate images for this disease
    disease_images = {
        "alzheimers": [
            "https://alzheimer-recherche.org/wp-content/uploads/2024/09/IRM-cerveau-1024x683-1.webp",
            "https://www.sante-sur-le-net.com/wp-content/uploads/2021/05/Diabete-type-3.jpg"
        ],
        "parkinsons": [
            "https://parkinsonenmonterrey.com/wp-content/uploads/2024/12/Temblor-parkinson-1-1200-1024x528.jpeg",
            "https://img.youm7.com/large/201904081054375437.jpg"
        ],
        "diabetes": [
            "https://www.aquaportail.com/pictures1712/sang-fluide-corporel.jpg",
             "https://cdn.futura-sciences.com/sources/diab%C3%A8te-hyperglyc%C3%A9mie-inflammation-autre-cause.jpg"
        ],
        "cancer": [
            "https://www.radiofrance.fr/s3/cruiser-production-eu3/2024/04/2c546932-a6b3-4d14-8d85-7495fa737ee0/640x340_sc_sc_gettyimages-1623197589.jpg",
            "https://media.istockphoto.com/id/1317832692/fr/photo/cellule-de-cancer-humain.jpg?s=612x612&w=0&k=20&c=zY1rfFOZajObgOf9C4fQH6Wl_TOrtMukaCrVJL8sXIo="
        ],
        "heart_disease": [
            "https://static.vecteezy.com/ti/photos-gratuite/p1/27798150-anatomie-de-humain-coeur-sur-medical-contexte-ai-generatif-photo.jpg",
            "https://resources.vidal.fr/files/content/images/vidal/maladies/illus-anatomie-coeur.jpg"
        ],
        "covid19": [
            "https://img.freepik.com/photos-premium/illustration-3d-coronavirus-covid-19-virus-au-microscope-dans-echantillon-sang_31965-4318.jpg?semt=ais_hybrid&w=740",
            "https://img.freepik.com/photos-gratuite/modelisation-3d-du-virus-covid_23-2149072245.jpg?w=360",
            
        ]
    }
    
    dna_images = [
        "https://cache.magicmaman.com/data/photo/w1000_ci/1mn/maladie-genetique.jpg",
        "https://img.freepik.com/photos-gratuite/formation-medicale-3d-cellules-virales-abstraites-design-defocalise_1048-15847.jpg?semt=ais_hybrid&w=740",
        "https://lejournal.cnrs.fr/sites/default/files/styles/visuel_principal/public/assets/images/adobestock_217861490_72dpi.jpg"
    ]
    
    return render_template('disease.html', 
                          translations=translations,
                          disease=disease_name,
                          disease_images=disease_images.get(disease_name, []),
                          dna_images=dna_images,
                          diseases=DISEASES,
                          current_lang=current_lang)

@app.route('/chatbot')
def chatbot():
    current_lang = session.get('language', 'en')
    translations = get_translations(current_lang)
    return render_template('chatbot.html', 
                          translations=translations,
                          diseases=DISEASES,
                          current_lang=current_lang)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        query = request.form.get('query')
        image_file = request.files.get('image')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        messages = [
            {
                "role": "user",
                "content": []
            }
        ]
        
        
        messages[0]["content"].append({
            "type": "text", 
            "text": query
        })
        
       
        if image_file and image_file.filename:
            try:
                
                image_content = image_file.read()
                
              
                try:
                    img = Image.open(io.BytesIO(image_content))
                    img.verify()
                except Exception as e:
                    logger.error(f"Invalid image format: {str(e)}")
                    return jsonify({"error": f"Invalid image format: {str(e)}"}), 400
                
                
                encoded_image = base64.b64encode(image_content).decode("utf-8")
                
               
                messages[0]["content"].append({
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                })
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                return jsonify({"error": f"Error processing image: {str(e)}"}), 400
        
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
       
        response = requests.post(
            GROQ_API_URL,
            json={
                "model": model,
                "messages": messages,
                "max_tokens": 1000
            },
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            logger.info("Processed response from API")
            return jsonify({"answer": answer})
        else:
            error_msg = f"Error from API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), response.status_code
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)