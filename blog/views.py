from django.shortcuts import render
from blog.models import Category, Post, Checkimage
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from blog.catORdog import is_cat_or_dog
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
    context = {
        "img_latest": img_latest,
    }
    return render(req, "catordog_result.html", context=context)