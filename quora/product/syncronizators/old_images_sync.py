from product.models import OldProductImage, Product
import progressbar, pathlib, re
from django.core.files.images import ImageFile


def imgProcess(image_path, product):

    s = image_path.stem.split("-")
    one_c_id = product.one_c_id
    name = image_path.name

    old_image = OldProductImage(
        one_c_id=one_c_id,
        product=product,
        image=ImageFile(open(image_path, "rb"), name),
    )

    old_image.save()


def doOldImages():
    src = "/home/manhee/tmp/"
    p = pathlib.Path(src)

    l = sum(1 for dummy in p.iterdir())
    prod_err = []
    reg_err = []
    with progressbar.ProgressBar(max_value=l) as bar:
        for i, x in enumerate(p.iterdir()):
            try:
                match = re.search(r"(\d{2,5})\.[a-z]+$", x.name)
                one_c_id = match.group(1)  # type: ignore
                product = Product.objects.get(one_c_id=one_c_id)
                imgProcess(x, product)
            except Exception as e:
                prod_err.append("fuck")
                reg_err.append("fuck")
            #         if i == 10:
            #             break
            bar.update(i)
        print(len(prod_err), len(reg_err))
