from django.urls import path

from src.user import views
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
    path("account/address/", views.AddressUpdateView.as_view(), name="account_address"),
    path("account/info/", views.InfoUpdateView.as_view(), name="account_info"),
    path("account/recovery_password/", views.ChangePassword.as_view(), name="account_recovery_password"),
    path("account/orders-history/", views.OrderHistoryListView.as_view(), name="order_history"),
    path("account/transaction-history/", views.TransactionListView.as_view(), name="transaction_history"),
    path("password_reset/", views.AsyncPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.AsyncPasswordResetViewDone.as_view(), name="password_reset_done"),
    path(
        "password-change/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password-change/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
