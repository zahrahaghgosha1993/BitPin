from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from app.models import UserScoreContent, Content
from app.serializers import UserScoreContentCreateSerializer, ContentListSerializer


class ContentListApiview(ListAPIView):
    serializer_class = ContentListSerializer
    queryset = Content.objects.all()
    # because of too many queries we have to cache serializer.data


class UserContentScoreUpdateCreateApiview(CreateAPIView):
    serializer_class = UserScoreContentCreateSerializer
    queryset = UserScoreContent.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)

    def create_or_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create_or_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create_or_update(self, serializer):
        serializer.save()
