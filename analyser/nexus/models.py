from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AccountTransaction(models.Model):
    Serial_No = models.IntegerField(primary_key=True, default=0)  # Use an appropriate default value
    Transaction_Date = models.DateField()
    Value_Date = models.DateField()
    Description = models.CharField(max_length=100, default="N/A")
    Cheque_Number = models.CharField(max_length=50, default="N/A")  
    Debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # FIXED: Set default as 0.00
    Credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # FIXED: Set default as 0.00
    Balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.Transaction_Date} - {self.Description} - ₹{self.Balance:.2f}"
