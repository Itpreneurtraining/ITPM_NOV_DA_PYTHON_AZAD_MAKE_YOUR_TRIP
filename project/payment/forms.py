from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    cvv = forms.CharField(max_length=4, required=False)

    class Meta:
        model = Payment
        fields = ['name', 'payment_method', 'upi_id', 'card_number', 'bank_name', 'wallet_name']

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')

        if method == 'UPI' and not cleaned_data.get('upi_id'):
            self.add_error('upi_id', 'UPI ID is required for UPI payment.')
        elif method == 'NETBANKING' and not cleaned_data.get('bank_name'):
            self.add_error('bank_name', 'Bank name is required for net banking.')
        elif method == 'CARD':
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Card number is required.')
            if not self.data.get('cvv'):
                self.add_error(None, 'CVV is required for card payment.')

        return cleaned_data
