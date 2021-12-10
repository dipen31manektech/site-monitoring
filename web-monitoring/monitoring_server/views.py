from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .serializers import ExceptionDetailsSerializer
from django.shortcuts import render, redirect
from .models import exceptionDetails


# Create your views here.


class ExceptionDetailsViewSet(generics.GenericAPIView):
    serializer_class = ExceptionDetailsSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response("Error Occured.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            exceptionRecord = self.serializer_class.objects.get()
            context = {
                'exceptionData': exceptionRecord,
            }
            return render(request, "exceptionmonitor/exceptionmonitor.html", context)
        except Exception as e:
            return Response("Error Occured.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def exceptionData(request):
    exceptionRecord = exceptionDetails.objects.all()
    context = {
        'exceptionData': exceptionRecord,
    }
    print(context)
    return render(request, "exceptionmonitor/exceptionmonitor.html", context)
