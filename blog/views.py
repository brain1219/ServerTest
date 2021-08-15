from django.shortcuts import render
from blog.models import Category, Post, Checkimage, CatAndDogUploadApi
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from blog.catORdog import is_cat_or_dog

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer, CatAndDogSerializer, CatAndDogUploadApiSerializer
from .models import Post



import os 

# Create your views here.
def index(req):
    post_latest = Post.objects.order_by("-createDate") # - : 내림차순, [:5] : 5개를 가져옴 
    allCategories = Category.objects.order_by("name")
    context = {
        "post_latest": post_latest,
        "allCategories": allCategories,
    }

    return render(req, "index.html", context=context)

class PostDetailView(generic.DetailView):
    model = Post

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "title_image", "content", "category"]
    
class catOrdog(CreateView):
    filePath = 'media/target'
    if os.path.exists(filePath):
        for file in os.scandir(filePath):
            os.remove(file.path)
            
    model = Checkimage
    fields = ["check_image"]

def catOrdog_result(req):
    
    img_latest = Checkimage.objects.order_by("-createDate")[:1]
    for img in img_latest:
        img.pred_val = is_cat_or_dog()
    checkimage = Checkimage.objects.get(check_image=img_latest[0].check_image, createDate=img_latest[0].createDate)
    checkimage.pred_val = img_latest[0].pred_val
    checkimage.save()
    context = {
        "img_latest": img_latest,
    }
    return render(req, "catordog_result.html", context=context)

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CatAndDogViewset(viewsets.ModelViewSet):
    queryset = Checkimage.objects.all()
    serializer_class = CatAndDogSerializer

class CatAndDogUploadApiViewset(viewsets.ModelViewSet):
    queryset = Checkimage.objects.all()
    serializer_class = CatAndDogUploadApiSerializer


# 이거 다섯 줄 짜는데 2시간 넘게 걸림ㄷㄷ
@api_view(['POST'])
def cat_and_dog_pred_api(request):
    serializer = CatAndDogUploadApiSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(is_cat_or_dog())    
