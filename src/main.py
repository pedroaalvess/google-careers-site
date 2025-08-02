import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Configuração da aplicação Flask
app = Flask(__name__)

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

# Importar modelos
sys.path.append(basedir)
try:
    from models.user import User
    from models.candidature import Candidature
except ImportError as e:
    print(f"Erro ao importar modelos: {e}")
    # Criar modelos básicos se não conseguir importar
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        
    class Candidature(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        spi = db.Column(db.String(50), nullable=False)
        phone = db.Column(db.String(20), nullable=False)
        motivation = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Importar rotas
try:
    from routes.user import user_bp
    from routes.candidature import candidature_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(candidature_bp, url_prefix='/api')
except ImportError as e:
    print(f"Erro ao importar rotas: {e}")
    # Criar rotas básicas se não conseguir importar
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "ok", "message": "Application is running"})

# Rota para servir arquivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    static_folder_path = os.path.join(basedir, 'static')
    return send_from_directory(static_folder_path, filename)

# Rota principal
@app.route('/')
def index():
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
    return jsonify({
        "status": "success",
        "message": "Google Careers Site is running!",
        "python_version": sys.version,
        "flask_version": "2.3.3"
    })

# Inicializar banco de dados
def init_db():
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
    
    # Inicializar banco de dados
    init_db()
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
else:
    # Para servidores WSGI (Gunicorn, etc.)
    init_db()

