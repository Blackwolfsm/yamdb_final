from django.contrib.auth.tokens import PasswordResetTokenGenerator


def get_user_confirmation_code(user):
    token_generator = PasswordResetTokenGenerator()
    return token_generator.make_token(user)
