from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_count')
def cart_count(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)

@register.filter(name='product_total')
def product_total(product, cart):
    return product.price * cart_count(product, cart)

@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    total = 0
    for product in products:
        total += product_total(product, cart)
    return total

@register.filter(name='order_total')
def order_total(num1, num2):
    return num1 * num2
