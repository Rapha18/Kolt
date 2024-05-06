from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser, TransactionHistory
from .serializers import CustomUserSerializer, TransactionHistorySerializer


class CreateUser(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Ce numéro de téléphone est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})

class AccountBalance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'solde': user.solde})

class TransferMoney(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        montant = request.data.get('montant')
        dest_phone_number = request.data.get('dest_phone_number')

        if not dest_phone_number or not montant:
            raise ValidationError("Le numéro de téléphone du destinataire et le montant sont requis.")

        if user.solde < montant:
            raise ValidationError("Solde insuffisant pour effectuer le transfert.")

        try:
            destinataire = CustomUser.objects.get(numero_telephone=dest_phone_number)
        except CustomUser.DoesNotExist:
            raise ValidationError("Le destinataire avec ce numéro de téléphone n'existe pas.")

        user.solde -= montant
        user.save()

        destinataire.solde += montant
        destinataire.save()

        TransactionHistory.objects.create(user=user, montant=montant, type_transaction='transfert')

        return Response({'message': 'Transfert réussi !'})

class VerifyPin(APIView):
    def post(self, request):
        pin_code = request.data.get('pin_code')
        user = request.user

        if not pin_code:
            return Response({'error': 'Le code PIN est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(user.pin_code) == pin_code:
            return Response({'message': 'Le code PIN est correct.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Le code PIN est incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionHistory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = TransactionHistory.objects.filter(user=user)
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)



class PartnerCallback(APIView):
    def post(self, request):
        data = request.data
        # Effectuez les opérations nécessaires avec les données reçues
        # Mettez à jour le solde du client en conséquence
        # Enregistrez la transaction dans l'historique
        # Retournez la réponse appropriée

        return Response({"message": "Callback received successfully."}, status=status.HTTP_200_OK)
