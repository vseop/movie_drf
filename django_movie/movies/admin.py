from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, RatingStar, Review, Rating
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание",widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'

# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категория"""
    list_display = ("id", "name", "url")  # отображаемые поля
    list_display_links = ("name",)  # поле ссылка


# class ReviewInline(admin.StackedInline): # при открытии фильма все отывы к нему
class ReviewInline(admin.TabularInline):  # выстраиваются по горизонтали
    """Отзывы на странице фильма"""
    model = Review
    extra = 1  # количество доп полей
    readonly_fields = ("name", "email")

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):  # вывод изображения
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100" height="80"')

    get_image.short_description = "Изображение"

class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True  # меню сохранить вверху
    save_as = True  # кнопка сохранить как новый объект
    list_editable = ("draft",)  # поле для редактирования из панели
    actions = ["publish", "unpublish"] # действия в админ панели
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    # fields = (
    # ("actors", "directors", "genres"),)  # групировка в одну строку (поля которые отобоажаются)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)  # группировка в одну строку
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))  # группировка в одну строку
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)  # группировка в одну строку
        }),
        ("Actors", {
            "classes": ("collapse",),  # свернутая группа
            "fields": (("actors", "directors", "genres", "category"),)  # группировка в одну строку
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_word"),)  # группировка в одну строку
        }),
        ("Options", {
            "fields": (("url", "draft"),)  # группировка в одну строку + ИМЯ группы
        }),

    )

    def get_image(self, obj):  # вывод изображения
        if obj.poster:
            return mark_safe(f'<img src={obj.poster.url} width="100" height="80"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',) # права доступа

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"

class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")  # сокрыть от редактирования


class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):  # вывод изображения
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="60" height="40"')

    get_image.short_description = "Изображение"


class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")

    readonly_fields = ("get_image",)

    def get_image(self, obj):  # вывод изображения
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="60" height="40"')

    get_image.short_description = "Изображение"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieShots, MovieShotsAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(RatingStar)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Rating, RatingAdmin)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"