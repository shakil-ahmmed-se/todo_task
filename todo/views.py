from django.shortcuts import render,redirect
from rest_framework import viewsets
from .serializers import TodoSerializer,PriorityChoiceSerializer
from .models import Todo, PriorityChoices, Profile
from . import serializers
from rest_framework import filters, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response("User Sign Up successful")
        return Response(serializer.errors)
    
def activate(req, uid64, token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    def post(self,request):
        serializer = serializers.UserLoginSerializers(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user=authenticate(username=username, password=password)

            if user:
                login(request, user)
                token, _=Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({"error": "invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, req):
        try:
            print(req.user)
            req.user.auth_token.delete()
            logout(req)
            return Response({"message": "logout Successfull"})
        except:
            return Response({"message": "failed to logout"})
        # return redirect('login')
    
class UsersInfo(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= serializers.UserSerializer

class ProfileInfo(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class= serializers.UserProfileSerializer



# my Main
# class TodoPagination(pagination.PageNumberPagination):
#     page_size = 3
#     page_size_query_param = page_size
#     max_page_size = 100
# pagination krle array change hoye jay



class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by("-id")
    permission_classes = [AllowAny]
    # pagination_class= TodoPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'priority__name']
    filterset_fields = {'completed':['exact']}


class PriorityChoiceViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = PriorityChoices.objects.all()
    serializer_class = serializers.PriorityChoiceSerializer