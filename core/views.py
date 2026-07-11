from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import PostSerializer, CategorySerializer, UserSerializer, CommentSerializer, TagSerializer, InfoSerializer
# Create your views here.
from rest_framework import status
from django.contrib.auth.models import User

# GenericView
from rest_framework import generics


# ViewSet
from rest_framework import viewsets, filters # filterdi qosiw


from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend


from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator

from . import utils
# Generic Views

# class PostList(generics.ListCreateAPIView):
#     queryset = models.Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Post.objects.all()
#     serializer_class = PostSerializer


# class CategoryList(generics.ListCreateAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = CategorySerializer


# class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = CategorySerializer




# ViewSet
class PostViewSet(viewsets.ModelViewSet):
    # queryset = models.Post.objects.select_related('author').all()
    queryset = models.Post.objects.select_related('author','category').prefetch_related('tags').all()
    # for post in queryset:
    #     print(f"ID: {post.id}\nTitle: {post.title}\nAvtor: {post.author.username}\nContent: {post.content}")
    #     print("Tags:")
    #     n = 1
    #     for tag in post.tags.all():
    #         print(f"{n}. {tag}")
    #         n += 1
        

    
    serializer_class = PostSerializer

    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]  # ozgerttik

    filter_backends = [filters.SearchFilter, DjangoFilterBackend] # izlew backend in qosiw
    search_fields = ['title', 'content', 'author__username']

    filterset_fields = ['author', 'created_at']

    # @cache_page(60 * 15)
    # @api_view(['GET'])
    # def list_posts(request):
    #     # Bul kod birinshi ret iske túsedi.
    #     # Keyingi 15 minut ishinde kelgen barlıq sorawlarǵa
    #     # bazaǵa barıw ornına kesh-ten juwap qaytarıladı.
    #     posts = models.Post.objects.select_related('author', 'category').prefetch_related('tags').all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # jana posttin avtorin avtomatli turde belgilew

  


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]


    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class TagViewset(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.select_related('posts', 'author').all()
    serializer_class = CommentSerializer
    pagination_class = None

from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response


class InfoViewSet(viewsets.ModelViewSet):
    queryset = models.Info.objects.all()
    serializer_class = InfoSerializer

    

class StatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        stats = utils.get_statistics()
        return Response(stats)
    


# 60 * 15 = 900 sekund (15 minut) keshlew


# APIVIew 

# class PostList(APIView):

#     def get(self, request, format=None):
#         posts = models.Post.objects.all()
        

#         # data = [
#         #     {
#         #         'id': post.id,
#         #         'title': post.title,
#         #         'author': post.author.username
#         #     }
#         #     for post in posts
#         # ]

#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    

#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetailView(APIView):
#     def get(self, request, pk, format=None):
#         post = models.Post.objects.get(pk=pk)

#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    

#     def put(self, request, pk, format=None):
#         post = models.Post.objects.filter(pk=pk).first()

#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#     def patch(self, request, pk, format=None):
#         post = models.Post.objects.filter(pk=pk).first()

#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#     def delete(self, request, pk, format=None):
#         post = models.Post.objects.filter(pk=pk).first()

#         if not post:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# class CategoryView(APIView):
#     def get(self, request, format=None):
#         category = models.Category.objects.all()

#         serializer = CategorySerializer(category, many=True)

#         return Response(serializer.data)
    


    
#     def post(self, request, format = None):
#         serializer = CategorySerializer(data = request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class CategoryDetailView(APIView):
#     def get(self, request, pk, format=None):
#         category = models.Category.objects.filter(pk=pk).first()

#         if not category:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = CategorySerializer(category)

#         return Response(serializer.data)
    


#     def put(self, request, pk, format=None):
#         category = models.Category.objects.filter(pk=pk).first()
#         if not category:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = CategorySerializer(category, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#     def patch(self, request, pk, format=None):
#         category = models.Category.objects.filter(pk=pk).first()
#         if not category:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = CategorySerializer(category, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
    



#     def delete(self, request, pk , format=None):
#         category = models.Category.objects.filter(pk=pk).first()

#         if not category:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)