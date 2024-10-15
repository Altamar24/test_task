from django.db.models import Q
from rest_framework import serializers

from accounts.models import User, Chat, Message
from cats.models import Cat


class ChatListSerializer(serializers.ModelSerializer):
    companion_name = serializers.SerializerMethodField()
    last_message_content = serializers.SerializerMethodField()
    last_message_datetime = serializers.DateTimeField()

    class Meta:
        model = Chat
        fields = (
            "id",
            "companion_name",
            "last_message_content",
            "last_message_datetime",
        )

    def get_last_message_content(self, obj) -> str:
        return obj.last_message_content

    def get_companion_name(self, obj) -> str:
        companion = obj.user_1 if obj.user_2 == self.context["request"].user else obj.user_2
        return f"{companion.first_name} {companion.last_name}"


class ChatSerializer(serializers.ModelSerializer):
    user_1 = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Chat
        fields = ("id", "user_1", "user_2")
    
    def create(self, validated_data):
        request_user = validated_data["user_1"]
        second_user = validated_data["user_2"]

        chat = Chat.objects.filter(
            Q(user_1=request_user, user_2=second_user)  #в поле user_2 возвращаем id первого пользователя, если второй равен текущему (тому, который сделал запрос). Иначе возвращаем айди второго.
            | Q(user_1=second_user, user_2=request_user)
        ).first()
        if not chat:
            chat = Chat.objects.create(
                user_1=request_user,
                user_2=second_user,
            )

        return chat

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation["user_2"] = (
            obj.user_1.pk
            if obj.user_2 == self.context["request"].user
            else obj.user_2.pk
        )
        return representation


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class CatListSerializer(serializers.ModelSerializer):
    breeder = UserShortSerializer()

    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "breeder",
            "breed",
            "age",
            "hairiness",
        )


class CatCreateUpdateSerializer(serializers.ModelSerializer):
    breeder = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    
    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "breeder",
            "breed",
            "age",
            "hairiness",
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "age",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data.get('age'),
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class UserListSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "age", "is_friend")

    def get_is_friend(self, obj) -> bool:
        current_user = self.context["request"].user
        return current_user in obj.friends.all()


class NestedCatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = (
            "id",
            "name",
            "breed",
            "age",
            "hairiness",
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()
    friend_count = serializers.SerializerMethodField()
    cats = NestedCatListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "is_friend",
            "friend_count",
            "cats",
        )

    def get_friend_count(self, obj) -> int:
        return obj.friends.count()

    def get_is_friend(self, obj) -> bool:
        return obj in self.context["request"].user.friends.all()


class MessageListSerializer(serializers.ModelSerializer):
    message_author = serializers.CharField()

    class Meta:
        model = Message
        fields = ("id", "content", "message_author", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, attrs):
        chat = attrs["chat"]
        author = attrs["author"]
        if chat.user_1 != author and chat.user_2 != author:
            raise serializers.ValidationError("Вы не являетесь участником этого чата.")
        return super().validate(attrs)

    class Meta:
        model = Message
        fields = ("id", "author", "content", "chat", "created_at")
