from django.shortcuts import render
from django.http import HttpResponse
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')

def main(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})
    pass
