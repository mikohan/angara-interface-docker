from django.utils.text import slugify
from transliterate import translit
import re
import os
from PIL import Image, ImageOps
from .stemer import Porter


def chk_img(img):
    if img and hasattr(img, "url"):
        return img.url
    return "/some/random/string"


def categorizer_split(
    instance, Category
):  # Instance - Product instance, Category - Category model, String -
    instance.category.clear()
    categories_qs = Category.objects.all().filter(id__gt=2000)
    string = instance.full_name.lower()
    ready = list()

    for cat in categories_qs:
        minus = [x.strip() for x in cat.minus.split("\n")]
        plus = [x.strip() for x in cat.plus.split("\n")]
        plus_single_list = []

        for p in plus:
            find = None
            single_list = p.split()
            plus_single_list.append(single_list)

        for sing_lst in plus_single_list:
            if all(plus_word.lower() in string.lower() for plus_word in sing_lst):
                find = string.lower()
        if find:
            # print(minus)
            if any(minus_word in find for minus_word in minus):
                pass
            else:
                if (cat.id, cat.name) not in ready:
                    ready.append({"id": cat.id, "name": cat.name})
                # print(minus, plus)
    for r in ready:
        instance.category.remove(Category.objects.get(id=r["id"]))
        instance.category.add(Category.objects.get(id=r["id"]))
    return ready


# Categorizer work
# def categorizer(instance, Category, string): # Instance - Product instance, Category - Category model, String -
#     categories_qs = Category.objects.all().filter(id__gt=2000)
#     string = string.lower()
#     ready = list()

#     for cat in categories_qs:
#         minus = [x.minus.strip() for x in cat.to_category_minus.all()]
#         plus = [x.plus.strip() for x in cat.to_category.all()]
#         plus_single_list = []

#         for p in plus:
#             find = None
#             single_list = p.split()
#             plus_single_list.append(single_list)

#         for sing_lst in plus_single_list:
#             if all(plus_word in string for plus_word in sing_lst):
#                 find = string
#         if find:
#             # print(minus)
#             if any(minus_word in find for minus_word in minus):
#                 pass
#             else:
#                 if (cat.id, cat.name) not in ready:
#                     ready.append({'id': cat.id, 'name': cat.name})
#                 #print(minus, plus)

#     for r in ready:
#         instance.category.remove(Category.objects.get(id=r['id']))
#         instance.category.add(Category.objects.get(id=r['id']))
#     return ready

# Slugifyer for products


def unique_slug_generator(instance, name, slug_field):

    slug = slugify(translit(name, "ru", reversed=True))

    model_class = instance.__class__

    while model_class._default_manager.filter(slug=slug).exists():

        object_pk = model_class._default_manager.latest("pk")
        object_pk = str(object_pk.id + 1)

        slug = f"{slug}-{object_pk}"
    return slug


def get_youtube_id(url):  # Getting youtube video ID form url
    myregexp = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    regexp = re.compile(myregexp)
    m = regexp.search(url)
    return m.group(1)


##########################################################
# This function uses nowhere but exist as an example for resizing by PIL


def image_resizer(img, size):  # Image resizer for saving to bd different sizes
    file = "tai.jpg"
    im = Image.open(file)
    file, ext = os.path.splitext(file)
    im = ImageOps.fit(im, size, method=Image.NEAREST, bleed=0.0, centering=(0.5, 0.5))

    im.save("thumbnail" + file + ext)


# File deletedef
def delete_file(path):  # Deleting Files from disk
    if os.path.isfile(path):
        os.remove(path)


def stemmer(string):
    """
    Returns array of stems for search
    """
    words = string.split(" ")
    s = Porter()
    stems = []
    for word in words:
        stems.append(s.stem(word))
    return stems
