from rest_framework import serializers
from .models import Server, Category, Channel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    num_member = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Server
        exclude = ("member",)

    def get_num_member(self, obj):
        if hasattr(obj, "num_member"):
            return obj.num_member
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_member = self.context.get("num_member")
        if not num_member :
            pass
        
            # data.pop("num_member":None)
        return data