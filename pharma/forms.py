from django import forms
from .models import Supplier, Product, Transaction

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'expiration_date', 'supplier']

    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     self.fields['expiration_date'].widget.attrs['class'] = 'form-control'
    #     self.fields['supplier'].widget.attrs['class'] = 'form-control'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'quantity']