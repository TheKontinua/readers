from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            print("This was the 'username' (email): ", username)
            user = UserModel.objects.get(email=username)
            print("This is the user returned in auth!", user)
            print("This is the password passed in: ", password)
            if user.check_password(password):
                print("this is the user being returned: ", user)
                return user
        except UserModel.DoesNotExist:
            return None
