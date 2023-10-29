from django.urls import path

from ..views import ConversationListForOrganization, ConversationListForPatient, MessageListCreateForPatient, MessageListCreateForOrganization

urlpatterns = [
    path("/me/inbox", ConversationListForPatient.as_view(), name="inbox-for-user"),
    path(
        "/me/inbox/<uuid:organization_uuid>",
        MessageListCreateForPatient.as_view(),
        name="message-create-for-user",
    ),
    path(
        "/we/<uuid:organization_uuid>/inbox",
        ConversationListForOrganization.as_view(),
        name="inbox-for-organization",
    ),
    path(
        "/we/<uuid:organization_uuid>/inbox/<uuid:user_uuid>",
        MessageListCreateForOrganization.as_view(),
        name="message-create-for-organization",
    ),
]
