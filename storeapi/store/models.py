import os
import time
import datetime
from PIL import Image
from django.db import models
from threading import Thread

global updateting_images
updateting_images = False

def resize_upload_images (image_path):

    global updateting_images
    updateting_images = True

    # Open original image
    img = Image.open (image_path)
    width, height = img.size

    # Resize image for full size
    new_img = img.resize((700, int(700*height/width)))
    new_img.save (image_path)

    # Resize image for regular size
    new_img = img.resize((350, int(350*height/width)))
    regular_path = str(image_path).replace("full-size", "")
    new_img.save (regular_path)

    # Move to images folder
    parent_folder = os.path.dirname(os.path.dirname(__file__))
    images_folder = os.path.join (parent_folder, "imgs")
    os.chdir (images_folder)

    # make commit and upload to github
    time_str = str(datetime.datetime.now())[:22]

    os.system (f'git add -A')
    os.system (f'git commit -m "update images {time_str}"')
    os.system (f'git push origin master')

    updateting_images = False

class KeaganBrand (models.Model):

    # Database
    name = models.CharField(max_length=20)
    details = models.TextField(max_length=500, default=None)
    image = models.ImageField (blank=True, upload_to='imgs/brands', default=None)

    # Show brand name in form
    def __str__ (self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "brands"
        verbose_name = "brand"

class KeaganProduct (models.Model):
    # database
    code = models.CharField (max_length=15)
    brand = models.ForeignKey (KeaganBrand, on_delete=models.CASCADE, null=True)
    name = models.CharField (max_length=40)
    price = models.FloatField ()
    image = models.ImageField (blank=True, upload_to='imgs/products/full-size', default=None)
    sizes = models.CharField (max_length=100, verbose_name="Sizes (separted by commas)")

    # Show product code, brand, namd and price, in form
    def __str__ (self):

        # Format product price
        if (len(str(self.price).split(".")[1]) == 1): 
            price_formated = f"{self.price}0"
        else:
            price_formated = f"{self.price}"

        return f"{self.code} ({self.brand}, {self.name}, {price_formated})" 

    # Do this when data is saving (rewrtite the save function)
    def save (self):

        # Call to default save function
        super().save()

        # Skip test recods
        if "test" in self.name:
            return None

        # Resize and upload image
        while True:
            if updateting_images:
                time.sleep (1)
                continue
            thread_obj = Thread (target=resize_upload_images, args=(self.image.path,))
            thread_obj.start ()
            break
            # resize_upload_images (self.image.path)

    class Meta:
        verbose_name_plural = "products"
        verbose_name = "product"

class KeaganBest (models.Model):
    
    # Database
    product = models.ForeignKey (KeaganProduct, on_delete=models.CASCADE, null=True)

    # Show brand name in form
    def __str__ (self):
        return f"{self.product}"

    class Meta:
        verbose_name_plural = "best products"
        verbose_name = "best product"

class KeaganNewProductsCategories (models.Model):
    
    # Database
    name = models.CharField (max_length=50)
    details = models.TextField(max_length=1000, default=None)

    # Show brand name in form
    def __str__ (self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "new products categories"
        verbose_name = "new products category"


class KeaganNewProduct (models.Model):
    # database
    category = models.ForeignKey (KeaganNewProductsCategories, on_delete=models.CASCADE, null=True)
    name = models.CharField (max_length=40)
    price = models.FloatField ()
    image = models.ImageField (blank=True, upload_to='imgs/products/full-size', default=None)

    # Show product code, brand, namd and price, in form
    def __str__ (self):

        # Format product price
        if (len(str(self.price).split(".")[1]) == 1): 
            price_formated = f"{self.price}0"
        else:
            price_formated = f"{self.price}"

        return f"{self.id} ({self.category}, {self.name}, {price_formated})" 

    # Do this when data is saving (rewrtite the save function)
    def save (self):

        # Call to default save function
        super().save()

        # Skip test recods
        if "test" in self.name:
            return None

        # Resize and upload image
        while True:
            if updateting_images:
                time.sleep (1)
                continue
            thread_obj = Thread (target=resize_upload_images, args=(self.image.path,))
            thread_obj.start ()
            break
            # resize_upload_images (self.image.path)

    class Meta:
        verbose_name_plural = "new products"
        verbose_name = "new product"