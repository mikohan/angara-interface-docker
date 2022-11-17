from django.db import models
from PIL import Image, ImageOps
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import ImageFile
from django.dispatch import receiver
import pathlib


# Custom path to upload images in webp
def img_path_webp(instance, filename, *args, **kwargs):
    path = os.path.join(
        "parts_webp",
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        filename + ".webp",
    )
    return path


# Custom path for tmp in webp
def img_path_webp_tmb(instance, filename, *args, **kwargs):
    path = os.path.join(
        "parts_webp",
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        "tmb",
        filename + ".webp",
    )
    return path


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


def img_path_old_webp(instance, filename, *args, **kwargs):
    path = os.path.join("old_parts", str(instance.product.one_c_id), filename + ".webp")
    return path


class OldProductImage(models.Model):
    """Class keep old images by one c id"""

    image = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img150 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img245 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img500 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    img800 = models.ImageField(upload_to=img_path_old, null=True, blank=True)
    one_c_id = models.IntegerField(null=True, blank=True)
    image_webp = models.ImageField(upload_to=img_path_old_webp, null=True, blank=True)
    image150_webp = models.ImageField(
        upload_to=img_path_old_webp, null=True, blank=True
    )
    image245_webp = models.ImageField(
        upload_to=img_path_old_webp, null=True, blank=True
    )
    image500_webp = models.ImageField(
        upload_to=img_path_old_webp, null=True, blank=True
    )
    image800_webp = models.ImageField(
        upload_to=img_path_old_webp, null=True, blank=True
    )

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
        ## Webp starts here

        image_webp = ImageOps.fit(
            im, (1920, 1280), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image_webp.save(output, format="WEBP", quality=70)
        output.seek(0)

        self.image_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        image150_webp = ImageOps.fit(
            im, (150, 100), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        image150_webp.save(output, format="webp", optimize=True, quality=70)
        output.seek(0)
        self.image150_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        image245_webp = ImageOps.fit(
            im, (245, 134), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        image245_webp.save(output, format="webp", optimize=True, quality=70)
        output.seek(0)
        self.image245_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        image500_webp = ImageOps.fit(
            im, (500, 333), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        image500_webp.save(output, format="webp", optimize=True, quality=70)
        output.seek(0)
        self.image500_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        image800_webp = ImageOps.fit(
            im, (900, 600), method=method, bleed=0.0, centering=(0.5, 0.4)
        )
        output = io.BytesIO()
        image800_webp.save(output, format="webp", optimize=True, quality=70)
        output.seek(0)
        self.image800_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
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
    """Class contains all images for products"""

    quality_webp = 50
    image = models.ImageField(max_length=255, upload_to=img_path, null=True, blank=True)
    # Webp section
    image_webp = models.ImageField(
        max_length=255, upload_to=img_path_webp, null=True, blank=True
    )
    image150_webp = models.ImageField(
        max_length=255, upload_to=img_path_webp_tmb, null=True, blank=True
    )
    image245_webp = models.ImageField(
        max_length=255, upload_to=img_path_webp_tmb, null=True, blank=True
    )
    image500_webp = models.ImageField(
        max_length=255, upload_to=img_path_webp_tmb, null=True, blank=True
    )
    image800_webp = models.ImageField(
        max_length=255, upload_to=img_path_webp_tmb, null=True, blank=True
    )
    # End webp section
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

        # Saving image into webp 1280x861
        image_webp = ImageOps.fit(
            im, size[4], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image_webp.save(output, format="WEBP", quality=self.quality_webp)
        output.seek(0)

        self.image_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        # Saving image into webp 150
        image150_webp = ImageOps.fit(
            im, size[0], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image150_webp.save(output, format="WEBP", quality=self.quality_webp)
        output.seek(0)

        self.image150_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        # Saving image into webp 245
        image245_webp = ImageOps.fit(
            im, size[1], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image245_webp.save(output, format="WEBP", quality=self.quality_webp)
        output.seek(0)

        self.image245_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        # Saving image into webp 500
        image500_webp = ImageOps.fit(
            im, size[2], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image500_webp.save(output, format="WEBP", quality=self.quality_webp)
        output.seek(0)

        self.image500_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        # Saving image into webp 500
        image800_webp = ImageOps.fit(
            im, size[3], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        image800_webp.save(output, format="WEBP", quality=self.quality_webp)
        output.seek(0)

        self.image800_webp = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/webp",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # saving rect 150
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
        # saving square 150x150
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
@receiver(models.signals.post_delete, sender=ProductImage)
def remove_images(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding MedaFile object is deleted"""
    print(instance.image.path)
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.image_webp:
        if os.path.isfile(instance.image_webp.path):
            os.remove(instance.image_webp.path)
    if instance.image150_webp:
        if os.path.isfile(instance.image150_webp.path):
            os.remove(instance.image150_webp.path)
    if instance.image245_webp:
        if os.path.isfile(instance.image245_webp.path):
            os.remove(instance.image245_webp.path)
    if instance.image500_webp:
        if os.path.isfile(instance.image500_webp.path):
            os.remove(instance.image500_webp.path)
    if instance.image800_webp:
        if os.path.isfile(instance.image800_webp.path):
            os.remove(instance.image800_webp.path)
    if instance.img150:
        if os.path.isfile(instance.img150.path):
            os.remove(instance.img150.path)
    if instance.img150x150:
        if os.path.isfile(instance.img150x150.path):
            os.remove(instance.img150x150.path)
    if instance.img245:
        if os.path.isfile(instance.img245.path):
            os.remove(instance.img245.path)
    if instance.img245x245:
        if os.path.isfile(instance.img245x245.path):
            os.remove(instance.img245x245.path)
    if instance.img500:
        if os.path.isfile(instance.img500.path):
            os.remove(instance.img500.path)
    if instance.img500x500:
        if os.path.isfile(instance.img500x500.path):
            os.remove(instance.img500x500.path)
    if instance.img800:
        if os.path.isfile(instance.img800.path):
            os.remove(instance.img800.path)
    if instance.img800x800:
        if os.path.isfile(instance.img800x800.path):
            os.remove(instance.img800x800.path)
