from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .models import Categories, Post
from .serializers import BlogPostSerializer, BlogCategorySerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get blog post
    """

    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        limit = self.request.GET.get("limit")
        if limit:
            return self.queryset.all().order_by("-date")[: int(limit)]

        return self.queryset


class BlogCategoryView(ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]


class BlogCategorySearchView(ListAPIView):

    """
    If isset category returns blog filtred by category
    else filtered by search string
    else just all queryset
    """

    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        search = self.request.GET.get("search")
        category = self.request.GET.get("category")

        if category:

            q = self.queryset.filter(categories=int(category))
            return q

        if search:
            q = self.queryset.filter(
                Q(title__icontains=search) | Q(text__icontains=search)
            )
            return q

        return self.queryset
