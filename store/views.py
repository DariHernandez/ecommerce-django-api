import os
import random
from . import models
from django.http import JsonResponse


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

def keagan_product (request, product_id):
    """ Return specific product data """

    """ Get product data """
    product = list(models.KeaganProduct.objects.filter (id=product_id).values())[0]

    """ Get random products """
    random_products = []

    # Get brand data
    brand_id = product["brand_id"]
    brand_name = list(models.KeaganBrand.objects.filter (id=brand_id).values())[0]["name"]

    # Get all products from current brand
    brand_products = list(models.KeaganProduct.objects.filter (brand=brand_id).values())

    # Remove current product from list
    brand_products.remove (product)

    # Select 4 random products
    for _ in range (4):

        # Select random product
        random_product = random.choice(brand_products)

        # Save in list
        random_products.append (random_product)

        # Remove element from list
        brand_products.remove (random_product)

    # Update images urls
    product = list(map(keagan_update_images_links, [product]))[0]

    # Update images urls
    random_products = list(map(keagan_update_images_links, random_products))

    # Format response
    response = {
        "brand": brand_name,
        "product": product,
        "random_products": random_products
    }

    return JsonResponse(response)

def keagan_product_new (request, product_id):
    """ Return specific new product data """

    """ Get product data """
    product = list(models.KeaganNewProduct.objects.filter (id=product_id).values())[0]

    """ Get random products """
    random_products = []

    # Get brand data
    category_id = product["category_id"]
    category_name = list(models.KeaganNewProductCategory.objects.filter (id=category_id).values())[0]["name"]

    # Get all products from current brand
    category_products = list(models.KeaganNewProduct.objects.filter (category=category_id).values())

    # Remove current product from list
    category_products.remove (product)

    # Select 4 random products
    for _ in range (4):

        # Select random product
        random_product = random.choice(category_products)

        # Save in list
        random_products.append (random_product)

        # Remove element from list
        category_products.remove (random_product)

    # Update images urls
    product = list(map(keagan_update_images_links, [product]))[0]

    # Update images urls
    random_products = list(map(keagan_update_images_links, random_products))

    # Format response
    response = {
        "category": category_name,
        "product": product,
        "random_products": random_products
    }

    return JsonResponse(response)
    