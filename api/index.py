from flask import Flask
from flask_cors import CORS
import os
import sys

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from main import app
except ImportError:
    # Fallback se não conseguir importar
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "Google Careers Site - Deploy Error: Cannot import main app"

# Configurar CORS para Vercel
CORS(app, origins=["*"])

# Configurar para produção
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# Para desenvolvimento local
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

