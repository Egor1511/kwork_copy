from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import FreelancerProfile
from users.serializers import UserRegisterSerializer
from users.services import get_profile_serializer, get_user_profile

User = get_user_model()


class RegisterView(APIView):
    @atomic
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = get_user_profile(user)
        if not profile:
            return Response({"error": "Profile not found"}, status=404)
        serializer_class = get_profile_serializer(profile)
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        profile = get_user_profile(user)
        if not profile:
            return Response({"error": "Profile not found"}, status=404)
        serializer_class = get_profile_serializer(profile)
        serializer = serializer_class(
            profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


