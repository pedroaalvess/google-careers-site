import os
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuração da aplicação Flask
app = Flask(__name__, static_folder='static', static_url_path='')

# Configuração CORS
CORS(app, origins=["*"])

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'database', 'app.db')

# Criar diretório do banco se não existir
os.makedirs(os.path.dirname(database_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração para uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
upload_folder = os.path.join(basedir, 'uploads')
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

# Inicializar banco de dados
db = SQLAlchemy(app)

# Modelos do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Candidature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    spi = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    motivation = db.Column(db.Text)
    document_front = db.Column(db.String(255))
    document_back = db.Column(db.String(255))
    residence_proof = db.Column(db.String(255))
    terms_accepted = db.Column(db.Boolean, default=False)
    validity_confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Rotas para arquivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir arquivos estáticos (CSS, JS, imagens)"""
    static_folder_path = os.path.join(basedir, 'static')
    return send_from_directory(static_folder_path, filename)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    """Servir arquivos de upload"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Rota principal
@app.route('/')
def index():
    """Página principal"""
    try:
        static_folder_path = os.path.join(basedir, 'static')
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404
    except Exception as e:
        return f"Erro ao carregar página: {str(e)}", 500

# Rota de teste
@app.route('/test')
def test():
    """Rota de teste para verificar funcionamento"""
    return jsonify({
        "status": "success",
        "message": "Google Careers Site is running!",
        "python_version": sys.version,
        "flask_version": "2.3.3",
        "static_folder": app.static_folder,
        "base_dir": basedir
    })

# Rotas da API
@app.route('/api/candidatures', methods=['POST'])
def create_candidature():
    """Criar nova candidatura"""
    try:
        data = request.form
        
        # Validar dados obrigatórios (usando nomes corretos do HTML)
        required_fields = ['nom_complet', 'email', 'spi', 'telephone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400
        
        # Processar uploads (usando nomes corretos do HTML)
        uploaded_files = {}
        file_fields = ['photo_recto', 'photo_verso', 'justificatif_domicile']
        
        for field in file_fields:
            if field in request.files:
                file = request.files[field]
                if file and file.filename:
                    filename = secure_filename(f"{data.get('nom_complet', 'user')}_{field}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    uploaded_files[field] = filename
        
        # Criar candidatura (mapeando nomes do HTML para campos do banco)
        candidature = Candidature(
            name=data.get('nom_complet'),  # HTML: nom_complet -> DB: name
            email=data.get('email'),
            spi=data.get('spi'),
            phone=data.get('telephone'),   # HTML: telephone -> DB: phone
            motivation=data.get('motivation', ''),
            document_front=uploaded_files.get('photo_recto'),      # HTML: photo_recto -> DB: document_front
            document_back=uploaded_files.get('photo_verso'),       # HTML: photo_verso -> DB: document_back
            residence_proof=uploaded_files.get('justificatif_domicile'),  # HTML: justificatif_domicile -> DB: residence_proof
            terms_accepted=data.get('accepte_traitement_donnees') == 'true',
            validity_confirmed=data.get('confirme_validite_documents') == 'true'
        )
        
        db.session.add(candidature)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Candidatura enviada com sucesso!",
            "id": candidature.id
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Erro ao processar candidatura: {str(e)}"}), 500

@app.route('/api/candidatures', methods=['GET'])
def get_candidatures():
    """Listar todas as candidaturas"""
    try:
        candidatures = Candidature.query.order_by(Candidature.created_at.desc()).all()
        result = []
        
        for c in candidatures:
            result.append({
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "spi": c.spi,
                "phone": c.phone,
                "motivation": c.motivation,
                "document_front": c.document_front,
                "document_back": c.document_back,
                "residence_proof": c.residence_proof,
                "terms_accepted": c.terms_accepted,
                "validity_confirmed": c.validity_confirmed,
                "created_at": c.created_at.isoformat() if c.created_at else None
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar candidaturas: {str(e)}"}), 500

# Rota de admin
@app.route('/api/admin/candidatures')
def admin_candidatures():
    """Painel de administração das candidaturas"""
    try:
        candidatures = Candidature.query.order_by(Candidature.created_at.desc()).all()
        
        html_template = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin - Google Careers</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
                h1 { color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }
                .stats { display: flex; gap: 20px; margin: 20px 0; }
                .stat-card { background: #e8f0fe; padding: 15px; border-radius: 8px; text-align: center; flex: 1; }
                .stat-number { font-size: 2em; font-weight: bold; color: #1a73e8; }
                .stat-label { color: #5f6368; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f8f9fa; font-weight: bold; }
                tr:hover { background: #f8f9fa; }
                .file-link { color: #1a73e8; text-decoration: none; }
                .file-link:hover { text-decoration: underline; }
                .status-yes { color: #34a853; font-weight: bold; }
                .status-no { color: #ea4335; font-weight: bold; }
                .date { color: #5f6368; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Google Careers - Painel de Administração</h1>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{{ total_candidatures }}</div>
                        <div class="stat-label">Total de Candidaturas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ today_candidatures }}</div>
                        <div class="stat-label">Hoje</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ with_documents }}</div>
                        <div class="stat-label">Com Documentos</div>
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Email</th>
                            <th>SPI</th>
                            <th>Telefone</th>
                            <th>Documentos</th>
                            <th>Termos</th>
                            <th>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for candidature in candidatures %}
                        <tr>
                            <td>{{ candidature.id }}</td>
                            <td>{{ candidature.name }}</td>
                            <td>{{ candidature.email }}</td>
                            <td>{{ candidature.spi }}</td>
                            <td>{{ candidature.phone }}</td>
                            <td>
                                {% if candidature.document_front %}
                                    <a href="/uploads/{{ candidature.document_front }}" class="file-link" target="_blank">Frente</a><br>
                                {% endif %}
                                {% if candidature.document_back %}
                                    <a href="/uploads/{{ candidature.document_back }}" class="file-link" target="_blank">Verso</a><br>
                                {% endif %}
                                {% if candidature.residence_proof %}
                                    <a href="/uploads/{{ candidature.residence_proof }}" class="file-link" target="_blank">Comprovante</a>
                                {% endif %}
                            </td>
                            <td>
                                <span class="{{ 'status-yes' if candidature.terms_accepted else 'status-no' }}">
                                    {{ 'Sim' if candidature.terms_accepted else 'Não' }}
                                </span>
                            </td>
                            <td class="date">{{ candidature.created_at.strftime('%d/%m/%Y %H:%M') if candidature.created_at else 'N/A' }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                
                {% if not candidatures %}
                <p style="text-align: center; color: #5f6368; margin-top: 40px;">
                    Nenhuma candidatura encontrada.
                </p>
                {% endif %}
            </div>
        </body>
        </html>
        """
        
        # Calcular estatísticas
        total_candidatures = len(candidatures)
        today = datetime.now().date()
        today_candidatures = len([c for c in candidatures if c.created_at and c.created_at.date() == today])
        with_documents = len([c for c in candidatures if c.document_front or c.document_back or c.residence_proof])
        
        return render_template_string(html_template, 
                                    candidatures=candidatures,
                                    total_candidatures=total_candidatures,
                                    today_candidatures=today_candidatures,
                                    with_documents=with_documents)
        
    except Exception as e:
        return f"Erro no painel de admin: {str(e)}", 500

# Inicializar banco de dados
def init_db():
    """Inicializar banco de dados"""
    try:
        with app.app_context():
            db.create_all()
            print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

if __name__ == '__main__':
    # Configuração para produção (Railway, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Iniciando aplicação na porta {port}")
    print(f"Modo debug: {debug_mode}")
    print(f"Diretório base: {basedir}")
    print(f"Pasta static: {os.path.join(basedir, 'static')}")
    
    # Inicializar banco de dados
    init_db()
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
else:
    # Para servidores WSGI (Gunicorn, etc.)
    init_db()

