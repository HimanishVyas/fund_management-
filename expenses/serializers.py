# expenses/serializers.py
from rest_framework import serializers
from .models import (
    Transaction,
    Budget,
    Income

)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'category', 'date', 'note']


class BudgetSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'user', 'user_full_name', 'category', 'month',
            'amount', 'created_at'
        ]
        read_only_fields = ['created_at', 'user_full_name']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()


class IncomeSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Income
        fields = [
            'id', 'user', 'user_full_name', 'amount', 'source',
            'date', 'note', 'created_at'
        ]
        read_only_fields = ['created_at', 'user_full_name']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
