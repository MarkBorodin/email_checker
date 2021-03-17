from rest_framework import generics, status
from rest_framework.response import Response

from email_checker.api.serializers import APIEmailSerializer, APIEmailSerializerResponse
from email_checker.models import APIEmail, Email
from email_checker.utils import check_email_valid, check_email_accessible, check_email_catchall


class EmailCheckView(generics.ListCreateAPIView):
    serializer_class = APIEmailSerializer
    queryset = APIEmail.objects.all()

    def post(self, request, *args, **kwargs):
        email_name = request.data['email']

        request.POST._mutable = True

        request.data['valid'] = check_email_valid(email_name)
        if request.data['valid'] is True:
            request.data['accessible'] = check_email_accessible(email_name)
        else:
            request.data['accessible'] = False
        request.data['catchall'] = check_email_catchall(email_name)

        request.POST._mutable = False

        serializer = APIEmailSerializerResponse(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
