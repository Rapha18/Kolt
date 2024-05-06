from django.urls import path
from .views import CreateUser, CustomAuthToken, AccountBalance, TransferMoney, VerifyPin, TransactionHistory, PartnerCallback

urlpatterns = [
    path('account/create-user/', CreateUser.as_view(), name='create_user'),
    path('account/api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('account/account-balance/', AccountBalance.as_view(), name='account_balance'),
    path('service/transfer-money/', TransferMoney.as_view(), name='transfer_money'),
    path('account/verify-pin/', VerifyPin.as_view(), name='verify_pin'),
    path('account/transaction-history/', TransactionHistory.as_view(), name='transaction_history'),
    path('account/tmoney-callback/', PartnerCallback.as_view(), name='tmoney_callback'),
]
