from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateListOderView.as_view(), name="orders"),
    path("<int:order_id>/", views.OderDetailView.as_view(), name="orders_detail"),
    path(
        "update-status/<int:order_id>/",
        views.UpdateOrderStatus.as_view(),
        name="update_order_status",
    ),
    path("user/<int:user_id>", views.GetUserOderView.as_view(), name="user_orders"),
    path(
        "user/<int:user_id>/order/<int:order_id>/",
        views.UserOderDetailView.as_view(),
        name="user_specific_order",
    ),
]
