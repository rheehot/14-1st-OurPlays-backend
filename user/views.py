import re
import jwt
import json
import bcrypt

from django.db        import models
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from my_settings      import SECRET_KEY

from .models          import User

class SignUp(View):
    def post(self, request):
        data           = json.loads(request.body)
        check_email    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        check_password = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        #최소 8자, 최소 하나의 문자, 하나의 숫자 및 하나의 특수 문자
        
        if not 'email' in data:
            return JsonResponse({'message':'EMAIL_ERROR'}, status=400)
            
        if not re.match(check_email, data['email']):
            return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
            
        if not re.match(check_password, data['password']):
            return JsonResponse({'message':'PASSWORD1_ERROR'}, status=400)
        
        if not re.match(check_password, data['password2']):
                return JsonResponse({'message':'PASSWORD1_ERROR'}, status=400)

        if data['password'] != data['password2']:
                return JsonResponse({'message':'PASSWORD_INCONSISTENCY'}, status=400)
                            
        if User.objects.filter(email = data['email']).exists():
             return JsonResponse({'message':'EXISTS_USER'}, status=400)
        
        user = User.objects.create(
            name     = data['name'],
            email    = data['email'],
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(),
        )
        return JsonResponse({'message':'SUCCESS_SIGNUP'}, status=200)
        
       
class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'user_User' not in data or 'password' not in data:
                return JsonResponse({'message':'KEY_ERROR_CHECK_DATA'}, status=400)

            user_data = User.objects.filter(Q(email=data['user_User']) | Q(name=data['user_User']))

            if not user_data:
                return JsonResponse({'message':'INVALITD_USER'}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user_data.values()[0]['password'].encode('utf-8')):
                signin_token = jwt.encode({'email':user_data.values()[0]['email']}, 'SECRET_KEY', algorithm='HS256')
                signon_token = signin_token.decode('utf-8')
                return JsonResponse({'message':'SUCCESS_LOGIN', 'token':signon_token}, status=200)

            return JsonResponse({'message':'INVALID_password'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)