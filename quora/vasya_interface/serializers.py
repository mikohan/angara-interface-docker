from rest_framework import serializers
from .models import Rows


class RowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = "__all__"


class CheckProductSerializer(serializers.Serializer):
    one_c_id = serializers.IntegerField(read_only=True)
    has_description = serializers.BooleanField(required=False)
    have_photo = serializers.BooleanField(required=False)
    have_attribute = serializers.BooleanField(required=False)
    have_description = serializers.BooleanField(required=False)
    have_video = serializers.BooleanField(required=False)
    have_photo_in_folder = serializers.BooleanField(required=False)


class CheckFolderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    one_c_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    cat_number = serializers.CharField(read_only=True)
    have_photo = serializers.BooleanField(required=False)


class FolderListSerializer(serializers.Serializer):

    fld = serializers.SerializerMethodField("get_fld")

    def get_fld(self, obj):
        return [x for x in obj]

    # part_list = serializers.ListField(child=serializers.CharField(max_length=50))
