from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Handles flash messages
from users.models import User
from customer.models import Customer, Cart, Address, Bill, Offer
from restaurant.models import Store, Slider, StoreCategory, Food, Foodcategory
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from customer.models import Address  # Replace with your actual model



@login_required(login_url='/login/')
def index(request):
    sliders = Slider.objects.all()
    store_categories = StoreCategory.objects.all()
    stores = Store.objects.all()  # Fixed typo: 'object' to 'objects'
    context = {
        "store_categories": store_categories,
        "stores": stores,
        "sliders": sliders,
    }
    return render(request, 'web/index.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            messages.error(request, 'Invalid email or password')
            context = {
                'error': True,
                'message': 'Invalid email or password',
            }
            return render(request, 'web/login.html', context=context)
    else:
        return render(request, 'web/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message': 'Email already exists',
            }
            return render(request, 'web/register.html', context=context)
        else:
            # Create a new user and associated customer
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True  # Corrected placement of this line
            )
            user.save()

            customer = Customer.objects.create(user=user)
            customer.save()

            return HttpResponseRedirect(reverse('web:login'))  # Redirect to login page
    else:
        return render(request, 'web/register.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('web:login'))


@login_required(login_url='/login/')
def restaurants(request, id):
    store_categories = StoreCategory.objects.all()
    store_category = get_object_or_404(StoreCategory, id=id)
    stores = Store.objects.filter(category=store_category)
    context = {
        "store_categories": store_categories,
        "stores": stores,
    }
    return render(request, 'web/restaurants.html', context=context)


@login_required(login_url='/login/')
def singlerestaurant(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    store = get_object_or_404(Store, id=id)
    foods = Food.objects.filter(store=store)
    foodcategory = Foodcategory.objects.filter(store=store)
    carts = Cart.objects.filter(store=store, customer=customer)
    cart_count = carts.count()
    cart_amount = carts.aggregate(Sum('amount'))['amount__sum']
    cart_quantities = {cart.product: cart.quantity for cart in carts}
    prod_with_qty = [(food, cart_quantities.get(food, 0)) for food in foods]

    context = {
        "store": store,
        "foods": foods,
        "foodcategory": foodcategory,
        "customer": customer,
        "prod_with_qty": prod_with_qty,
        "cart_count": cart_count,
        "cart_amount": cart_amount,
    }

    return render(request, 'web/singleresturant.html', context=context)


@login_required(login_url='/login/')
def add_cart(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    food = get_object_or_404(Food, id=id)
    store = food.store
    
    cart = Cart.objects.create(
        customer=customer,
        product=food,
        store=store,
        amount=food.price,
        quantity=1
    )
    cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def plus_cart(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    food = get_object_or_404(Food, id=id)
    store = food.store

    cart = Cart.objects.get(store=store, customer=customer)

    # Update cart fields
    cart.quantity += 1
    cart.amount += food.price
    cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def mines_cart(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    food = get_object_or_404(Food, id=id)
    store = food.store

    cart = Cart.objects.get(store=store, customer=customer)

    # Update cart fields
    cart.quantity -= 1
    cart.amount -= food.price
    cart.save()
    
    if cart.quantity == 0:
        cart.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login/')
def cart(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = Cart.objects.filter(customer=customer)

    if cart_items.exists():
        cart_amount = cart_items.aggregate(Sum('amount'))['amount__sum']
        store = cart_items.first().store
    else:
        store = None
        cart_amount = 0

    deliverycharges  = 50
    discount = 0

    # Handle CartBill
    if Bill.objects.filter(customer=customer).exists():
        cartbill = Bill.objects.get(customer=customer)
        cartbill.itemtotal = cart_amount
        cartbill.final_amount = cart_amount + deliverycharges  - float(cartbill.offerapplied)
        cartbill.save()
    else:
        cartbill = Bill.objects.create(
            customer=customer,
            itemtotal=cart_amount,
            deliverycharges =deliverycharges ,
            final_amount=cart_amount + deliverycharges ,
            offerapplied=0,
            address=None
        )

    error_message = None

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = Offer.objects.get(code=code)
            if offer.is_percentage:
                discount = round((offer.discount / 100) * cart_amount)
            else:
                discount = offer.discount

                cartbill.offerapplied = discount
                cartbill.final_amount = cart_amount + deliverycharges  - float(discount)
                cartbill.save()
                success_message = 'Coupon code applied successfully!'
        except Offer.DoesNotExist:
            error_message = 'Invalid coupon code. Please try again.'

    address = cartbill.address

    context = {
        "customer": customer,
        "cart_items": cart_items,
        "cart_amount": cart_amount,
        "store": store,
        "cartbill": cartbill,
        "address": address,
        "discount": discount,
        "error_message": error_message,
        "success_message": success_message if 'success_message' in locals() else None,
    }

    return render(request, 'web/cart.html', context=context)

@login_required(login_url='/login/')
def add_address(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':  # Corrected to 'POST'
        city = request.POST.get('address')
        apartment = request.POST.get('apartment')  # Removed extra space
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        landmark = request.POST.get('landmark')
        address_type = request.POST.get('address_type')
         
        address = Address.objects.create(
            customer=customer,
            address=city,
            appartement=apartment,
            name=name,
            phone=phone,
            landmark=landmark,
            address_type=address_type,
        )
        address.save()
        return HttpResponseRedirect(reverse('web:address'))
    else:
        return render(request, 'web/address.html')


def address(request):
    customer = Customer.objects.get(user=request.user)
    
    address=Address.objects.filter(customer=customer)

    context = {
        "address": address,
    }

    return render(request, 'web/address_two.html',context=context)


def delete_item(request, item_id):

    item = Address.objects.get(id=item_id)
    item.delete()
    return HttpResponseRedirect(reverse('web:address'))




def set_address(request, item_id):
    customer = Customer.objects.get(user=request.user)

    item = Address.objects.get(id=item_id)
    bill = Bill.objects.filter(customer=customer).first()
    bill.address = item
    bill.save()

    return HttpResponseRedirect(reverse('web:cart'))

def checkout(request):
    customer = Customer.objects.get(user=request.user)
    
    try:
        cart_bill = Bill.objects.get(customer=customer)
    except Bill.DoesNotExist:
        cart_bill = None


        context = {
            'itemtotal':cart_bill.itemtotal or 0,
            'offerapplied':cart_bill.offerapplied or 0,
            'deliverycharges':cart_bill.deliverycharges or 0,
            'final_amount':cart_bill.final_amount or 0,



        }


    return render(request, 'web/checkout.html',context=context) 

   






