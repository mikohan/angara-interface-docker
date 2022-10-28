from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type, renderer_context):
        charset = "utf-8"

        response = None

        if "ErrorDetail" in str(data):
            response = json.dumps({"errors": data}).encode(charset)
        else:
            response = json.dumps({"data": data}).encode(charset)

        return response
