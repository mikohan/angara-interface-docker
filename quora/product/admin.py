from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin
from django.contrib import admin  # type: ignore
from product.models import (
    Price,
    PriceHistory,
    Stock,
    Product,
    Units,
    Category,
    Store,
    ProductVideos,
    ProductImage,
    ProductAttribute,
    ProductDescription,
    ProductAttributeName,
    Cross,
    ProductBages,
    ProductRating,
    CategoryYandexMarket,
    CategoryOzon,
    OldProductImage,
)
from product.models.models_vehicle import Years, CarEngine, CarMake, CarModel, Country

admin.site.register(Product)
admin.site.register(Units)
admin.site.register(Country)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(CarEngine)
admin.site.register(ProductAttribute)
admin.site.register(ProductDescription)
admin.site.register(ProductImage)
admin.site.register(ProductVideos)
admin.site.register(ProductAttributeName)
admin.site.register(Cross)
admin.site.register(Store)
admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(PriceHistory)
admin.site.register(Years)
admin.site.register(ProductBages)
admin.site.register(ProductRating)
admin.site.register(CategoryYandexMarket)
admin.site.register(CategoryOzon)
admin.site.register(OldProductImage)


# admin.site.register(Category, MPTTModelAdmin)


class CategoryAdmin(DjangoMpttAdmin):
    tree_auto_open = 0
    tree_load_on_demand = 0
    use_context_menu = True


admin.site.register(Category, CategoryAdmin)
