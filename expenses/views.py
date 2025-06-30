# expenses/views.py
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .models import User


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ["get", "post", "put", "patch", "delete"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "user__email",
        "category",
        "date",
        "note",
        "type"
    ]
    ordering_fields = [
        "category",
        "date",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        request = self.request
        category = request.query_params.get("category", None)
        date = request.query_params.get("date", None)
        queryset = self.queryset.filter(user=request.user)
        if category:
            queryset = queryset.filter(category=category)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def create(self, request, *args, **kwargs):

        try:
            data = request.data
            user = request.user
            data['user'] = user.id
            if data.get('operation'):
                response_data = {
                    "error": f"error: No operation Found, Must Add the Operation To Do",
                }
                return Response(
                    response_data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = TransactionSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # update user's Balance
            current_balance = user.balance
            data = request.data
            if data.get('operation') == 'debited':
                new_balance = current_balance - data.get('amount')
            elif data.get('operation') == 'credited':
                new_balance = current_balance + data.get('amount')
            else:
                new_balance = user.balance

            user.balance = new_balance
            user.save()

            response_data = {
                "message": "New Transaction Added",
            }
            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            response_data = {
                "error": f"error: {e}",
            }
            return Response(
                response_data,
                status=status.HTTP_400_BAD_REQUEST
            )



