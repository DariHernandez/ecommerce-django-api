import random
from django.shortcuts import render
from django.http import JsonResponse
from . import models

def index (request):
    """Return basic response in home"""
    response = {
        "status": "running",
        "stores": ["keagan",]
    }
    return JsonResponse(response)

def keagan_home (request):
    """Return all data for load home page"""

    """ Get and format new products """
    new_products_formated = []

    # Get categories
    new_products_categories = list(models.keagan_new_products_categories.objects.values())
    for new_products_categorie in new_products_categories:
        category_data = {}

        new_products_categorie_id = new_products_categorie["id"]

        # Add variables  to local dict
        category_data["category_name"] = new_products_categorie["name"]
        category_data["category_details"] = new_products_categorie["details"]

        # Get products for current category
        new_products = list(models.keagan_new_product.objects.filter (category=new_products_categorie_id).values())
        category_data["new_products"] = new_products

        # Save to main dict
        new_products_formated.append (category_data)

    """ Get and format regular products """
    regular_products_formated = []

    # Get brands
    products_brands = list(models.keagan_brand.objects.values())
    for products_brand in products_brands:
        brand_data = {}

        brand_id = products_brand["id"]

        # Add variables
        brand_data["id"] = brand_id
        brand_data["name"] = products_brand["name"]
        brand_data["details"] = products_brand["details"]
        brand_data["image"] = products_brand["image"]

        # Get products for current category
        products = list(models.keagan_product.objects.filter (brand=brand_id).values())[0:4]
        brand_data["products"] = products

        # Save to main dict
        regular_products_formated.append (brand_data)
    
    """ Get and format best products """
    best_products_formated = []

    # Get best products
    best_products = list(models.keagan_best.objects.values())
    for best_product in best_products:

        best_product_id = best_product["id"]

        # Get product data
        product_data = list(models.keagan_product.objects.filter (id=best_product_id).values())[0]
        best_products_formated.append (product_data)

    # Format response
    response = {
        "store": "keagan",
        "new_products": new_products_formated,
        "regular_products": regular_products_formated,
        "best_products": best_products_formated
    }
    return JsonResponse(response, safe=True)

def keagan_category_products (request, brand_id):
    """Return all products from soecific category"""

    # Get brand data
    brand = list(models.keagan_brand.objects.filter (id=brand_id).values())[0]

    # Get products for current category
    products = list(models.keagan_product.objects.filter (brand=brand_id).values())

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
    product = list(models.keagan_product.objects.filter (id=product_id).values())[0]

    """ Get random products """
    random_products = []

    # Get brand data
    brand_id = product["brand_id"]
    brand_name = list(models.keagan_brand.objects.filter (id=brand_id).values())[0]["name"]

    # Get all products from current brand
    brand_products = list(models.keagan_product.objects.filter (brand=brand_id).values())

    # Remove current product from list
    brand_products.remove (product)

    # Select 4 random products
    for _ in range (4):

        # Select random product
        random_index = random.randint(1, len(brand_products)-1)
        random_product = brand_products[random_index]

        # Save in list
        random_products.append (random_product)

        # Remove element from list
        brand_products.remove (random_product)


    # Format response
    response = {
        "brand": brand_name,
        "product": product,
        "random_products": random_products
    }

    return JsonResponse(response)
    