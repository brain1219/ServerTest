from django.db import models
from django.urls import reverse
import os

# Create your models here.
# 글의 분류
class Category(models.Model):
    name = models.CharField(max_length=50, help_text="글의 분류를 입력하세요.(ex: 일상)")

    def __str__(self):
        return self.name

# 글 (제목, 작성일, 이미지, 내용, 분류))
class Post(models.Model):
    title = models.CharField(max_length=200) # CharField = 짧은 텍스트
    title_image = models.ImageField(blank=True) # 공백 허용
    content = models.TextField() # TextField = 긴 텍스트
    createDate = models.DateTimeField(auto_now_add=True) # 기본값 = 현재 날짜/시간
    updateDate = models.DateTimeField(auto_now_add=True) # 기본값 = 현재 날짜/시간
    # 분류의 경우 하나의 분류에 여러가지 글이 포함될 수 있고 하나의 글이 여러가지 분류에 포함될 수 있음 (다대다 관계)
    category = models.ManyToManyField(Category, help_text="글의 분류를 설정하세요.")

    def __str__(self):
        return self.title

    # 1번 글의 경우 주소 : ../post/1
    def get_absolute_url(self):
        return reverse("post", args=[str(self.id)])

    def is_content_more90(self):
        return len(self.content) > 90

    def get_content_under90(self):
        return self.content[:90]

#catordog

class Checkimage(models.Model):
    check_image = models.ImageField(upload_to="target")
    createDate = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("catOrdog_result")