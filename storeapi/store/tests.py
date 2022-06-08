import os
from . import models
from django.test import TestCase

static_folder = os.path.join (os.path.dirname(__file__), "static", "store")

class TestKeaganModels (TestCase):

    def __init__ (self,  *args, **kwargs):
        super(TestKeaganModels, self).__init__(*args, **kwargs)

        # Test variables
        self.image = os.path.join(static_folder, "test.jpg")

        self.brand_name = "test brand"
        self.brand_details = "test brand details"
        
        self.product_code = "0001"
        self.product_brand = 1
        self.product_name = "test product"
        self.product_price = 10
        self.product_sizes = "5,6,7"

    # ----- Brand model functions --------------------------------

    def brand_create (self):
        """
        Add a new register to the KeaganBrand model
        """

        # Add a new brand
        brand = models.KeaganBrand (
            name=self.brand_name, 
            details=self.brand_details, 
            image=self.image)
        brand.save()
        return brand
    
    def brand_read (self):
        """
        Chack if register is correctly saved in KeaganBrand model
        """

        # Count the number of brands
        brands = models.KeaganBrand.objects.filter(name=self.brand_name)
        self.assertEqual (len(brands), 1)
        
        # Check brand content
        self.assertEqual (brands[0].name, self.brand_name)
        self.assertEqual (brands[0].details, self.brand_details)
        self.assertEqual (brands[0].image, self.image)

    def brand_update (self):
        """
        Update register in KeaganBrand model and check the changes
        """

        # Get brand
        brand = models.KeaganBrand.objects.filter(name=self.brand_name)[0]

        # Update values
        brand.details = f"{self.brand_details} updated"
        brand.save ()

        # Get brand again
        brand = models.KeaganBrand.objects.filter(name=self.brand_name)[0]

        # Validate updated values
        self.assertEqual (brand.details, f"{self.brand_details} updated")

    def brand_delete (self):
        """
        Delete test register in KeaganBrand
        """

        # Get brand
        brand = models.KeaganBrand.objects.filter(name=self.brand_name)[0]

        # Delete
        brand.delete ()

        # Check if its deleted
        brands = models.KeaganBrand.objects.filter(name=self.brand_name)
        self.assertEqual (len(brands), 0)
    
    # ----- Product model functions --------------------------------

    def product_create (self):
        """
        Add a new register to the KeaganProduct model
        """

        # Add test brand
        brand = self.brand_create ()

        # Add a new product
        product = models.KeaganProduct (
            code=self.product_code,
            brand=brand,
            name=self.product_name,
            price=self.product_price,
            image=self.image,
            sizes=self.product_sizes)
        product.save()

        return product
    
    def product_read (self):
        """
        Chack if register is correctly saved in KeaganProduct model
        """

        # Count the number of products
        products = models.KeaganProduct.objects.filter(name=self.product_name)
        self.assertEqual (len(products), 1)
        
        # Check product content
        self.assertEqual (products[0].code, self.product_code)
        self.assertEqual (products[0].name, self.product_name)
        self.assertEqual (products[0].price, self.product_price)
        self.assertEqual (products[0].image, self.image)
        self.assertEqual (products[0].sizes, self.product_sizes)

    def product_update (self):
        """
        Update register in KeaganProduct model and check the changes
        """

        # Get product
        product = models.KeaganProduct.objects.filter(name=self.product_name)[0]

        # Update values
        product.sizes = "10,11,12"
        product.save ()

        # Get product again
        product = models.KeaganProduct.objects.filter(name=self.product_name)[0]

        # Validate updated values
        self.assertEqual (product.sizes, "10,11,12")

    def product_delete (self):
        """
        Delete test register in KeaganProduct
        """

        # Get product
        product = models.KeaganProduct.objects.filter(name=self.product_name)[0]

        # Delete
        product.delete ()

        # Check if its deleted
        products = models.KeaganProduct.objects.filter(name=self.product_name)
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
        self.assertEqual (best[0].product.code, self.product_code)

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

    def new_product_categories_create (self):
        """
        Add a new register to the KeaganNewProductsCategories model
        """

        # Add a new brand
        category = models.KeaganNewProductsCategories (
            name=self.brand_name, 
            details=self.brand_details)
        category.save()
        return category
    
    def new_product_categories_read (self):
        """
        Chack if register is correctly saved in KeaganNewProductsCategories model
        """

        # Count the number of brands
        categories = models.KeaganNewProductsCategories.objects.filter(name=self.brand_name)
        self.assertEqual (len(categories), 1)
        
        # Check brand content
        self.assertEqual (categories[0].name, self.brand_name)
        self.assertEqual (categories[0].details, self.brand_details)

    def new_product_categories_update (self):
        """
        Update register in KeaganNewProductsCategories model and check the changes
        """

        # Get brand
        category = models.KeaganNewProductsCategories.objects.filter(name=self.brand_name)[0]

        # Update values
        category.details = f"{self.brand_details} updated"
        category.save ()

        # Get brand again
        category = models.KeaganNewProductsCategories.objects.filter(name=self.brand_name)[0]

        # Validate updated values
        self.assertEqual (category.details, f"{self.brand_details} updated")

    def new_product_categories_delete (self):
        """
        Delete test register in KeaganNewProductsCategories
        """

        # Get brand
        category = models.KeaganNewProductsCategories.objects.filter(name=self.brand_name)[0]

        # Delete
        category.delete ()

        # Check if its deleted
        categories = models.KeaganNewProductsCategories.objects.filter(name=self.brand_name)
        self.assertEqual (len(categories), 0)

    # ----- New Product Categories model functions ------------------------------

    def new_product_create (self):
        """
        Add a new register to the KeaganNewProduct model
        """

        # Add test brand
        category = self.new_product_categories_create ()

        # Add a new product
        new_product = models.KeaganNewProduct (
            category=category,
            name=self.product_name,
            price=self.product_price,
            image=self.image)
        new_product.save()

        return new_product
    
    def new_product_read (self):
        """
        Chack if register is correctly saved in KeaganNewProduct model
        """

        # Count the number of products
        new_products = models.KeaganNewProduct.objects.filter(name=self.product_name)
        self.assertEqual (len(new_products), 1)
        
        # Check product content
        self.assertEqual (new_products[0].name, self.product_name)
        self.assertEqual (new_products[0].price, self.product_price)
        self.assertEqual (new_products[0].image, self.image)

    def new_product_update (self):
        """
        Update register in KeaganNewProduct model and check the changes
        """

        # Get product
        new_product = models.KeaganNewProduct.objects.filter(name=self.product_name)[0]

        # Update values
        new_product.price = 20
        new_product.save ()

        # Get product again
        new_product = models.KeaganNewProduct.objects.filter(name=self.product_name)[0]

        # Validate updated values
        self.assertEqual (new_product.price, 20)

    def new_product_delete (self):
        """
        Delete test register in KeaganNewProduct
        """

        # Get product
        new_product = models.KeaganNewProduct.objects.filter(name=self.product_name)[0]

        # Delete
        new_product.delete ()

        # Check if its deleted
        new_products = models.KeaganNewProduct.objects.filter(name=self.product_name)
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

    def test_new_product_categories_crud (self):
        """
        Test KeaganNewProductsCategories model crud
        """
        self.new_product_categories_create ()
        self.new_product_categories_read ()
        self.new_product_categories_update ()
        self.new_product_categories_delete ()

    def test_new_product_crud (self):
        """
        Test KeaganNewProduct model crud
        """
        self.new_product_create ()
        self.new_product_read ()
        self.new_product_update ()
        self.new_product_delete ()
