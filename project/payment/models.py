from django.db import models
from django.core.exceptions import ValidationError

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('CARD', 'Debit/Credit Card'),
        ('NETBANKING', 'Net Banking'),
        ('WALLET', 'Wallet'),
    ]

    # Fields for payment details
    name = models.CharField(max_length=100, blank=True)  # optional name
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    wallet_name = models.CharField(max_length=50, blank=True, null=True)

    # Amount to be paid
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    status = models.CharField(max_length=20, default='Success')  # always success for demo
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validation based on payment method
        if self.payment_method == 'CARD' and not self.card_number:
            raise ValidationError('Card number is required for card payments.')
        if self.payment_method == 'NETBANKING' and not self.bank_name:
            raise ValidationError('Bank name is required for net banking payments.')
        if self.payment_method == 'UPI' and not self.upi_id:
            raise ValidationError('UPI ID is required for UPI payments.')
        if self.payment_method == 'WALLET' and not self.wallet_name:
            raise ValidationError('Wallet name is required for wallet payments.')

    def __str__(self):
        return f"{self.payment_method} - ₹{self.amount} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
