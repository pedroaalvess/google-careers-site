# 🚀 Tutorial Completo de Deploy - Google Careers Site

Este tutorial te guiará através do processo completo de deploy do site Google Careers no **Railway** e **Vercel**.

## 📋 Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta no [Railway](https://railway.app) OU [Vercel](https://vercel.com)
- Git instalado localmente
- Python 3.8+ (para Railway)
- Node.js 16+ (para Vercel)

## 📁 Estrutura do Projeto

```
google-careers-site/
├── src/
│   ├── static/
│   │   ├── index.html          # Página principal
│   │   ├── styles.css          # Estilos CSS
│   │   ├── script.js           # JavaScript
│   │   └── google_careers_logo.webp  # Logo
│   ├── models/
│   │   ├── user.py             # Modelo usuário
│   │   └── candidature.py      # Modelo candidatura
│   ├── routes/
│   │   ├── user.py             # Routes usuário
│   │   └── candidature.py      # Routes candidatura
│   ├── uploads/                # Arquivos enviados
│   ├── database/
│   │   └── app.db              # Banco SQLite
│   └── main.py                 # Aplicação Flask
├── venv/                       # Ambiente virtual
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão Python (Railway)
├── Procfile                    # Comando de start (Railway)
├── vercel.json                 # Config Vercel
├── package.json                # Config Node.js (Vercel)
├── README.md                   # Documentação
└── DEPLOY_TUTORIAL.md          # Este tutorial
```

---

# 🚂 DEPLOY NO RAILWAY

Railway é ideal para aplicações Flask/Python com banco de dados.

## 1️⃣ Preparação do Projeto

### Criar arquivos necessários:

**requirements.txt** (já incluído):
```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Werkzeug==2.3.7
```

**runtime.txt**:
```txt
python-3.11.0
```

**Procfile**:
```txt
web: python src/main.py
```

## 2️⃣ Upload para GitHub

```bash
# 1. Inicializar repositório Git
git init

# 2. Adicionar arquivos
git add .

# 3. Commit inicial
git commit -m "Initial commit - Google Careers Site"

# 4. Conectar ao GitHub
git remote add origin https://github.com/SEU_USUARIO/google-careers-site.git

# 5. Push para GitHub
git push -u origin main
```

## 3️⃣ Deploy no Railway

1. **Acesse [Railway.app](https://railway.app)**
2. **Faça login com GitHub**
3. **Clique em "New Project"**
4. **Selecione "Deploy from GitHub repo"**
5. **Escolha seu repositório `google-careers-site`**
6. **Railway detectará automaticamente que é um projeto Python**

### Configurações no Railway:

1. **Variables (Variáveis de Ambiente)**:
   - Não são necessárias para este projeto

2. **Settings**:
   - **Start Command**: `python src/main.py`
   - **Port**: `5000` (automático)

3. **Deploy**:
   - Railway fará o deploy automaticamente
   - Aguarde o processo completar (~3-5 minutos)

## 4️⃣ Acessar Aplicação

- Railway fornecerá uma URL como: `https://seu-projeto.railway.app`
- O site estará disponível 24/7

---

# ⚡ DEPLOY NO VERCEL

Vercel é otimizado para aplicações serverless. Requer adaptação do Flask.

## 1️⃣ Preparação para Vercel

### Criar estrutura serverless:

**vercel.json**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

**api/index.py** (adaptação do main.py):
```python
from flask import Flask
from flask_cors import CORS
import os
import sys

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app

# Configurar CORS para Vercel
CORS(app, origins=["*"])

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == "__main__":
    app.run()
```

**requirements.txt** (mesmo conteúdo):
```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Werkzeug==2.3.7
```

## 2️⃣ Deploy no Vercel

### Opção A: Via GitHub

1. **Acesse [Vercel.com](https://vercel.com)**
2. **Faça login com GitHub**
3. **Clique em "New Project"**
4. **Selecione seu repositório**
5. **Configure**:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (deixe vazio)
   - **Output Directory**: (deixe vazio)

### Opção B: Via CLI

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Seguir prompts:
# - Link to existing project? N
# - Project name: google-careers-site
# - Directory: ./
# - Override settings? N
```

## 3️⃣ Configurações no Vercel

1. **Environment Variables**: Não necessárias
2. **Domains**: Vercel fornece domínio automático
3. **Functions**: Configuração automática

---

# 🔧 CONFIGURAÇÕES AVANÇADAS

## Railway - Configurações Opcionais

### Domínio Customizado:
1. **Settings → Domains**
2. **Add Custom Domain**
3. **Configure DNS** (CNAME para railway.app)

### Banco de Dados Externo:
1. **Add Service → Database → PostgreSQL**
2. **Conectar variáveis de ambiente**
3. **Migrar de SQLite para PostgreSQL**

### Monitoramento:
1. **Metrics** - CPU, RAM, Network
2. **Logs** - Logs em tempo real
3. **Deployments** - Histórico de deploys

## Vercel - Configurações Opcionais

### Domínio Customizado:
1. **Settings → Domains**
2. **Add Domain**
3. **Configure DNS** (A record ou CNAME)

### Analytics:
1. **Analytics** - Visitantes e performance
2. **Speed Insights** - Core Web Vitals
3. **Functions** - Monitoramento serverless

---

# 🐛 TROUBLESHOOTING

## Problemas Comuns - Railway

### ❌ Build Failed
```bash
# Verificar requirements.txt
pip freeze > requirements.txt

# Verificar runtime.txt
echo "python-3.11.0" > runtime.txt
```

### ❌ Port Error
```python
# Em main.py, usar porta do Railway
import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### ❌ Database Error
```python
# Verificar caminho do banco
db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
```

## Problemas Comuns - Vercel

### ❌ Function Timeout
- Vercel tem limite de 10s para functions gratuitas
- Otimizar queries do banco de dados
- Considerar Railway para aplicações com banco

### ❌ File Upload Issues
- Vercel não suporta upload de arquivos persistente
- Usar serviços externos (AWS S3, Cloudinary)
- Ou migrar para Railway

### ❌ Static Files
```json
// vercel.json - configurar rotas estáticas
{
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

---

# 📊 COMPARAÇÃO: RAILWAY vs VERCEL

## 🚂 Railway
✅ **Vantagens:**
- Ideal para Flask/Python
- Suporte nativo a bancos de dados
- Upload de arquivos funciona
- Logs detalhados
- Fácil configuração

❌ **Desvantagens:**
- Plano gratuito limitado
- Menos otimizado para frontend

## ⚡ Vercel
✅ **Vantagens:**
- Extremamente rápido (CDN global)
- Excelente para frontend
- Deploy automático
- Analytics integrado

❌ **Desvantagens:**
- Complexo para Flask
- Não suporta upload persistente
- Limitações de função serverless

## 🎯 RECOMENDAÇÃO

**Para este projeto (Google Careers):**
- **Use Railway** - Melhor suporte para Flask + SQLite + uploads
- Vercel seria ideal apenas para frontend estático

---

# 🔒 SEGURANÇA E PRODUÇÃO

## Configurações de Segurança

### 1. Variáveis de Ambiente
```python
# Usar variáveis para dados sensíveis
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
```

### 2. HTTPS
- Railway: Automático
- Vercel: Automático
- Domínio customizado: Configurar SSL

### 3. CORS
```python
# Configurar origens permitidas
CORS(app, origins=["https://seudominio.com"])
```

## Backup do Banco

### Railway:
```bash
# Download do banco via Railway CLI
railway connect
# Copiar arquivo app.db
```

### Backup Automático:
```python
# Implementar backup periódico
import schedule
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('database/app.db', f'backups/backup_{timestamp}.db')

schedule.every().day.at("02:00").do(backup_database)
```

---

# 📞 SUPORTE

## Railway
- **Documentação**: [docs.railway.app](https://docs.railway.app)
- **Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Status**: [status.railway.app](https://status.railway.app)

## Vercel
- **Documentação**: [vercel.com/docs](https://vercel.com/docs)
- **Discord**: [vercel.com/discord](https://vercel.com/discord)
- **Status**: [status.vercel.com](https://status.vercel.com)

---

# ✅ CHECKLIST FINAL

## Antes do Deploy:
- [ ] Código commitado no GitHub
- [ ] requirements.txt atualizado
- [ ] Arquivos de configuração criados
- [ ] Banco de dados testado localmente
- [ ] Upload de arquivos funcionando

## Após Deploy:
- [ ] Site acessível via URL
- [ ] Formulário funcionando
- [ ] Upload de documentos OK
- [ ] Admin panel acessível
- [ ] Responsividade mobile OK

## Manutenção:
- [ ] Monitorar logs regularmente
- [ ] Backup do banco de dados
- [ ] Atualizar dependências
- [ ] Verificar performance
- [ ] Renovar domínio (se customizado)

---

**🎉 Parabéns! Seu site Google Careers está online!**

Para dúvidas ou suporte, consulte a documentação oficial das plataformas ou entre em contato.

