from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Authenticate using e-mail account.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):

        if email is None:
            email = kwargs.get('email')
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password)\
                    and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):

        if phone is None:
            phone = kwargs.get('phone')
        if phone is None or password is None:
            return
        try:
            user = UserModel.objects.get(phone=phone)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) \
                    and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
