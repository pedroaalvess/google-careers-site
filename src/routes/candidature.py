import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from src.models.candidature import Candidature
from src.models.user import db
from datetime import datetime
import uuid

candidature_bp = Blueprint('candidature', __name__)

# Configurações de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder

@candidature_bp.route('/candidatures', methods=['POST'])
def submit_candidature():
    try:
        # Vérifier que tous les champs requis sont présents
        required_fields = ['nom_complet', 'email', 'spi', 'telephone', 
                          'accepte_traitement_donnees', 'confirme_validite_documents']
        
        for field in required_fields:
            if field not in request.form:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Vérifier que les cases sont cochées
        if request.form.get('accepte_traitement_donnees') != 'true':
            return jsonify({'error': 'Vous devez accepter le traitement des données personnelles'}), 400
            
        if request.form.get('confirme_validite_documents') != 'true':
            return jsonify({'error': 'Vous devez confirmer la validité de vos documents'}), 400
        
        # Créer une nouvelle candidature
        candidature = Candidature(
            nom_complet=request.form['nom_complet'],
            email=request.form['email'],
            spi=request.form['spi'],
            telephone=request.form['telephone'],
            motivation=request.form.get('motivation', ''),
            accepte_traitement_donnees=True,
            confirme_validite_documents=True,
            ip_address=request.remote_addr
        )
        
        # Gérer les uploads de fichiers
        upload_folder = get_upload_folder()
        
        # Photo recto
        if 'photo_recto' in request.files:
            file = request.files['photo_recto']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                candidature.photo_recto = filepath
        
        # Photo verso
        if 'photo_verso' in request.files:
            file = request.files['photo_verso']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                candidature.photo_verso = filepath
        
        # Justificatif de domicile
        if 'justificatif_domicile' in request.files:
            file = request.files['justificatif_domicile']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                candidature.justificatif_domicile = filepath
        
        # Sauvegarder en base de données
        db.session.add(candidature)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Candidature soumise avec succès!',
            'candidature_id': candidature.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la soumission: {str(e)}'}), 500

@candidature_bp.route('/candidatures', methods=['GET'])
def get_candidatures():
    """Endpoint pour récupérer toutes les candidatures (pour l'admin)"""
    try:
        candidatures = Candidature.query.order_by(Candidature.date_candidature.desc()).all()
        return jsonify([candidature.to_dict() for candidature in candidatures]), 200
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération: {str(e)}'}), 500

@candidature_bp.route('/candidatures/<int:candidature_id>', methods=['GET'])
def get_candidature(candidature_id):
    """Endpoint pour récupérer une candidature spécifique"""
    try:
        candidature = Candidature.query.get_or_404(candidature_id)
        return jsonify(candidature.to_dict()), 200
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération: {str(e)}'}), 500



@candidature_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Servir arquivos uploadados"""
    try:
        upload_folder = get_upload_folder()
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        return jsonify({'error': f'Arquivo não encontrado: {str(e)}'}), 404

@candidature_bp.route('/admin/candidatures', methods=['GET'])
def admin_candidatures():
    """Página de administração para visualizar candidaturas"""
    try:
        candidatures = Candidature.query.order_by(Candidature.date_candidature.desc()).all()
        
        # Criar HTML simples para visualização
        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Administration - Candidatures Google</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #1a73e8; text-align: center; }
                .stats { display: flex; gap: 20px; margin-bottom: 30px; }
                .stat-card { background: white; padding: 20px; border-radius: 8px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .stat-number { font-size: 2rem; font-weight: bold; color: #1a73e8; }
                .stat-label { color: #666; margin-top: 5px; }
                table { width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
                th { background: #1a73e8; color: white; }
                .documents { display: flex; gap: 10px; }
                .doc-link { background: #e8f0fe; color: #1a73e8; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 0.8rem; }
                .doc-link:hover { background: #d2e3fc; }
                .status-ok { color: #34a853; font-weight: bold; }
                .status-missing { color: #ea4335; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏢 Administration Google Careers</h1>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">""" + str(len(candidatures)) + """</div>
                        <div class="stat-label">Total Candidatures</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">""" + str(len([c for c in candidatures if c.photo_recto and c.photo_verso and c.justificatif_domicile])) + """</div>
                        <div class="stat-label">Dossiers Complets</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">""" + str(len([c for c in candidatures if c.date_candidature.date() == datetime.utcnow().date()])) + """</div>
                        <div class="stat-label">Aujourd'hui</div>
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nom Complet</th>
                            <th>Email</th>
                            <th>SPI</th>
                            <th>Téléphone</th>
                            <th>Documents</th>
                            <th>Date</th>
                            <th>Statut</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for candidature in candidatures:
            docs_html = '<div class="documents">'
            if candidature.photo_recto:
                docs_html += f'<a href="/api/uploads/{os.path.basename(candidature.photo_recto)}" target="_blank" class="doc-link">Recto</a>'
            if candidature.photo_verso:
                docs_html += f'<a href="/api/uploads/{os.path.basename(candidature.photo_verso)}" target="_blank" class="doc-link">Verso</a>'
            if candidature.justificatif_domicile:
                docs_html += f'<a href="/api/uploads/{os.path.basename(candidature.justificatif_domicile)}" target="_blank" class="doc-link">Domicile</a>'
            docs_html += '</div>'
            
            complete = candidature.photo_recto and candidature.photo_verso and candidature.justificatif_domicile
            status_class = "status-ok" if complete else "status-missing"
            status_text = "✅ Complet" if complete else "⚠️ Incomplet"
            
            html += f"""
                        <tr>
                            <td>#{candidature.id}</td>
                            <td>{candidature.nom_complet}</td>
                            <td>{candidature.email}</td>
                            <td>{candidature.spi}</td>
                            <td>{candidature.telephone}</td>
                            <td>{docs_html}</td>
                            <td>{candidature.date_candidature.strftime('%d/%m/%Y %H:%M')}</td>
                            <td class="{status_class}">{status_text}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération: {str(e)}'}), 500

