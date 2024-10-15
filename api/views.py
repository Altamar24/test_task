from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Subquery, Q
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin, 
    ListModelMixin, 
    RetrieveModelMixin, 
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from accounts.models import Message, Chat
from api.serializers import (
    UserRegistrationSerializer, 
    UserListSerializer, 
    UserRetrieveSerializer, 
    CatListSerializer, 
    CatCreateUpdateSerializer, 
    ChatSerializer,
    ChatListSerializer,
    MessageListSerializer,
    MessageSerializer
)
from cats.models import Cat

User = get_user_model()

class UserViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all().order_by("-id")

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action in ["retrieve", "me"]:
            return UserRetrieveSerializer
        return UserListSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny] #Для create используется класс AllowAny, который дает доступ к эндпоинту без аутентификации.
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    @action(detail=True, methods=["get"])
    def friends(self, request, pk=None):
        user = self.get_object()
        queryset = self.filter_queryset(
            self.get_queryset().filter(friends=user)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = User.objects.all().prefetch_related(
            "friends",
        ).order_by("-id")
        return queryset
    
    @action(detail=True, methods=["post"])
    def add_friend(self, request, pk=None):
        user = self.get_object()
        request.user.friends.add(user)
        return Response("Friend added")

    @action(detail=True, methods=["post"])
    def remove_friend(self, request, pk=None):
        user = self.get_object()
        request.user.friends.remove(user)
        return Response("Friend removed")
    

class CatViewSet(ModelViewSet):
    queryset = Cat.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return CatListSerializer
        return CatCreateUpdateSerializer
    
    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.breeder != self.request.user:
            raise PermissionDenied("Вы не являетесь заводчиком этого кота.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.breeder != self.request.user:
            raise PermissionDenied("Вы не являетесь заводчиком этого кота.")
        instance.delete()


class ChatViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ChatListSerializer
        if self.action == "messages":
            return MessageListSerializer
        return ChatSerializer
    
    def get_queryset(self):
        user = self.request.user

        last_message_subquery = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-created_at').values('created_at')[:1]
        last_message_content_subquery = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-created_at').values('content')[:1]

        qs = Chat.objects.filter(
            Q(user_1=user) | Q(user_2=user),
            messages__isnull=False,
        ).annotate(
            last_message_datetime=Subquery(last_message_subquery),
            last_message_content=Subquery(last_message_content_subquery),
        ).select_related(
            "user_1",
            "user_2",
        ).order_by("-last_message_datetime").distinct()
        return qs
    

class MessageViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all().order_by("-id")

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не являетесь автором этого сообщения.")
        instance.delete()
    