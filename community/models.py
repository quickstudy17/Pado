from django.db import models
from django.conf import settings

# Create your models here.
class Article(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')

def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)  

class Image(models.Model):
    # media/images에 이미지 저장
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class PrivateArticle(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class PrivateArticleImage(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    private_article = models.ForeignKey(PrivateArticle, on_delete=models.CASCADE)




class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')



