from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.utils import timezone
from .models import (Product, Category, Review, Wishlist,
                     Order, OrderItem, Coupon, Newsletter)
from .forms import ReviewForm, OrderForm

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort')
    categories = Category.objects.all()
    featured = Product.objects.filter(is_featured=True)[:4]

    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category__id=category_id)
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'popular':
        products = products.order_by('-views_count')

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'sort': sort,
        'featured': featured,
        'total_products': products.count(),
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    # Incrémenter les vues
    product.views_count += 1
    product.save()

    related_products = Product.objects.filter(
        category=product.category).exclude(id=id)[:3]
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    form = ReviewForm()
    in_wishlist = False
    already_reviewed = False

    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, product=product).exists()
        already_reviewed = Review.objects.filter(
            user=request.user, product=product).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if already_reviewed:
            messages.warning(request, 'Vous avez déjà laissé un avis.')
            return redirect('product_detail', id=id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Avis ajouté avec succès !')
            return redirect('product_detail', id=id)

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'in_wishlist': in_wishlist,
        'already_reviewed': already_reviewed,
        'rating_range': range(1, 6),
    })

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    # Coupon appliqué
    coupon = request.session.get('coupon')
    discount = 0
    final_total = total
    if coupon:
        discount = total * coupon['discount'] / 100
        final_total = total - discount

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'coupon': coupon,
        'discount': discount,
        'final_total': final_total,
    })

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').upper()
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            if coupon.valid_until and coupon.valid_until < timezone.now().date():
                messages.error(request, 'Ce coupon a expiré.')
            else:
                request.session['coupon'] = {
                    'code': coupon.code,
                    'discount': coupon.discount,
                }
                messages.success(request,
                    f'Coupon "{code}" appliqué : -{coupon.discount}% !')
        except Coupon.DoesNotExist:
            messages.error(request, 'Code coupon invalide.')
    return redirect('cart')

@login_required
def remove_coupon(request):
    if 'coupon' in request.session:
        del request.session['coupon']
        messages.info(request, 'Coupon supprimé.')
    return redirect('cart')

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    if product.stock == 0:
        messages.error(request, 'Ce produit est en rupture de stock.')
        return redirect('product_list')
    cart = request.session.get('cart', {})
    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1
    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" ajouté au panier !')
    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    messages.warning(request, 'Produit supprimé du panier.')
    return redirect('cart')

@login_required
def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=id)
    if str(id) in cart:
        if cart[str(id)] < product.stock:
            cart[str(id)] += 1
        else:
            messages.warning(request, 'Stock insuffisant.')
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        if cart[str(id)] > 1:
            cart[str(id)] -= 1
        else:
            del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def toggle_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    obj, created = Wishlist.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'"{product.name}" retiré des favoris.')
    else:
        messages.success(request, f'"{product.name}" ajouté aux favoris !')
    return redirect('product_detail', id=id)

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Votre panier est vide.')
        return redirect('cart')

    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    coupon_data = request.session.get('coupon')
    discount = 0
    final_total = total
    coupon_obj = None
    if coupon_data:
        discount = total * coupon_data['discount'] / 100
        final_total = total - discount
        try:
            coupon_obj = Coupon.objects.get(code=coupon_data['code'])
        except Coupon.DoesNotExist:
            pass

    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = final_total
            order.discount_amount = discount
            if coupon_obj:
                order.coupon = coupon_obj
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                )
                # Décrémenter le stock
                item['product'].stock -= item['quantity']
                item['product'].save()

            request.session['cart'] = {}
            if 'coupon' in request.session:
                del request.session['coupon']

            messages.success(request,
                f'🎉 Commande #{order.id} passée avec succès !')
            return redirect('order_confirm', id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
        'coupon': coupon_data,
        'form': form,
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_confirm(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    return render(request, 'order_confirm.html', {'order': order})

@login_required
def cancel_order(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request, f'Commande #{order.id} annulée.')
    else:
        messages.error(request,
            'Impossible d\'annuler cette commande.')
    return redirect('order_list')

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            _, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request,
                    'Vous êtes abonné à notre newsletter !')
            else:
                messages.info(request, 'Vous êtes déjà abonné.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))