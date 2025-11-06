# Chatbot IA Générative — Projet Santé

Ce projet fournit une **application web interactive** permettant l'accès à l'information médicale et de santé via une interface conversationnelle intelligente.

---

## 1. Contexte et objectifs

Le chatbot a pour objectifs de :  

- Fournir aux utilisateurs (patients, accompagnants, professionnels non spécialistes) une interface simple pour poser des questions sur des maladies et obtenir des réponses contextualisées.  
- Permettre l'envoi d'images (photos, scans) pour enrichir la requête et améliorer la précision des réponses.  
- Centraliser les interactions pour produire des jeux de données analytiques et monitorer l'usage et les erreurs.  

> ⚠️ **Remarque :** Cette application est informative et ne remplace pas un avis médical professionnel.

---

## 2. Publics cibles et cas d'utilisation

### Publics

- **Utilisateurs finaux** : personnes cherchant des informations fiables sur des maladies et symptômes.  
- **Professionnels de santé non spécialiste** : accès rapide à des synthèses médicales.  

### Cas d'utilisation

- Recherche d'informations médicales  
- Vérification de ressources médicales  
- Discussion multimodale (texte + image)  
- Collecte de feedback sur la qualité des réponses  

---

## 3. Fonctionnalités principales

- Interface web multilingue (FR / EN / AR)  
- Catalogue de maladies avec images et contenu statique  
- Chat en temps réel avec support texte + image  
- Backend Flask pour préparation des messages et orchestration de l'API externe  
- Validation et encodage des images en **base64** côté serveur (Pillow)  

---

## 4. Architecture technique

### Composants principaux

- **Frontend** : templates HTML + JavaScript pour l’UI et la gestion des requêtes  
- **Backend** : Flask (`app.py`) pour routes, validation des entrées, encodage images, orchestration API  
- **API externe** : service génératif type GROQ/OpenAI pour produire les réponses  



## 5. Flux de données

1. L'utilisateur soumet une requête via l'interface (texte + image optionnelle).  
2. Le frontend envoie une requête POST à `/api/chat`.  
3. Le backend effectue les actions suivantes :  
   - Valide le texte et l'image (via Pillow)  
   - Encode l'image en base64 si présente  
   - Construit le payload attendu par l'API externe  
   - Appelle l'API via `requests` avec la clé `GROQ_API_KEY`  
4. La réponse générée est renvoyée au frontend et peut être journalisée pour analyse.  
