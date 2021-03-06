import os
import time
from PIL import Image
from django.db import models
from threading import Thread
# from . import images_server

global updateting_images
updateting_images = False

app_folder = os.path.dirname (__file__)

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

    # file_name = os.path.basename (image_path)
    # images_server.upload_keagan (test_id="", file_name=file_name)

    updateting_images = False


class KeaganBrand (models.Model):

    # Database
    name = models.CharField(max_length=250)
    details = models.TextField(max_length=500, default=None)
    image = models.ImageField (blank=True, upload_to=f'keagan/brands', default=None, max_length=500)

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
    image = models.ImageField (blank=True, upload_to=f'keagan/products/full-size', default=None, max_length=500)
    sizes = models.CharField (max_length=100, verbose_name="Sizes (separted by commas)", blank=True, null=True)

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

class KeaganNewProductCategory (models.Model):

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
    category = models.ForeignKey (KeaganNewProductCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField (max_length=40)
    price = models.FloatField ()
    image = models.ImageField (blank=True, upload_to=f'keagan/products/full-size', default=None, max_length=500)

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