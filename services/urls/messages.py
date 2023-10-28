from django.urls import path

from ..views import ConversationList, MessageListCreate

urlpatterns = [
    path("/me/inbox", ConversationList.as_view(), name="inbox-for-user"),
    path(
        "/me/inbox/<uuid:organization_uuid>",
        MessageListCreate.as_view(),
        name="message-create-for-user",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/inbox",
        ConversationList.as_view(),
        name="inbox-for-org",
    ),
    path(
        "/organizations/<uuid:organization_uuid>/inbox/<uuid:user_uuid>",
        MessageListCreate.as_view(),
        name="message-create-for-org",
    ),
]
