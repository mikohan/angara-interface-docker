from product.models.models import ProductRating
import math
from functools import reduce
from django.db.models import Avg, Q
from users.models import AutoUser
from product.models import CarModel, CarMake, Category, Product
from graphene import (
    String,
    ObjectType,
    Date,
    ID,
    Field,
    Schema,
    List,
    Boolean,
    Int,
    DateTime,
)
from django.db.models import Count
from .utils import chk_img
from .schemaTypes import *
from .schemaMutations import Mutation
from .utils import stemmer
from .schema_helpers import makeProduct


# connections.create_connection(hosts=["{settings.ELASTIC_URL}"], timeout=20)
# esh = Elasticsearch(["http://{settings.ELASTIC_URL}"])
class ratingAvgType(ObjectType):
    ratingAvg = Int()


def ratingAvg(productId):
    try:
        product = Product.objects.get(id=productId)
        qs = ProductRating.objects.filter(product=product)
        avg = qs.aggregate(avg_score=Avg("score"))
        count = qs.count()

        return math.ceil(avg["avg_score"]), count
    except Exception as e:
        return None, None


class Query(ObjectType):

    vehicle = Field(NewCarModelType, slug=String())
    vehicles = List(NewCarModelType)
    makes = List(CarMakeType)
    make = Field(CarMakeType, slug=String(required=False))
    vehicles_by_make = List(NewCarModelType, slug=String(required=True))
    vehicles_by_priority = List(NewCarModelType, priority=Int(required=True))
    category_by_slug = Field(CategoryType, slug=String(required=True))
    category_all = List(CategoryType)
    category_top = List(CategoryType)
    popular_products = List(
        PopularProductByModelType,
        slugs=List(String),
        quantity=Int(required=True),
    )
    similarProducts = List(ProductType, slug=String(required=True), quantity=Int())
    togetherProduct = List(ProductType, slug=String(required=True))
    product = Field(ProductType, slug=String(required=True))
    productOneC = Field(ProductType, onec=Int(required=True))
    autouser = Field(AutoUserType, userId=String(required=True))
    rating = Field(RatingType, productId=Int(), userId=String())
    productRating = Field(GetRatingType, productId=Int())
    analogs = List(ProductType, catNumber=String(), productId=Int())
    latestProducts = List(ProductType, limit=Int())

    def resolve_latestProducts(self, info, limit):
        qs = Product.objects.all().order_by("-created_date")[:limit]
        ret = []
        for prod in qs:
            ret.append(makeProduct(prod))
        return ret

    def resolve_togetherProduct(self, info, slug):
        try:
            product = Product.objects.get(slug=slug)
            returnProduct = []
            for related in product.related.all():
                returnProduct.append(makeProduct(related))
            return returnProduct
        except Exception as e:
            print("Error in get together products", e)
            return []

    def resolve_similarProducts(self, info, slug, quantity):
        try:
            product = Product.objects.get(slug=slug)
            searchWords = stemmer(product.name)
            query = reduce(
                lambda q, value: q & Q(name__icontains=value), searchWords[:1], Q()
            )
            models = [x.slug for x in product.car_model.all()]

            similar = (
                Product.objects.filter(car_model__slug__in=models)
                .filter(query)
                .exclude(id=product.id)[:quantity]
            )
            returnProductList = []
            for prod in similar:
                returnProductList.append(makeProduct(prod))
            return returnProductList
        except Exception as e:
            print(e)
            return []

    def resolve_analogs(self, info, catNumber, productId):
        try:

            qs = (
                Product.objects.filter(cat_number=catNumber)
                .exclude(id=productId)
                .distinct()
            )
            returnProductList = []
            for prod in qs:
                returnProductList.append(makeProduct(prod))
            return returnProductList
        except Exception as e:
            print("Error in resolve analogs", e)
            return []

    def resolve_productRating(self, info, productId):
        try:
            product = Product.objects.get(id=productId)
            rating = ProductRating.objects.filter(product=product)
            count = rating.count()
            avg = rating.aggregate(avg_score=Avg("score"))
            return {"rating": avg["avg_score"], "ratingCount": count}

        except:
            return {"rating": None, "ratingCoung": None}

    def resolve_rating(self, info, productId, userId):
        try:
            product = Product.objects.get(id=productId)
            qs = ProductRating.objects.get(product=product, autoUser__userId=userId)
            return {"score": qs.score, "autouser": qs.autoUser}
        except:
            return None

    def resolve_autouser(self, info, userId):
        qs = AutoUser.objects.get(userId=userId)
        return {
            "userId": qs.userId,
            "createdDate": qs.created_date,
            "updatedDate": qs.updated_date,
        }

    def resolve_popular_products(self, info, slugs, quantity=20):
        try:
            qs = (
                Product.objects.filter(car_model__slug__in=slugs)
                .filter(product_image__isnull=False)
                .distinct()[:quantity]
            )  # Needs to add some filter by popularity
            lst = []
            for prod in qs:
                lst.append(makeProduct(prod))
            return lst
        except Exception as e:
            print("Error in resolve_popular_products", e)
            return []

    def resolve_category_all(self, info):
        cats = Category.objects.all()
        lst = []

        for cat in cats:
            parent = None
            try:
                parent = cat.parent.id
            except:
                parent = None
            lst.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "parent": parent,
                    "image": cat.image,
                    "type": cat.type,
                    "layout": cat.layout,
                }
            )
        return lst

    # Resolving categories top level
    def resolve_category_top(self, info):
        cats = Category.objects.filter(parent__isnull=True)
        lst = []

        for cat in cats:
            parent = None
            try:
                parent = cat.parent.id
            except:
                parent = None
            lst.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "parent": parent,
                    "image": cat.image,
                    "type": cat.type,
                    "layout": cat.layout,
                    "weight": cat.weight,
                }
            )
        return lst

    def resolve_category_by_slug(self, info, slug):
        cat = Category.objects.filter(slug=slug).first()
        try:
            parent = cat.parent.id
        except:
            parent = None
        return {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "parent": parent,
            "image": cat.image,
            "type": cat.type,
            "layout": cat.layout,
        }

    def resolve_vehicles_by_make(self, info, slug):
        qs = (
            CarModel.objects.filter(active=True)
            .filter(carmake__slug=slug)
            .annotate(count=Count("model_product"))
            .order_by("-priority", "-weight")
        )
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "rusname": car.rusname,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "priority": car.priority,
                    "image": car.image.url if car.image else None,
                    "weight": car.weight,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
                    "country": car.carmake.country,
                    "count": car.count,
                }
            )
        return lst

    def resolve_vehicles_by_priority(self, info, priority):
        qs = (
            CarModel.objects.filter(active=True)
            .filter(priority__gte=priority)
            .order_by("-carmake__priority", "-priority", "-weight")
        )
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "rusname": car.rusname,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "priority": car.priority,
                    "image": car.image.url if car.image else None,
                    "weight": car.weight,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
                    "country": car.carmake.country,
                }
            )
        return lst

    def resolve_makes(self, info):
        qs = CarMake.objects.all()
        lst = []
        for make in qs:
            lst.append(
                {
                    "id": make.id,
                    "name": make.name,
                    "rusname": make.rusname,
                    "slug": make.slug,
                    "country": make.country.country,
                    "priority": make.priority,
                    "image": make.image.url if make.image else None,
                }
            )
        return lst

    def resolve_make(self, info, slug):
        make = CarMake.objects.filter(slug=slug).first()
        return {
            "id": make.id,
            "name": make.name,
            "rusname": make.rusname,
            "slug": make.slug,
            "country": make.country.country,
            "priority": make.priority,
            "image": make.image.url if make.image else None,
        }

    def resolve_vehicle(self, info, slug):
        try:
            car = CarModel.objects.filter(slug=slug).first()
            years = [car.year_from, car.year_to] if (car) else []

            return {
                "id": car.id,
                "model": car.name,
                "rusname": car.rusname,
                "year": years,
                "engine": car.engine.all(),
                "slug": car.slug,
                "priority": car.priority,
                "history": car.model_history,
                "liquids": car.model_liquids,
                "to": car.model_to,
                "image": car.image.url if car.image else None,
                "weight": car.weight,
                "make": {
                    "id": car.carmake.id,
                    "name": car.carmake.name,
                    "slug": car.carmake.slug,
                    "country": car.carmake.country,
                    "priority": car.carmake.priority,
                },
                "make_slug": car.carmake.slug,
                "country": car.carmake.country,
            }
        except Exception as e:
            print(e, "in exception")
            return None

    def resolve_vehicles(self, info):
        qs = CarModel.objects.all()
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "rusname": car.rusname,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "priority": car.priority,
                    "image": car.image.url if car.image else None,
                    "weight": car.weight,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
                    "country": car.carmake.country,
                }
            )

        return lst

    def resolve_product(self, info, slug):

        try:
            prod = Product.objects.get(slug=slug)
            return makeProduct(prod)
        except Exception as e:
            print("Product not found in GraphQl product/schema line 326", e)

    def resolve_productOneC(self, info, onec):

        try:
            prod = Product.objects.get(one_c_id=onec)
            return makeProduct(prod)
        except Exception as e:
            print("Product not found in GraphQl product/schema line 326", e)


schema = Schema(query=Query, mutation=Mutation)
