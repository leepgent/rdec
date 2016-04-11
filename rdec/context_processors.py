from django.conf import settings


def league_name(request):
    return {'LEAGUE_NAME': settings.LEAGUE_NAME}
