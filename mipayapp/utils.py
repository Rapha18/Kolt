import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def credit_service(request):
    data = request.data
    payload = {
        "idRequete": data.get("idRequete"),
        "numeroClient": data.get("numeroClient"),
        "montant": data.get("montant"),
        "refCommande": data.get("refCommande"),
        "dateHeureRequete": data.get("dateHeureRequete"),
        "description": data.get("description")
    }
    response = requests.post("https://tgpp-mbanking-stp-gw-gen.togocom.tg/m-banking/v1/api/tpcredit", json=payload)
    return Response(response.json(), status=response.status_code)

@api_view(['POST'])
def handle_credit_response(request):
    data = request.data
    # Traitez la réponse en conséquence
    return Response({"message": "Credit response received."})

@api_view(['GET'])
def check_credit_request_status(request):
    id_requete = request.query_params.get('idRequete')
    response = requests.get(f"https://tgpp-mbanking-stp-gw-gen.togocom.tg/m-banking/v1/api/tpcredit/check-transaction-id?idRequete={id_requete}")
    return Response(response.json(), status=response.status_code)

# Définissez les URLs Django
urlpatterns = [
    path('credit-service/', views.credit_service, name='credit_service'),
    path('handle-credit-response/', views.handle_credit_response, name='handle_credit_response'),
    path('check-credit-request-status/', views.check_credit_request_status, name='check_credit_request_status'),
]


@api_view(['POST'])
def debit_push_ussd(request):
    data = request.data
    payload = {
        "numeroClient": data.get("numeroClient"),
        "montant": data.get("montant"),
        "refCommande": data.get("refCommande"),
        "dateHeureRequete": data.get("dateHeureRequete"),
        "description": data.get("description")
    }
    response = requests.post("https://tgpp-mbanking-stp-gw-gen.togocom.tg/push-api/v1/debit", json=payload)
    return Response(response.json(), status=response.status_code)

@api_view(['POST'])
def partner_callback(request):
    data = request.data
    # Effectuez les opérations nécessaires avec les données reçues
    return Response({"message": "Callback received successfully."})

@api_view(['GET'])
def check_transaction_status(request):
    id_requete = request.query_params.get('idRequete')
    response = requests.get(f"https://tgpp-mbanking-stp-gw-gen.togocom.tg/push-api/v1/transactionid?idRequete={id_requete}")
    return Response(response.json(), status=response.status_code)

# URLs Django
urlpatterns = [
    path('debit-push-ussd/', views.debit_push_ussd, name='debit_push_ussd'),
    path('partner-callback/', views.partner_callback, name='partner_callback'),
    path('check-transaction-status/', views.check_transaction_status, name='check_transaction_status'),
]




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import CustomUser, TransactionHistory
from .serializers import CustomUserSerializer, TransactionHistorySerializer

class CreditService(APIView):
    def post(self, request):
        data = request.data
        payload = {
            "idRequete": data.get("idRequete"),
            "numeroClient": data.get("numeroClient"),
            "montant": data.get("montant"),
            "refCommande": data.get("refCommande"),
            "dateHeureRequete": data.get("dateHeureRequete"),
            "description": data.get("description")
        }
        response = requests.post("https://tgpp-mbanking-stp-gw-gen.togocom.tg/m-banking/v1/api/tpcredit", json=payload)

        if response.status_code == 200:
            # Mettre à jour le solde du client
            user = CustomUser.objects.get(numero_telephone=data.get("numeroClient"))
            user.solde += data.get("montant")
            user.save()

            # Enregistrer la transaction dans l'historique
            TransactionHistory.objects.create(
                user=user,
                montant=data.get("montant"),
                type_transaction='recharge',  # ou le type approprié
            )

            return Response({"message": "Recharge réussie !"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Échec de la recharge !"}, status=status.HTTP_400_BAD_REQUEST)

class DebitPushUSSD(APIView):
    def post(self, request):
        data = request.data
        payload = {
            "numeroClient": data.get("numeroClient"),
            "montant": data.get("montant"),
            "refCommande": data.get("refCommande"),
            "dateHeureRequete": data.get("dateHeureRequete"),
            "description": data.get("description")
        }
        response = requests.post("https://tgpp-mbanking-stp-gw-gen.togocom.tg/push-api/v1/debit", json=payload)

        if response.status_code == 200:
            # Mettre à jour le solde du client
            user = CustomUser.objects.get(numero_telephone=data.get("numeroClient"))
            user.solde -= data.get("montant")
            user.save()

            # Enregistrer la transaction dans l'historique
            TransactionHistory.objects.create(
                user=user,
                montant=data.get("montant"),
                type_transaction='retrait',  # ou le type approprié
            )

            return Response({"message": "Retrait réussi !"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Échec du retrait !"}, status=status.HTTP_400_BAD_REQUEST)

class PartnerCallback(APIView):
    def post(self, request):
        data = request.data
        # Effectuez les opérations nécessaires avec les données reçues
        # Mettez à jour le solde du client en conséquence
        # Enregistrez la transaction dans l'historique
        # Retournez la réponse appropriée

        return Response({"message": "Callback received successfully."}, status=status.HTTP_200_OK)


