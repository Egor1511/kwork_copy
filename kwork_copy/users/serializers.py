from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import FreelancerProfile, CustomerProfile

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        write_only=True,
        max_length=2
    )
    password = serializers.CharField(
        write_only=True,
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        profile_role = validated_data.pop('role')
        user = User.objects.create_user(email=validated_data['email'],
                                        username=validated_data['username'],
                                        )
        user.set_password(validated_data['password'])
        user.save()
        if profile_role == CustomerProfile.Role.CUSTOMER:
            profile = CustomerProfile.objects.create(user=user,
                                                     role=profile_role)
        elif profile_role == FreelancerProfile.Role.FREELANCER:
            profile = FreelancerProfile.objects.create(user=user,
                                                       role=profile_role)
        profile.save()
        return user


class OrderNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FreelancerProfileSerializer(serializers.ModelSerializer):
    orders = OrderNestedSerializer(many=True, read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = ['id', 'user', 'name', 'contact_info', 'experience', 'role',
                  'orders']


class CustomerProfileSerializer(serializers.ModelSerializer):
    orders = OrderNestedSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'name', 'contact_info', 'experience', 'role',
                  'orders']
