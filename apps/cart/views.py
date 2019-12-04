from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def cart(request):
    guest_cart = 1
    return render(request, 'cart.html', {'guest_cart': guest_cart})
