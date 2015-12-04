from django.shortcuts import render
from django.http import HttpResponse
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductImage = get_model('catalogue', 'ProductImage')

def main(request):
    # print dir(ProductImage)
    products = Product.objects.all()

    product_rows = [[]];
    for product in products:
        print product.primary_image()
        if(len(product_rows)==0 or len(product_rows[-1]) >=2):
            product_rows.append([])
        product_rows[-1].append(product);
    return render(request, 'product-oscar.html', {'product_rows': product_rows})
