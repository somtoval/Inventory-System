from django.shortcuts import render

# def dashboard(request):
#     return render(request, 'index.html')


# # AUTHENTICATION
# def signin(request):
#     # Code goes here
#     return render(request, 'signin.html')

# def signout(request):
#     # Code goes here
#     return render(request, 'signout.html')


# # CRUD
# def createProduct(request):
#     # Code goes here
#     return render(request, 'createProduct.html')

# def viewProduct(request):
#     # Code goes here
#     return render(request, 'viewProduct.html')

# def updateProduct(request):
#     # Code goes here
#     return render(request, 'updateProduct.html')

# def deleteProduct(request):
#     # Code goes here
#     return render(request, 'deleteProduct.html')


"""
    This view has a form where by accountant or clerk can key in products
    to be ordered and their quantities and it displays the score 
    and then clicks submit/new button to update the quantities of drug it and then renders the form again
"""
# def order(request):
#     # Code and orderform goes here
#     return render(request, 'order.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Supplier, Product, Transaction
from .forms import SupplierForm, ProductForm, TransactionForm
from django.db.models import Sum, Count

def dashboard(request):
    # Summary data
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()
    total_transactions = Transaction.objects.count()
    total_quantity = Product.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Data for charts
    products = Product.objects.all()
    product_names = [product.name for product in products]
    product_quantities = [product.quantity for product in products]

    transactions = Transaction.objects.all()
    transaction_dates = [transaction.transaction_date.strftime('%Y-%m-%d') for transaction in transactions]
    transaction_quantities = [transaction.quantity for transaction in transactions]

    context = {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_transactions': total_transactions,
        'total_quantity': total_quantity,
        'product_names': product_names,
        'product_quantities': product_quantities,
        'transaction_dates': transaction_dates,
        'transaction_quantities': transaction_quantities,
    }
    return render(request, 'dashboard.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_add(request):
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'form_title': 'Add Product', 'suppliers':suppliers})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    suppliers = Supplier.objects.all()
    print(f'Product: {product.expiration_date}')
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'form_title': 'Edit Product', 'suppliers':suppliers})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form.html', {'form': form, 'form_title': 'Add Supplier'})

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form.html', {'form': form, 'form_title': 'Edit Supplier'})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-transaction_date')
    return render(request, 'transaction_list.html', {'transactions': transactions})

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            # Update product quantity
            product = transaction.product
            product.quantity -= transaction.quantity
            product.save()
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form, 'form_title': 'Add Transaction'})

def login_view(request):
    # Add login logic here
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        # # Handle form submission
        # logout(request)
        pass
    return render(request, 'login.html')
