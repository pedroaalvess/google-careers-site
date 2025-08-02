from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Candidature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Informações pessoais
    nom_complet = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    spi = db.Column(db.String(50), nullable=False)  # Numéro SPI
    telephone = db.Column(db.String(20), nullable=False)
    
    # Documentos uploadados (caminhos dos arquivos)
    photo_recto = db.Column(db.String(500), nullable=True)  # Foto frente do documento
    photo_verso = db.Column(db.String(500), nullable=True)  # Foto verso do documento
    justificatif_domicile = db.Column(db.String(500), nullable=True)  # Comprovante de residência
    
    # Pergunta motivacional
    motivation = db.Column(db.Text, nullable=True)  # Pourquoi souhaitez-vous rejoindre Google ?
    
    # Termos aceitos
    accepte_traitement_donnees = db.Column(db.Boolean, nullable=False, default=False)
    confirme_validite_documents = db.Column(db.Boolean, nullable=False, default=False)
    
    # Metadados
    date_candidature = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # Para auditoria
    
    def __repr__(self):
        return f'<Candidature {self.nom_complet} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom_complet': self.nom_complet,
            'email': self.email,
            'spi': self.spi,
            'telephone': self.telephone,
            'photo_recto': self.photo_recto,
            'photo_verso': self.photo_verso,
            'justificatif_domicile': self.justificatif_domicile,
            'motivation': self.motivation,
            'accepte_traitement_donnees': self.accepte_traitement_donnees,
            'confirme_validite_documents': self.confirme_validite_documents,
            'date_candidature': self.date_candidature.isoformat() if self.date_candidature else None,
            'ip_address': self.ip_address
        }

