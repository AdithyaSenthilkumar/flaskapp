from flask import request,jsonify
from flask_restx import Resource, Namespace
from model_fields import invoice_fields
from models import Invoice
from flask_jwt_extended import jwt_required
from datetime import datetime
import uuid

invoice_ns=Namespace('invoices',description='Namespace for Invoice operations')
invoice_model=invoice_ns.model('Invoice',invoice_fields)

@invoice_ns.route('/invoices')
class InvoicesResource(Resource):
    @invoice_ns.marshal_list_with(invoice_model)
    @jwt_required()
    def get(self):
        """Get all invoices"""
        invoices=Invoice.query.all()
        return invoices
    
    @invoice_ns.marshal_with(invoice_model)
    @invoice_ns.expect(invoice_model)
    def post(self):
        """Create a new invoice"""
        data=request.get_json()
        new_invoice=Invoice(
            division=data.get('division'),
            invoice_number=data.get('invoice_number'),
            invoice_date=data.get('invoice_date'),
            supplier_name=data.get('supplier_name'),
            supplier_address=data.get('supplier_address'),
            supplier_GSTIN=data.get('supplier_GSTIN'),
            customer_address=data.get('customer_address'),
            customer_GSTIN=data.get('customer_GSTIN'),
            PO_number=data.get('PO_number'),
            total_amount=data.get('total_amount'),
            total_tax_percentage=data.get('total_tax_percentage'),
            job_ID=data.get('job_ID'),
            vehicle_number=data.get('vehicle_number'),
            s3_filepath=data.get('s3_filepath'),
            scanning_date=datetime.now(),
            status=data.get('status'),
            processed_by=data.get('processed_by'),
            approved_by=data.get('approved_by'),
            reference_number=str(uuid.uuid4()),
            data=data.get('data'),
            ocr_quality_score=data.get('ocr_quality_score')
        )
        new_invoice.save()
        return new_invoice,201

@invoice_ns.route('/invoices/<int:id>')
class InvoiceResource(Resource):
    @invoice_ns.marshal_with(invoice_model)
    def get(self,id):
        """Get an invoice by id"""
        invoice=Invoice.query.get_or_404(id)
        if invoice:
            return invoice
        return jsonify({"message":"Invoice not found"})
    @invoice_ns.marshal_with(invoice_model)
    @jwt_required()
    def delete(self,id):
        """Delete an invoice by id"""
        deleted_invoice=Invoice.query.get_or_404(id)
        if deleted_invoice:
            deleted_invoice.delete()
            return deleted_invoice
        return jsonify({"message":"Invoice not found"})
    
    @invoice_ns.marshal_with(invoice_model)
    @invoice_ns.expect(invoice_model)
    def put(self,id):
        """Update an invoice by id"""
        updated_invoice=Invoice.query.get_or_404(id)
        if updated_invoice:
            data=request.get_json()
            updated_invoice.update(**data)
            return updated_invoice
        return jsonify({"message":"Invoice not found"})
