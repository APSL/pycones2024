from django.contrib.auth import login
from drf_spectacular.utils import OpenApiResponse, extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        summary="login.",
        request=AuthTokenSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Login.",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized or invalid token."),
        },
    )
    def post(self, request, format=None):  # type: ignore
        """
        Creates a token for the user requested.
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=None)
