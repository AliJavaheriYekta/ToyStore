from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from store.forms import CommentForm
from store.models import Product, Comment, Category


@login_required
def product_index(request):
    available_quantity = F('stock')
    products = Product.objects.annotate(available_quantity=available_quantity).order_by("-created_at")
    context = {
        "products": products,
    }
    return render(request, "store/index.html", context)


def product_category(request, category):
    available_quantity = F('stock')
    products = Product.objects.annotate(available_quantity=available_quantity).filter(
        category__name__contains=category
    ).order_by("-created_at")
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "store/category.html", context)


def product_category_detail(request, slug):
    available_quantity = F('stock')
    products = Product.objects.annotate(available_quantity=available_quantity).filter(
        category__slug=slug
    ).order_by("-created_at")
    category = Category.objects.filter(slug=slug)
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "store/category.html", context)


def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        form = CommentForm()
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(
                    user=request.user,
                    content=form.data["body"],
                    product=product,
                )
                comment.save()
                return HttpResponseRedirect(request.path_info)

        # Retrieve related data
        brand = product.brand
        categories = product.category.all()
        comments = product.comments.filter(is_active=True)
        media_files = product.media.all()

    except Product.DoesNotExist:
        # Handle product not found case (e.g., redirect to 404 page)
        return render(request, '404.html')

    context = {
        'product': product,
        'brand': brand,
        'categories': categories,
        'comments': comments,
        'media_files': media_files
    }

    return render(request, "store/product_detail.html", context)


# @api_view(['POST'])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     if username is not None and password is not None:
#         user = User.objects.create_user(username, password=password)
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key})
#     else:
#         return Response({'error': 'Username and password are required'})
#
