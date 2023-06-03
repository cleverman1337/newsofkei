from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Articles(models.Model):
    title = models.CharField('имя статьи', max_length=140)
    anons = models.CharField('анонс', max_length=250)
    text_in_box = models.TextField('Текст статьи')
    date = models.DateTimeField('дата публикации')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    imgurl = models.CharField('ссылка на изображение', max_length=255, blank=True, null=True)
    likes = models.PositiveIntegerField('лайки', default=0)
    dislikes = models.PositiveIntegerField('дизлайки', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def increase_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])

    def increase_dislikes(self):
        self.dislikes += 1
        self.save(update_fields=['dislikes'])

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
