import os 
import re
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image, ImageFilter
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AccountTransaction, UploadedFile
from .serializers import AccountTransactionSerializer, UploadedFileSerializer
import pytesseract

# Set the Tesseract OCR path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Ensure the media directory exists before saving the file
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)

def extract_text_from_image(file_path):
    """Extracts text from an image file using Tesseract OCR"""
    img = Image.open(file_path)
    
    # Improve OCR accuracy
    img = img.convert("L")  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen image

    extracted_text = pytesseract.image_to_string(img)

    # Normalize text encoding and remove extra spaces
    extracted_text = extracted_text.encode("utf-8").decode("utf-8")
    extracted_text = re.sub(r"\s+", " ", extracted_text).strip()
    
    print(f"📝 Extracted text from {file_path}:\n{extracted_text}")  # Debugging output
    
    return extracted_text

def save_transactions_to_db(transactions):
    """Saves extracted transactions into the database."""
    for txn in transactions:
        value_date = txn.get("value_date", None)  # Get value_date or None

        if not value_date:  # Skip if value_date is missing
            print(f"⚠️ Skipping transaction due to missing Value Date: {txn}")
            continue  

        AccountTransaction.objects.create(
            Serial_No=txn.get("serial_no", 0),
            Transaction_Date=txn.get("date"),  # Ensure this key matches parsed data
            Value_Date=value_date,  # Ensure this key matches parsed data
            Description=txn.get("description", "N/A"),
            Cheque_Number=txn.get("cheque_number", "N/A"),
            Debit=txn.get("debit", 0.00),
            Credit=txn.get("credit", 0.00),
            Balance=txn.get("balance", 0.00),
        )

def parse_transactions(text):
    """Parses transactions from extracted text and ensures valid date format."""
    transactions = []
    lines = text.split("\n")
    
    date_pattern = re.compile(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b")  
    
    for line in lines:
        print(f"🔍 Checking line: {line}")  # Debugging
        parts = line.split()
        if len(parts) < 4:
            continue  

        match = date_pattern.findall(line)
        if len(match) < 2:
            print(f"❌ Skipping invalid transaction line: {line}")  
            continue  

        transaction_date = match[0]
        value_date = match[1]
        
        description = " ".join(parts[2:-2])  
        debit = float(parts[-2]) if "DR" in line else 0.00
        credit = float(parts[-2]) if "CR" in line else 0.00
        balance = float(parts[-1])

        transactions.append({
            "date": transaction_date,
            "value_date": value_date,
            "description": description,
            "debit": debit,
            "credit": credit,
            "balance": balance,
        })

    print(f"✅ Parsed {len(transactions)} transactions")  
    return transactions

class AccountTransactionViewSet(viewsets.ModelViewSet):
    queryset = AccountTransaction.objects.all()
    serializer_class = AccountTransactionSerializer

class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            uploaded_file = file_serializer.save()
            file_path = uploaded_file.file.path
            
            extracted_text = self.extract_text(file_path)
            errors = self.analyze_transactions(extracted_text)

            if errors:
                return Response({"status": "error", "errors": errors}, status=400)
            else:
                return Response({"status": "success", "message": "No errors found!"}, status=200)

        return Response(file_serializer.errors, status=400)

    def extract_text(self, file_path):
        """Extracts text from PDF or image files."""
        text = ""
        if file_path.endswith(".pdf"):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith((".jpg", ".png")):
            text = extract_text_from_image(file_path)
        return text

    def extract_text_from_pdf(self, file_path):
        """Extracts text from a PDF file."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def analyze_transactions(self, text):
        """Analyzes extracted text and detects transaction errors."""
        errors = []
        lines = text.split("\n")

        for line in lines:
            if "error" in line.lower():  
                errors.append(line)

        return errors

class AnalyzeFileView(APIView):
    def post(self, request, *args, **kwargs):
        file_name = request.data.get("file_name")
        print(f"🔍 Received file analysis request for: {file_name}")  

        if not file_name:
            print("⚠️ No file name provided in request!")  
            return Response({"error": "File name is required"}, status=400)

        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_name)
        print(f"📂 Expected file path: {file_path}")  

        if not os.path.exists(file_path):
            print("❌ File not found at expected path!")  
            return Response({"error": "File not found"}, status=404)

        extracted_text = self.extract_text(file_path)
        transactions = parse_transactions(extracted_text)
        save_transactions_to_db(transactions)

        return Response({"transactions": transactions}, status=200)

    def extract_text(self, file_path):
        """Extracts text from PDF or image files."""
        text = ""
        if file_path.endswith(".pdf"):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.endswith((".jpg", ".png")):
            text = extract_text_from_image(file_path)
        return text

    def extract_text_from_pdf(self, file_path):
        """Extracts text from a PDF file."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
