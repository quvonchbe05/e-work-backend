from django.conf import settings
import jwt



def decode_jwt(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        bearer_token = token.split(' ')[1]
        payload = jwt.decode(bearer_token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None
