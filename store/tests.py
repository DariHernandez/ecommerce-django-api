import os
import time
import json
from unicodedata import category
import requests
from . import models
from . import images_server
from django.test import TestCase
from django.urls import reverse



static_folder = os.path.join (os.path.dirname(__file__), "static", "store")
image = os.path.join(static_folder, "test.jpg")

brand_name = "test brand"
brand_details = "test brand details"

product_code = "0001"
product_brand = 1
product_name = "test product"
product_price = 10
product_sizes = "5,6,7"

class TestKeaganModels (TestCase):
        

    # ----- Brand model functions --------------------------------

    def brand_create (self):
        """
        Add a new register to the KeaganBrand model
        """

        # Add a new brand
        brand = models.KeaganBrand (
            name=brand_name, 
            details=brand_details, 
            image=image)
        brand.save()
        return brand
    
    def brand_read (self):
        """
        Chack if register is correctly saved in KeaganBrand model
        """

        # Count the number of brands
        brands = models.KeaganBrand.objects.filter(name=brand_name)
        self.assertEqual (len(brands), 1)
        
        # Check brand content
        self.assertEqual (brands[0].name, brand_name)
        self.assertEqual (brands[0].details, brand_details)
        self.assertEqual (brands[0].image, image)

    def brand_update (self):
        """
        Update register in KeaganBrand model and check the changes
        """

        # Get brand
        brand = models.KeaganBrand.objects.filter(name=brand_name)[0]

        # Update values
        brand.details = f"{brand_details} updated"
        brand.save ()

        # Get brand again
        brand = models.KeaganBrand.objects.filter(name=brand_name)[0]

        # Validate updated values
        self.assertEqual (brand.details, f"{brand_details} updated")

    def brand_delete (self):
        """
        Delete test register in KeaganBrand
        """

        # Get brand
        brand = models.KeaganBrand.objects.filter(name=brand_name)[0]

        # Delete
        brand.delete ()

        # Check if its deleted
        brands = models.KeaganBrand.objects.filter(name=brand_name)
        self.assertEqual (len(brands), 0)
    
    # ----- Product model functions --------------------------------

    def product_create (self, name=product_name, brand=None):
        """
        Add a new register to the KeaganProduct model
        """

        # Add test brand
        if not brand:
            brand = self.brand_create ()

        # Add a new product
        product = models.KeaganProduct (
            code=product_code,
            brand=brand,
            name=name,
            price=product_price,
            image=image,
            sizes=product_sizes)
        product.save()

        return product
    
    def product_read (self):
        """
        Chack if register is correctly saved in KeaganProduct model
        """

        # Count the number of products
        products = models.KeaganProduct.objects.filter(name=product_name)
        self.assertEqual (len(products), 1)
        
        # Check product content
        self.assertEqual (products[0].code, product_code)
        self.assertEqual (products[0].name, product_name)
        self.assertEqual (products[0].price, product_price)
        self.assertEqual (products[0].image, image)
        self.assertEqual (products[0].sizes, product_sizes)

    def product_update (self):
        """
        Update register in KeaganProduct model and check the changes
        """

        # Get product
        product = models.KeaganProduct.objects.filter(name=product_name)[0]

        # Update values
        product.sizes = "10,11,12"
        product.save ()

        # Get product again
        product = models.KeaganProduct.objects.filter(name=product_name)[0]

        # Validate updated values
        self.assertEqual (product.sizes, "10,11,12")

    def product_delete (self):
        """
        Delete test register in KeaganProduct
        """

        # Get product
        product = models.KeaganProduct.objects.filter(name=product_name)[0]

        # Delete
        product.delete ()

        # Check if its deleted
        products = models.KeaganProduct.objects.filter(name=product_name)
        self.assertEqual (len(products), 0)

    # ----- Best model functions --------------------------------

    def best_create (self):
        """
        Add a new register to the KeaganBest model
        """

        # Add test product
        product = self.product_create ()

        # Add a new product
        best = models.KeaganBest (product=product)
        best.save()
    
    def best_read (self):
        """
        Chack if register is correctly saved in KeaganBest model
        """

        # Count the number of products
        best = models.KeaganBest.objects.all()
        self.assertEqual (len(best), 1)
        
        # Check product content
        self.assertEqual (best[0].product.code, product_code)

    def best_delete (self):
        """
        Delete test register in KeaganBest
        """

        # Get product
        best = models.KeaganBest.objects.all()[0]

        # Delete
        best.delete ()

        # Check if its deleted
        bests = models.KeaganBest.objects.all()
        self.assertEqual (len(bests), 0)

    # ----- New Product Categories model functions --------------------------------

    def new_product_category_create (self):
        """
        Add a new register to the KeaganNewProductCategory model
        """

        # Add a new brand
        category = models.KeaganNewProductCategory (
            name=brand_name, 
            details=brand_details)
        category.save()
        return category
    
    def new_product_category_read (self):
        """
        Chack if register is correctly saved in KeaganNewProductCategory model
        """

        # Count the number of brands
        categories = models.KeaganNewProductCategory.objects.filter(name=brand_name)
        self.assertEqual (len(categories), 1)
        
        # Check brand content
        self.assertEqual (categories[0].name, brand_name)
        self.assertEqual (categories[0].details, brand_details)

    def new_product_category_update (self):
        """
        Update register in KeaganNewProductCategory model and check the changes
        """

        # Get brand
        category = models.KeaganNewProductCategory.objects.filter(name=brand_name)[0]

        # Update values
        category.details = f"{brand_details} updated"
        category.save ()

        # Get brand again
        category = models.KeaganNewProductCategory.objects.filter(name=brand_name)[0]

        # Validate updated values
        self.assertEqual (category.details, f"{brand_details} updated")

    def new_product_category_delete (self):
        """
        Delete test register in KeaganNewProductCategory
        """

        # Get brand
        category = models.KeaganNewProductCategory.objects.filter(name=brand_name)[0]

        # Delete
        category.delete ()

        # Check if its deleted
        categories = models.KeaganNewProductCategory.objects.filter(name=brand_name)
        self.assertEqual (len(categories), 0)

    # ----- New Product Categories model functions ------------------------------

    def new_product_create (self, name=product_name, category=None):
        """
        Add a new register to the KeaganNewProduct model
        """

        # Add test brand
        if not category:
            category = self.new_product_category_create ()

        # Add a new product
        new_product = models.KeaganNewProduct (
            category=category,
            name=name,
            price=product_price,
            image=image)
        new_product.save()

        return new_product
    
    def new_product_read (self):
        """
        Chack if register is correctly saved in KeaganNewProduct model
        """

        # Count the number of products
        new_products = models.KeaganNewProduct.objects.filter(name=product_name)
        self.assertEqual (len(new_products), 1)
        
        # Check product content
        self.assertEqual (new_products[0].name, product_name)
        self.assertEqual (new_products[0].price, product_price)
        self.assertEqual (new_products[0].image, image)

    def new_product_update (self):
        """
        Update register in KeaganNewProduct model and check the changes
        """

        # Get product
        new_product = models.KeaganNewProduct.objects.filter(name=product_name)[0]

        # Update values
        new_product.price = 20
        new_product.save ()

        # Get product again
        new_product = models.KeaganNewProduct.objects.filter(name=product_name)[0]

        # Validate updated values
        self.assertEqual (new_product.price, 20)

    def new_product_delete (self):
        """
        Delete test register in KeaganNewProduct
        """

        # Get product
        new_product = models.KeaganNewProduct.objects.filter(name=product_name)[0]

        # Delete
        new_product.delete ()

        # Check if its deleted
        new_products = models.KeaganNewProduct.objects.filter(name=product_name)
        self.assertEqual (len(new_products), 0)

    # ----- Test functions --------------------------------

    def test_brand_curd (self):
        """
        Test KeaganBrand model crud
        """
        self.brand_create ()
        self.brand_read ()
        self.brand_update ()
        self.brand_delete ()

    def test_product_curd (self):
        """
        Test KeaganProduct model crud
        """
        self.product_create ()
        self.product_read ()
        self.product_update ()
        self.product_delete ()

    def test_best_curd (self):
        """
        Test KeaganBest model crud
        """
        self.best_create ()
        self.best_read ()
        self.best_delete ()

    def test_new_product_category_crud (self):
        """
        Test KeaganNewProductCategory model crud
        """
        self.new_product_category_create ()
        self.new_product_category_read ()
        self.new_product_category_update ()
        self.new_product_category_delete ()

    def test_new_product_crud (self):
        """
        Test KeaganNewProduct model crud
        """
        self.new_product_create ()
        self.new_product_read ()
        self.new_product_update ()
        self.new_product_delete ()

class TestImageServer (TestCase):

    def test_keagan (self):
        """
        Download sample image and upload to github
        """
        now = time.time()

        # Urls and paths
        image_url = "https://www.darideveloper.com/imgs/logo.png"
        parent_folder = os.path.dirname(__file__)
        image_path = os.path.join (parent_folder, "static", "store", "imgs_keagan", f"test-img{now}.png")

        # Download sample image
        res = requests.get (image_url)
        res.raise_for_status()
        file = open (image_path, "wb")
        for chunk in res.iter_content(100000):
            file.write (chunk)
        file.close()

        # Upload new image to github
        images_server.upload_keagan (test_id=int(now), test_start=True)

        # Delete image
        os.remove (image_path)

        # Delete image from github
        images_server.upload_keagan (test_id=int(now), test_start=False)

class TestApi (TestCase):

    def test_index (self):
        """
        Test the main endpoint of the api
        """

        stores = ["keagan"]

        # Get response
        response = self.client.get(reverse('store:index'))
        self.assertEqual (response.status_code, 200)

        # Check response content
        json_data = json.loads(response.content)
        self.assertEqual (json_data["stores"], stores)

    def test_keagan_home (self):
        """Test home data retuned for the keagan_home endpoint"""

        # Save sample data
        test_keagan_models = TestKeaganModels ()
        test_keagan_models.new_product_create ()
        test_keagan_models.best_create ()
        
        # Get response
        response = self.client.get(reverse('store:keagan_home'))
        self.assertEqual (response.status_code, 200)

        # Check general response content
        json_data = json.loads(response.content)
        self.assertIn ("new_products", json_data)
        self.assertIn ("regular_products", json_data)
        self.assertIn ("best_products", json_data)

        # Check new products
        new_products = json_data["new_products"]
        self.assertGreaterEqual (len(new_products), 1)
        
        new_products_frist = new_products[0]
        self.assertEqual (new_products_frist["category_name"], brand_name)
        self.assertEqual (new_products_frist["category_details"], brand_details)

        new_products_frist_product = new_products_frist["new_products"][0]
        self.assertEqual (new_products_frist_product["name"], product_name)
        self.assertEqual (new_products_frist_product["price"], product_price)

        # Check regular products
        regular_products = json_data["regular_products"]
        self.assertGreaterEqual (len(regular_products), 1)

        regular_products_first_category = regular_products[0]
        self.assertEqual (regular_products_first_category["name"], brand_name)
        self.assertEqual (regular_products_first_category["details"], brand_details)
        
        regular_products_first_product = regular_products_first_category["products"][0]
        self.assertEqual (regular_products_first_product["code"], product_code)
        self.assertEqual (regular_products_first_product["name"], product_name)
        self.assertEqual (regular_products_first_product["price"], product_price)
        self.assertEqual (regular_products_first_product["sizes"], product_sizes)

        # Check best product
        best_product = json_data["best_products"][0]
        self.assertEqual (best_product["code"], product_code)
        self.assertEqual (best_product["name"], product_name)
        self.assertEqual (best_product["price"], product_price)
        self.assertEqual (best_product["sizes"], product_sizes)


    def test_keagan_category_products (self):
        """Test category data retuned for the keagan_category_products endpoint"""

        # Save sample data
        test_keagan_models = TestKeaganModels ()
        test_keagan_models.product_create ()

        # Get response
        response = self.client.get(reverse('store:keagan_category_products', kwargs={"brand_id":1}))
        self.assertEqual (response.status_code, 200)

        # Check general response content
        json_data = json.loads(response.content)
        self.assertGreaterEqual (len(json_data), 2)

        # Check brand data
        self.assertEqual (json_data["brand_name"], brand_name)
        self.assertEqual (json_data["brand_details"], brand_details)

        # Check product data
        product = json_data["products"][0]
        self.assertEqual (product["code"], product_code)
        self.assertEqual (product["name"], product_name)
        self.assertEqual (product["price"], product_price)
        self.assertEqual (product["sizes"], product_sizes)

    def test_keagan_product (self):
        """Test product data retuned for the keagan_product endpoint"""

        main_product_name = "test main product"
        related_product_name = "test related product"

        # Save sample data
        test_keagan_models = TestKeaganModels ()
        brand = test_keagan_models.brand_create ()
        product = test_keagan_models.product_create (main_product_name, brand)
        for product_num in range (1,5):
            test_keagan_models.product_create (f"{related_product_name} {product_num}", brand)

        # Get response
        response = self.client.get(reverse('store:keagan_product', kwargs={"product_id":product.id}))
        self.assertEqual (response.status_code, 200)

        # Check general response content
        json_data = json.loads(response.content)
        self.assertEqual (json_data["brand"], brand_name)

        # Check main product data
        product = json_data["product"]
        self.assertEqual (product["code"], product_code)
        self.assertEqual (product["name"], main_product_name)
        self.assertEqual (product["price"], product_price)
        self.assertEqual (product["sizes"], product_sizes)

        # Check random products data
        random_products = json_data["random_products"]
        self.assertEqual (len(random_products), 4)
        random_products_first = random_products[1]
        self.assertEqual (random_products_first["code"], product_code)
        self.assertIn (related_product_name, random_products_first["name"])
        self.assertEqual (random_products_first["price"], product_price)
        self.assertEqual (random_products_first["sizes"], product_sizes)

    def test_keagan_product_new (self):
        """Test product data retuned for the keagan_product_new endpoint"""

        main_product_name = "test main product"
        related_product_name = "test related product"

        # Save sample data
        test_keagan_models = TestKeaganModels ()
        category = test_keagan_models.new_product_category_create ()
        product = test_keagan_models.new_product_create (main_product_name, category)
        for product_num in range (1,5):
            test_keagan_models.new_product_create (f"{related_product_name} {product_num}", category)

        # Get response
        response = self.client.get(reverse('store:keagan_product_new', kwargs={"product_id":product.id}))
        self.assertEqual (response.status_code, 200)

        # Check general response content
        json_data = json.loads(response.content)
        self.assertEqual (json_data["category"], brand_name)

        # Check main product data
        product = json_data["product"]
        self.assertEqual (product["name"], main_product_name)
        self.assertEqual (product["price"], product_price)

        # Check random products data
        random_products = json_data["random_products"]
        self.assertEqual (len(random_products), 4)
        random_products_first = random_products[1]
        self.assertIn (related_product_name, random_products_first["name"])
        self.assertEqual (random_products_first["price"], product_price)





    
