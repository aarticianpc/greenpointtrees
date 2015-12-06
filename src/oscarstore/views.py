from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from oscar.core.loading import get_model, get_class
from paypal.express.views import RedirectView
from paypal.express.exceptions import (
    EmptyBasketException, MissingShippingAddressException,
    MissingShippingMethodException, InvalidBasket)


from paypal.express.facade import (
    get_paypal_url, fetch_transaction_details, confirm_transaction)

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductImage = get_model('catalogue', 'ProductImage')

# Load views dynamically
PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')

ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Selector = get_class('partner.strategy', 'Selector')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')

def main(request):
    selector = Selector()
    strategy = selector.strategy(request=request, user=request.user)
    # print dir(ProductImage)
    products = Product.objects.all()

    product_rows = [[]];
    for product in products:
        purchase_info = strategy.fetch_for_product(product=product)
        product.price = purchase_info.price
        if(len(product_rows)==0 or len(product_rows[-1]) >=2):
            product_rows.append([])
        product_rows[-1].append(product);
    # return render(request, 'product-oscar.html', {'product_rows': product_rows})
    return render(request, 'product.html', {'product_rows': product_rows})


class RedirectView(RedirectView):
    def _get_redirect_url(self, basket, **kwargs):
        if basket.is_empty:
            raise EmptyBasketException()

        params = {
            'basket': basket,
            'shipping_methods': []          # setup a default empty list
        }                                   # to support no_shipping

        user = self.request.user
        if self.as_payment_method:
            print 'as payment method'
            if basket.is_shipping_required():
                print 'is shipping required'
                # Only check for shipping details if required.
                shipping_addr = self.get_shipping_address(basket)
                if not shipping_addr:
                    raise MissingShippingAddressException()

                shipping_method = self.get_shipping_method(
                    basket, shipping_addr)
                if not shipping_method:
                    raise MissingShippingMethodException()

                params['shipping_address'] = shipping_addr
                params['shipping_method'] = shipping_method
                params['shipping_methods'] = []

        else:
            # Maik doubts that this code ever worked. Assigning
            # shipping method instances to Paypal params
            # isn't going to work, is it?
            shipping_addr = self.get_shipping_address(basket)
            if not shipping_addr:
                raise MissingShippingAddressException()

            shipping_method = self.get_shipping_method(
                basket, shipping_addr)
            if not shipping_method:
                raise MissingShippingMethodException()

            params['shipping_address'] = shipping_addr
            params['shipping_method'] = shipping_method
            print shipping_method, 'canhho'
            # shipping_methods = Repository().get_shipping_methods(
            #     user=user, basket=basket, request=self.request)
            # params['shipping_methods'] = shipping_methods
            params['shipping_methods'] = []
        if settings.DEBUG:
            # Determine the localserver's hostname to use when
            # in testing mode
            params['host'] = self.request.META['HTTP_HOST']

        if user.is_authenticated():
            params['user'] = user

        params['paypal_params'] = self._get_paypal_params(basket)

        return get_paypal_url(**params)

    def _get_paypal_params(self, basket):
        shipping_address = self.get_shipping_address(basket)
        if (shipping_address):
            # active_address_fields
            return {
                'PAYMENTREQUEST_0_SHIPTONAME' : shipping_address.name, 
                'PAYMENTREQUEST_0_SHIPTOSTREET': shipping_address.line1,
                'PAYMENTREQUEST_0_SHIPTOSTREET2': shipping_address.line2,
                'PAYMENTREQUEST_0_SHIPTOCITY' : shipping_address.city, 
                'PAYMENTREQUEST_0_SHIPTOSTATE' : shipping_address.state,
                'PAYMENTREQUEST_0_SHIPTOZIP' : shipping_address.postcode, 
                'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE' :  shipping_address.country_id
            }
        else:
            return {}
        """
        Return any additional PayPal parameters
        """