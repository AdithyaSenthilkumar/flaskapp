from exts import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email= db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        pass


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.String(50), nullable=False)
    invoice_number = db.Column(db.String(255), unique=True, nullable=False)
    invoice_date = db.Column(db.String(50))
    supplier_name = db.Column(db.String(255))
    supplier_address = db.Column(db.Text)
    supplier_GSTIN = db.Column(db.String(50))
    customer_address = db.Column(db.Text)
    customer_GSTIN = db.Column(db.String(50))
    PO_number = db.Column(db.String(255))
    total_amount = db.Column(db.String(50))
    total_tax_percentage = db.Column(db.String(50))
    job_ID = db.Column(db.String(50))
    vehicle_number = db.Column(db.String(50))
    s3_filepath = db.Column(db.Text)
    scanning_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    processed_by = db.Column(db.String(80))
    approved_by = db.Column(db.String(80))
    reference_number = db.Column(db.String(255), unique=True, nullable=False)
    data = db.Column(db.JSON)
    ocr_quality_score = db.Column(db.Float)

    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
        db.session.commit()
        
    
