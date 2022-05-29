from distutils.command.upload import upload
from django.db import models
from PIL import Image

class keagansklosetboutique_brand (models.Model):

    # Database
    name = models.CharField(max_length=20)
    details = models.TextField(max_length=500, default=None)
    image = models.ImageField (blank=True, upload_to='brands', default=None)

    # Show brand name in form
    def __str__ (self):
        return f"{self.name}"


class keagansklosetboutique_product (models.Model):
    # database
    code = models.CharField (max_length=15)
    brand = models.ForeignKey (keagansklosetboutique_brand, on_delete=models.CASCADE, null=True)
    name = models.CharField (max_length=40)
    price = models.FloatField ()
    image = models.ImageField (blank=True, upload_to='products/full-size', default=None)
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

        # Open original image
        img = Image.open (self.image.path)
        width, height = img.size

        # Resize image for full size
        new_img = img.resize((700, int(700*height/width)))
        new_img.save (self.image.path)

        # Resize image for regular size
        new_img = img.resize((350, int(350*height/width)))
        regular_path = str(self.image.path).replace("full-size", "")
        new_img.save (regular_path)
