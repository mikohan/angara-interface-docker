from django.conf import settings


def main_host(request):
    """
    Here I defined main site url to use it in vue.js file
    """
    # return {'MAIN_HOST': f"{scheme}://{host}"}
    return {'MAIN_HOST': f"{settings.MAIN_HOST_SSL}://{settings.MAIN_HOST}"}
