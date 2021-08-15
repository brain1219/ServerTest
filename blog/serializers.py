from rest_framework import serializers
from .models import Post, Checkimage, CatAndDogUploadApi
from django.core.files.base import ContentFile
import base64
import six

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            
            target_file_name = 'target.jpg'
            data = ContentFile(decoded_file, name=target_file_name)
        return super(Base64ImageField, self).to_internal_value(data)



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'title_image')

class CatAndDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkimage
        fields = ('check_image', 'pred_val')

class CatAndDogUploadApiSerializer(serializers.ModelSerializer):
    check_image = Base64ImageField(
        max_length=None, use_url=True
    )

    class Meta:
        model = CatAndDogUploadApi
        fields = ('check_image', 'createDate')