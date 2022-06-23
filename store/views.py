import os
import stripe
import random
from . import models
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .credentials import credentials


keagan_images_server = "https://darideveloper.pythonanywhere.com/media/keagan"

def index (request):
    """Return basic response in home"""
    response = {
        "status": "running",
        "stores": ["keagan",]
    }
    return JsonResponse(response)

def keagan_update_images_links (product):

    # Get image name
    image = product["image"]
    image_name = os.path.basename (image)
    product["image"] = image_name

    # Add links
    product["image_url_full"] = f"{keagan_images_server}/products/full-size/{image_name}"
    product["image_url"] = f"{keagan_images_server}/products/{image_name}"

    return product

def keagan_get_brand_image_link (brand_image):
    image_name = os.path.basename (brand_image)
    return f"{keagan_images_server}/brands/{image_name}"

def keagan_home (request):
    """Return all data for load home page"""

    # ///// Get and format new products ////////////////////
    new_products_formated = []

    # Get categories
    new_products_categories = list(models.KeaganNewProductCategory.objects.values())
    for new_products_categorie in new_products_categories:
        category_data = {}

        new_products_categorie_id = new_products_categorie["id"]

        # Add variables  to local dict
        category_data["category_name"] = new_products_categorie["name"]
        category_data["category_details"] = new_products_categorie["details"]

        # Get products for current category
        new_products = list(models.KeaganNewProduct.objects.filter (category=new_products_categorie_id).values())

        # Update images urls
        new_products = list(map(keagan_update_images_links, new_products))

        category_data["new_products"] = new_products

        # Save to main dict
        new_products_formated.append (category_data)

    #///// Get and format regular products ////////////////////
    regular_products_formated = []

    # Get brands
    products_brands = list(models.KeaganBrand.objects.values())
    for products_brand in products_brands:
        brand_data = {}

        brand_id = products_brand["id"]

        # Add variables
        brand_data["id"] = brand_id
        brand_data["name"] = products_brand["name"]
        brand_data["details"] = products_brand["details"]
        brand_data["image"] = keagan_get_brand_image_link(products_brand["image"])

        # Get products for current category
        products = list(models.KeaganProduct.objects.filter (brand=brand_id).values())

        # Update images urls
        products = list(map(keagan_update_images_links, products))

        brand_data["products"] = products

        # Save to main dict
        regular_products_formated.append (brand_data)

    #  ///// Get and format best products ////////////////////
    best_products_formated = []

    # Get best products
    best_products = list(models.KeaganBest.objects.values())
    for best_product in best_products:

        best_product_id = best_product["product_id"]

        # Get product data
        product_data = list(models.KeaganProduct.objects.filter (id=best_product_id).values())[0]

        # Get brand name
        brand_data = list(models.KeaganBrand.objects.filter (id=product_data["brand_id"]).values())[0]
        brand_name = brand_data["name"]

        # Add name to product data
        product_data["brand_name"] = brand_name

        best_products_formated.append (product_data)

    # Update images urls
    best_products_formated = list(map(keagan_update_images_links, best_products_formated))

    # Format response
    response = {
        "store": "keagan",
        "new_products": new_products_formated,
        "regular_products": regular_products_formated,
        "best_products": best_products_formated
    }
    return JsonResponse(response, safe=True)

def keagan_category_products (request, brand_name):
    """Return all products from soecific category"""

    # Get brand data
    brand = list(models.KeaganBrand.objects.filter (name=brand_name).values())[0]

    # Get products for current category
    products = list(models.KeaganProduct.objects.filter (brand=brand["id"]).values())

    # Update images urls
    products = list(map(keagan_update_images_links, products))

    # Format response
    response = {
        "brand_name": brand["name"],
        "brand_details": brand["details"],
        "brand_image": brand["image"],
        "products": products
    }

    return JsonResponse(response)

def keagan_payment (request):

    api_key = credentials["keagans"]["secret"]

    web_page = "https://www.keagansklosetboutique.com/product"

    # Set api key
    stripe.api_key = api_key

    # Get product data
    product_code = request.GET ["code"]
    product_quantity = request.GET ["quantity"]
    product_size = request.GET ["size"]
    product = models.KeaganProduct.objects.filter(code=product_code)[0]

    # Create product
    image_name = os.path.basename (str(product.image))
    stripe_product = stripe.Product.create(name=product.name,
                        description=f"{product.name} of {product.brand} brand. Size: {product_size}.",
                        images = [
                            f"{keagan_images_server}/products/full-size/{image_name}",
                            f"{keagan_images_server}/products/{image_name}",
                            ]
                        )

    # Create product price
    stripe_price = stripe.Price.create(
        unit_amount=int(product.price*100),
        currency="usd",
        product=stripe_product["id"],
        tax_behavior="exclusive",
    )

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': stripe_price["id"],
                    'quantity': product_quantity,
                },
            ],
            mode='payment',
            success_url=web_page + '?done=true',
            cancel_url=web_page + f'?code={product_code}',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return HttpResponse(str(e))

    return HttpResponseRedirect(checkout_session.url)
