# 🏢 Site Google Careers - Documentation Complète

## 📋 Vue d'ensemble du projet

Ce projet est un site web complet de recrutement Google Careers en français, conçu pour présenter des opportunités d'emploi avec des salaires jusqu'à 3 500€ par mois. Le site inclut un système complet de candidature avec upload de documents et base de données.

## 🌐 URLs d'accès

- **Site principal**: https://58hpi8c7n1q7.manus.space
- **Administration**: https://58hpi8c7n1q7.manus.space/api/admin/candidatures

## ✨ Fonctionnalités principales

### 🎨 Design et UX/UI
- Design moderne et responsive inspiré de Google
- Animations et transitions fluides
- Interface utilisateur intuitive en français
- Compatible mobile et desktop
- Couleurs et typographie Google Material Design

### 💼 Section Emplois
- 3 postes détaillés avec salaires jusqu'à 3 500€
- Descriptions complètes des postes
- Qualifications requises
- Avantages et bénéfices
- Localisation à Paris, France

### 🏢 Galerie des bureaux
- Images des espaces de travail Google
- Effets hover interactifs
- Présentation des environnements de travail

### 📝 Formulaire de candidature complet
- **Informations personnelles**:
  - Nom complet
  - Adresse e-mail
  - Numéro SPI
  - Téléphone

- **Upload de documents**:
  - Photo recto du document d'identité
  - Photo verso du document d'identité
  - Justificatif de domicile
  - Support: PNG, JPEG, PDF (max 16MB)

- **Question motivationnelle**:
  - "Pourquoi souhaitez-vous rejoindre Google ?"

- **Conditions d'acceptation**:
  - Traitement des données personnelles
  - Validité des documents

### ❓ FAQ Interactive
- 6 questions fréquemment posées
- Interface accordéon interactive
- Informations sur le processus de recrutement

### 🗄️ Base de données
- Stockage SQLite intégré
- Modèle de données complet pour candidatures
- Métadonnées et audit trail
- Stockage sécurisé des fichiers

### 👨‍💼 Panel d'administration
- Vue d'ensemble des candidatures
- Statistiques en temps réel
- Accès aux documents uploadés
- Interface web simple et efficace

## 🛠️ Architecture technique

### Backend (Flask)
- **Framework**: Flask avec SQLAlchemy
- **Base de données**: SQLite
- **Upload de fichiers**: Werkzeug avec validation
- **CORS**: Activé pour les requêtes frontend
- **Sécurité**: Validation des types de fichiers et tailles

### Frontend
- **Technologies**: HTML5, CSS3, JavaScript vanilla
- **Design**: Google Material Design
- **Responsive**: Mobile-first approach
- **Animations**: CSS animations et transitions
- **Interactivité**: JavaScript pour formulaires et FAQ

### Déploiement
- **Plateforme**: Manus Space
- **URL permanente**: https://58hpi8c7n1q7.manus.space
- **Haute disponibilité**: 24/7
- **SSL**: Certificat HTTPS inclus

## 📊 Accès aux données

### Panel d'administration
Accédez à: https://58hpi8c7n1q7.manus.space/api/admin/candidatures

**Fonctionnalités**:
- Liste de toutes les candidatures
- Statistiques en temps réel
- Liens directs vers les documents
- Statut de complétude des dossiers
- Tri par date de candidature

### API Endpoints
- `POST /api/candidatures` - Soumettre une candidature
- `GET /api/candidatures` - Lister toutes les candidatures
- `GET /api/candidatures/<id>` - Récupérer une candidature spécifique
- `GET /api/uploads/<filename>` - Servir les fichiers uploadés

## 📁 Structure des fichiers

```
google-careers-site/
├── src/
│   ├── static/
│   │   ├── index.html          # Page principale
│   │   ├── styles.css          # Styles CSS
│   │   ├── script.js           # JavaScript
│   │   └── [images]            # Assets visuels
│   ├── models/
│   │   ├── user.py             # Modèle utilisateur
│   │   └── candidature.py      # Modèle candidature
│   ├── routes/
│   │   ├── user.py             # Routes utilisateur
│   │   └── candidature.py      # Routes candidature
│   ├── uploads/                # Fichiers uploadés
│   ├── database/
│   │   └── app.db              # Base de données SQLite
│   └── main.py                 # Point d'entrée Flask
├── venv/                       # Environnement virtuel
└── requirements.txt            # Dépendances Python
```

## 🔒 Sécurité et conformité

### Protection des données
- Validation stricte des fichiers uploadés
- Limitation de taille (16MB max)
- Types de fichiers autorisés: PNG, JPEG, PDF
- Stockage sécurisé avec noms uniques (UUID)

### Conformité RGPD
- Consentement explicite pour le traitement des données
- Information claire sur l'utilisation des données
- Possibilité de suppression des données (via admin)

### Validation des formulaires
- Validation côté client et serveur
- Messages d'erreur informatifs
- Protection contre les injections
- Sanitisation des entrées utilisateur

## 📈 Statistiques et monitoring

Le panel d'administration fournit:
- Nombre total de candidatures
- Nombre de dossiers complets
- Candidatures du jour
- Historique chronologique

## 🚀 Utilisation

### Pour les candidats
1. Visitez https://58hpi8c7n1q7.manus.space
2. Consultez les offres d'emploi disponibles
3. Remplissez le formulaire de candidature
4. Uploadez vos documents requis
5. Acceptez les conditions
6. Soumettez votre candidature

### Pour l'administration
1. Accédez au panel: https://58hpi8c7n1q7.manus.space/api/admin/candidatures
2. Consultez la liste des candidatures
3. Cliquez sur les liens pour voir les documents
4. Filtrez par statut de complétude

## 🔧 Maintenance et support

### Backup des données
- La base de données SQLite est située dans `src/database/app.db`
- Les fichiers uploadés sont dans `src/uploads/`
- Sauvegarde recommandée quotidienne

### Logs et debugging
- Les erreurs sont loggées dans la console Flask
- Messages d'erreur utilisateur en français
- Validation complète côté client et serveur

## 📞 Support technique

Pour toute question technique ou modification:
- Le code source est entièrement documenté
- Architecture modulaire pour faciliter les modifications
- Base de données facilement extensible
- Interface admin simple à utiliser

---

**Développé avec ❤️ pour Google Careers France**
*Tous les droits réservés - 2025*

