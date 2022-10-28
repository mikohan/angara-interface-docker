from django.db import models
from PIL import Image, ImageOps
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import ImageFile


# Custom path to upload images
def img_path(instance, filename, *args, **kwargs):
    path = os.path.join(
        "parts",
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        filename,
    )
    return path


def img_path_tmb(instance, filename, *args, **kwargs):
    path = os.path.join(
        "parts",
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        "tmb",
        filename,
    )
    return path


def img_path_old(instance, filename, *args, **kwargs):
    path = os.path.join("old_parts", str(instance.product.one_c_id), filename)
    return path


class OldProductImage(models.Model):
    """Class keep old images by one c id"""

    image = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img150 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img245 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img500 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img800 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    one_c_id = models.IntegerField(null=True, blank=True)

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="old_images",
    )

    class Meta:
        verbose_name = "Старые Фото"
        verbose_name_plural = "Старые Фото"

    def __str__(self):
        return str(self.product.one_c_id)

    def save(self, *args, **kwargs):

        method = Image.ANTIALIAS

        im = Image.open(io.BytesIO(self.image.read()))
        # Checking image size

        imw, imh = im.size

        img_big = ImageOps.fit(
            im, (1920, 1280), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img_big.save(output, format="JPEG", optimize=True, quality=70)
        output.seek(0)
        self.image = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        img150 = ImageOps.fit(
            im, (150, 100), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        img150.save(output, format="JPEG", optimize=True, quality=70)
        output.seek(0)
        self.img150 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # 245
        img245 = ImageOps.fit(
            im, (245, 134), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        img245.save(output, format="JPEG", optimize=True, quality=70)
        output.seek(0)
        self.img245 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        # 245
        img500 = ImageOps.fit(
            im, (500, 334), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        img500.save(output, format="JPEG", optimize=True, quality=70)
        output.seek(0)
        self.img500 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        img800 = ImageOps.fit(
            im, (900, 600), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        img800.save(output, format="JPEG", optimize=True, quality=70)
        output.seek(0)
        self.img800 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        super().save(*args, **kwargs)


###############################################################################
# Product images
class ProductImage(models.Model):
    image = models.ImageField(max_length=255, upload_to=img_path, null=True, blank=True)
    img150 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img245 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img500 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img800 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img245x245 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img150x150 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img500x500 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img800x800 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    main = models.BooleanField(default=False, blank=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_image",
    )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def save(self, *args, **kwargs):
        if self.main == True:
            qs = ProductImage.objects.filter(product=self.product).exclude(id=self.id)
            qs.update(main=False)

        size = ((150, 100), (245, 164), (500, 333), (900, 600), (1280, 860))
        method = Image.ANTIALIAS

        im = Image.open(io.BytesIO(self.image.read()))
        # im = Image.open(self.image)
        imw, imh = im.size
        if imw > 1920:
            img_big = ImageOps.fit(
                im, (1920, 1280), method=method, bleed=0.0, centering=(0.5, 0.5)
            )
            output = io.BytesIO()
            img_big.save(output, format="JPEG", quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{self.image.name}",
                "image/jpeg",
                output.getbuffer().nbytes,
                "utf-8",
                None,
            )

        # Rectangle 150x100
        img150 = ImageOps.fit(
            im, size[0], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img150.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img150 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 150x150
        img150x150 = ImageOps.fit(
            im, (150, 150), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img150x150.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img150x150 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 245x164
        img245 = ImageOps.fit(
            im, size[1], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img245.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img245 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 245x245
        img245x245 = ImageOps.fit(
            im, (245, 245), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img245x245.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img245x245 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 500x333
        img500 = ImageOps.fit(
            im, size[2], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img500.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img500 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 500x500
        img500x500 = ImageOps.fit(
            im, (500, 500), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img500x500.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img500x500 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 900x600
        img800 = ImageOps.fit(
            im, size[3], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img800.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img800 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 900x900
        img800x800 = ImageOps.fit(
            im, (900, 900), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img800x800.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img800x800 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product.slug) + "_" + str(self.id)


###############################################################################
