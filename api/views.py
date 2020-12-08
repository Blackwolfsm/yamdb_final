from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.utilities import get_user_confirmation_code
from yamdb.models import User, Review, Title, Category, Genre
from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdmin)
from .serializers import (UserSerializer, ReviewSerializer,
                          CommentSerializer, CategorySerializer,
                          GenreSerializer, TitleReadSerializer,
                          TitleWriteSerializer)


@api_view(['POST'])
def get_confirmation_code(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    true_user_confirmation_code = get_user_confirmation_code(user)
    send_mail(
        'Confirmation code',
        f'Here is your confirmation code: {true_user_confirmation_code}',
        'admin@yamdb.ru',
        [user.email],
        fail_silently=False,
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    email = request.data.get('email')
    received_user_confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    true_user_confirmation_code = get_user_confirmation_code(user)
    if received_user_confirmation_code == true_user_confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token), })
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            data = request.data
            serializer = UserSerializer(request.user, data=data,
                                        partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsAdmin]


class CreateDestroyListModelMixin(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateDestroyListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=slug']
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=slug']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title_id=title.id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=review_id, title=title)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
