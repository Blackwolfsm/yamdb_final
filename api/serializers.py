from rest_framework import serializers

from yamdb.models import User, Review, Comment, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'bio', 'email', 'role']
        extra_kwargs = {'email': {'required': True}}


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)

    def validate_slug(self, slug):
        check_db = Category.objects.filter(slug=slug.lower())
        if check_db:
            raise serializers.ValidationError(
                'such field already exists')
        return slug

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)

    def validate_slug(self, slug):
        check_db = Genre.objects.filter(slug=slug.lower())
        if check_db:
            raise serializers.ValidationError(
                'such field already exists')
        return slug

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', required=False,
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all(),
                                         required=False)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    def validate(self, data):
        super().validate('attrs')
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        title = (self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
