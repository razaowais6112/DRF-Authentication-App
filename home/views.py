from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication




# Create your views here.
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        
        request.user.auth_token.delete()
        return Response({'status': True, 'messgae': 'user logged-out'},
            status=status.HTTP_200_OK)

class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        username = request.data.get('username')
        password = request.data.get('password')
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
    
        print(request.user)
        # user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        # user = authenticate(username = username, password = password)

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)

            if check_password(password, user.password):
                token, _ = Token.objects.get_or_create(user = user)

                return Response({
                    'status' : True,
                    'message': 'user logged-in',
                    'token': str(token)
                    }, status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except User.DoesNotExist:
            return Response({'error': 'User Not Found.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        # if not user:
        #     return Response({
        #         'status' : False,
        #         'message' : 'invalid credentials' 
        #     }, status.HTTP_400_BAD_REQUEST)
        
        # token, _ = Token.objects.get_or_create(user = user)

        # return Response({
        #     'status' : True,
        #     'message': 'user logged-in',
        #     'token': str(token)
        #     }, status.HTTP_202_ACCEPTED)
    



class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({'status': True, 'message': 'user created'}, status.HTTP_201_CREATED)
    
class StudentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # student_objs = Student.objects.filter(color__isnull = False)
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)
        return Response({'status':200, 'payload': serializer.data})

    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'your data is saved'})

    def put(self, request):
        data = request.data
        student_obj = Student.objects.get(id = data['id'])
        serializer = StudentSerializer(student_obj, data=data,partial = True)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'Changes Made'})
    
    def patch(self, request):
        data = request.data
        student_obj = Student.objects.filter(id = data['id'])
        if not student_obj.exists():
            return Response({'status': False,'message' : 'invalid id'},status.HTTP_400_BAD_REQUEST)
        
        student_obj = Student.objects.get(id = data['id'])
        serializer = StudentSerializerPatch(student_obj, data=data,partial = True)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'Partial Changes Made'})

    # def patch(self, request):
    #     data = request.data
    #     student_obj = Student.objects.filter(id = data['id'])
    #     if not student_obj.exists():
    #         return Response({'status': False,'message' : 'invalid id'},status.HTTP_400_BAD_REQUEST)
    #     serializer = StudentSerializer(student_obj, data=data, partial= True)

    #     if not serializer.is_valid():
    #         # print(serializer.errors)
    #         return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
    #     serializer.save()
        
    #     return Response({'status':200, 'payload': serializer.data, 'message': 'Partial Changes Made'})

    def delete(self, request):
        data = request.data
        student_obj = Student.objects.get(id = data['id'])
        student_obj.delete()
        return Response({'message' : 'Student details deleted'})


        

# @api_view(['POST'])
# def login(request):
#     data = request.data
#     serializer = LoginSerializer(data=data)

#     if serializer.is_valid():
#         data = serializer.validated_data
#         print(data)
#         return Response({'message':'success'})
    
#     return Response(serializer.errors)


@api_view(["GET","POST","PUT","PATCH","DELETE"])
def student(request):


    if request.method == "GET" :
        # student_objs = Student.objects.filter(color__isnull = False)
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs, many=True)
        return Response({'status':200, 'payload': serializer.data})
    
    elif request.method == "POST":
        data = request.data
        serializer = StudentSerializer(data=data)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'your data is saved'})
    
    elif request.method == "PUT":
        data = request.data
        student_obj = Student.objects.get(id = data['id'])
        serializer = StudentSerializer(student_obj, data=data)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'Changes Made'})
    
    elif request.method == "PATCH":
        data = request.data
        student_obj = Student.objects.get(id = data['id'])
        serializer = StudentSerializer(student_obj, data=data, partial= True)

        if not serializer.is_valid():
            # print(serializer.errors)
            return Response({'status':403, 'errors': serializer.errors , 'message': 'something went wrong'})
        
        serializer.save()
        
        return Response({'status':200, 'payload': serializer.data, 'message': 'Partial Changes Made'})
    
    elif request.method == "DELETE":
        data = request.data
        student_obj = Student.objects.get(id = data['id'])
        student_obj.delete()
        return Response({'message' : 'Student details deleted'})


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
        
        serializer = StudentSerializer(queryset, many=True)
        return Response({ 'status' : 200, 'data' : serializer.data }, status= status.HTTP_200_OK)
    





