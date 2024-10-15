from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, CatViewSet, ChatViewSet, MessageViewSet

router = SimpleRouter()
router.register(r'cats', CatViewSet, basename="cats")
router.register(r'chats', ChatViewSet, basename="chats")
router.register(r'users', UserViewSet, basename="users")
router.register(r'messages', MessageViewSet, basename="messages")

urlpatterns = router.urls
