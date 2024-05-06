
from rest_framework import serializers
from .models import CustomUser, TransactionHistory

class CustomUserSerializer(serializers.ModelSerializer):
    mot_de_passe = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'nom_complet', 'numero_telephone', 'mot_de_passe', 'solde')
        
    def create(self, validated_data):
        mot_de_passe = validated_data.pop('mot_de_passe', None)
        user = CustomUser.objects.create(**validated_data)
        if mot_de_passe is not None:
            user.set_password(mot_de_passe)
            user.save()

        return user

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ('id', 'user', 'montant', 'type_transaction', 'date')
