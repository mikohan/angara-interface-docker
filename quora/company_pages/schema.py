from company_pages.models import CompanyPages
from django.db.models import Count, Q
from blog.models import Post, Categories
from product.schemaTypes import NewCarModelType
from functools import reduce
from product.utils import stemmer
from operator import or_


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


class PageType(ObjectType):
    id = ID()
    slug = String()
    title = String()
    textHTML = String()
    text = String()
    author = String()


class CategoryType(ObjectType):
    id = ID()
    slug = String()
    name = String()
    posts_count = Int()


class PostType(ObjectType):
    id = ID()
    slug = String()
    image = String()
    title = String()
    excerpt = String()
    text = String()
    partsCategory = List(CategoryType)
    category = List(CategoryType)
    date = Date()
    author = String()
    car = List(NewCarModelType)
    totalCount = Int()
    count = Int()
    tags = List(String)


def makePost(post):

    models = [
        {
            "id": x.id,
            "slug": x.slug,
            "name": x.name,
            "model": x.name,
            "priority": x.priority,
            "image": x.image.url if x.image else None,
            "rusname": x.rusname,
            "make": {
                "slug": x.carmake.slug,
                "name": x.carmake.name,
                "id": x.carmake.id,
                "country": x.carmake.country,
            },
        }
        for x in post.car.all()
    ]
    partsCategory = [
        {
            "id": x.id,
            "slug": x.slug,
            "name": x.name,
        }
        for x in post.parts_category.all()
    ]
    if len(partsCategory) == 0:
        partsCategory = []
    tags = []
    try:
        for x in post.categories.all():
            tags.append(x)
    except Exception as e:
        print("No tags or something", e)

    ret = {
        "slug": post.slug,
        "id": post.id,
        "image": post.image.url if post.image else None,
        "title": post.title,
        "excerpt": post.excerpt,
        "text": post.text,
        "date": post.date,
        "author": post.author,
        "partsCategory": partsCategory,
        "category": [
            {"id": x.id, "slug": x.slug, "name": x.name} for x in post.categories.all()
        ],
        "car": models,
        "tags": tags,
    }
    return ret


class Query(ObjectType):
    page = Field(PageType, slug=String())
    pages = List(PageType)
    post = Field(PostType, slug=String())
    posts = List(PostType, limit=Int())
    categories = List(CategoryType)
    totalPosts = Int()
    postsByCategory = List(
        PostType,
        slug=String(required=True),
        pageFrom=Int(required=True),
        pageTo=Int(required=True),
    )
    postsSearch = List(
        PostType,
        search=String(required=True),
        pageFrom=Int(required=True),
        pageTo=Int(required=True),
    )
    postsByCar = List(PostType, model=String(required=True), limit=Int(required=True))

    def resolve_postsSearch(self, info, search, pageFrom, pageTo):
        searchWords = stemmer(search)
        query = reduce(lambda q, value: q | Q(text__icontains=value), searchWords, Q())
        queryTitle = reduce(or_, (Q(title__icontains=value) for value in searchWords))
        totalQuery = Q(query | queryTitle)
        qs = Post.objects.filter(totalQuery)[pageFrom:pageTo]

        genQs = Post.objects.all()
        totalCount = genQs.count()

        count = Post.objects.filter(totalQuery).count()
        if count == 0:
            qs = genQs[pageFrom:pageTo]
            count = 100
        ret = []
        for post in qs:
            newPost = makePost(post)
            newPost["totalCount"] = totalCount
            newPost["count"] = count
            ret.append(newPost)
        return ret

    def resolve_postsByCar(self, info, model, limit):
        try:
            qs = Post.objects.filter(car__slug=model).order_by("-date")[:limit]
            ret = []
            for post in qs:
                ret.append(makePost(post))
            return ret
        except Exception as e:
            print("Probably no posts in post by model slug", e)
            return []

    def resolve_totalPosts(self, info):
        qs = Post.objects.all()
        return qs.count()

    def resolve_categories(self, info):
        qs = (
            Categories.objects.all()
            .annotate(posts_count=Count("blog_categories"))
            .order_by("-priority")
        )
        return qs

    def resolve_page(self, info, slug):
        qs = CompanyPages.objects.get(slug=slug)
        return qs

    def resolve_pages(self, info):
        qs = CompanyPages.objects.all()
        return qs

    def resolve_postsByCategory(self, info, slug, pageFrom, pageTo):
        posts = None
        f = pageFrom
        t = pageTo
        if slug == "vse-kategorii":
            posts = Post.objects.all()[f:t]
        else:
            posts = Post.objects.filter(categories__slug=slug)[f:t]
        ret = []
        for post in posts:
            ret.append(makePost(post))
        return ret

    def resolve_post(self, info, slug):
        post = Post.objects.get(slug=slug)
        totalCount = Post.objects.all().count()
        ret = makePost(post)
        ret["totalCount"] = totalCount
        return ret

    def resolve_posts(self, info, limit):
        qs = Post.objects.all()
        if limit != 0:
            qs = Post.objects.all().order_by("-date")[:limit]
        posts = []
        for post in qs:
            ret = makePost(post)
            posts.append(ret)
        return posts


schema = Schema(query=Query)
