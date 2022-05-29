from distutils.command.upload import upload
from django.db import models
from PIL import Image

def resizes_images (image_path):
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


class keagan_brand (models.Model):

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

class keagan_product (models.Model):
    # database
    code = models.CharField (max_length=15)
    brand = models.ForeignKey (keagan_brand, on_delete=models.CASCADE, null=True)
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

        # Resize image
        resizes_images (self.image.path)

    class Meta:
        verbose_name_plural = "products"
        verbose_name = "product"

class keagan_best (models.Model):
    
    # Database
    product = models.ForeignKey (keagan_product, on_delete=models.CASCADE, null=True)

    # Show brand name in form
    def __str__ (self):
        return f"{self.product}"

    class Meta:
        verbose_name_plural = "best products"
        verbose_name = "best product"

class keagan_new_products_categories (models.Model):
    
    # Database
    name = models.CharField (max_length=50)
    details = models.TextField(max_length=1000, default=None)

    # Show brand name in form
    def __str__ (self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "new products categories"
        verbose_name = "new products category"


class keagan_new_product (models.Model):
    # database
    category = models.ForeignKey (keagan_new_products_categories, on_delete=models.CASCADE, null=True)
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

        # Resize image
        resizes_images (self.image.path)

    class Meta:
        verbose_name_plural = "new products"
        verbose_name = "new product"