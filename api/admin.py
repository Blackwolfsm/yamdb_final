from django.contrib import admin

from yamdb.models import Review, Comment, Title, Genre, Category


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    list_filter = ('pub_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'pub_date', 'author')
    list_filter = ('pub_date',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year',
                    'category', 'description')


admin.site.register(Genre)
admin.site.register(Category)
