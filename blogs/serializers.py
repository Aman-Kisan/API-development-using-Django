from rest_framework import serializers
from .models import Blog, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


# nested serializers    
class BlogSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)      #the property name has to be same as the related name
    class Meta:
        model = Blog
        fields = "__all__"