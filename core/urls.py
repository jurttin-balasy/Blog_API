

# Generic View and APIView

# from django.urls import path
# from .views import PostList, PostDetailView, CategoryDetailView, CategoryList

# urlpatterns = [
#     path('posts/', PostList.as_view(), name='post-list'),
#     path('posts/<int:pk>/', PostDetailView.as_view(), name='post'),
#     path('categories/', CategoryList.as_view(), name='categories'),
#     path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category'),

# ]






# ViewSET

from rest_framework.routers import DefaultRouter

from .views import  PostViewSet, CategoryViewSet, UserViewSet, CommentViewSet, TagViewset

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tags', TagViewset, basename='tags')

router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = router.urls