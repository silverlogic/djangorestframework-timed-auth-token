from rest_framework.generics import CreateAPIView

from .serializers import TimedAuthTokenCreateSerializer


class TimedAuthTokenCreateView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = TimedAuthTokenCreateSerializer
