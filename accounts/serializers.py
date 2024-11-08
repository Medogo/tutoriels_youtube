from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #accepts_terms = serializers.BooleanField(required=True)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'password', 'email', 'is_active', 'is_staff' )

    def validate_accpets_terms(self, data):
        if not data.get('accepts_terms'):
            raise serializers.ValidationError("vous devez accepter les conditions generales pour vous inscrire")
        return data

    def create(self, validate_data):
        password = validate_data.pop('password')
        user = CustomUser(**validate_data)
        user.set_password(password)
        user.is_active = False    # on le desactive jusqu'a ce que il confirme son compte par mail
        user.save()
        return user