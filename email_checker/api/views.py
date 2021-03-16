from rest_framework import generics, status
from rest_framework.response import Response

from email_checker.api.serializers import APIEmailSerializer
from email_checker.models import APIEmail
from email_checker.utils import check_email_valid, check_email_accessible, check_email_catchall


class EmailCheckView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = APIEmailSerializer
    # queryset = Test.objects.all()

    # def get_queryset(self):

        # obj = APIEmail.objects.create(
        #     email=email_name,
        #     valid=check_email_valid(email_name),
        #     accessible=check_email_accessible(email_name),
        #     catchall=check_email_catchall(email_name)
        # )
        # obj.save()
        # return obj

    def post(self, request, *args, **kwargs):
        serializer = APIEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
