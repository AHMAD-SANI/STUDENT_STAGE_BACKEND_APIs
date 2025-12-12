from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializer import questionSerializer, answerSerializer, newsSerializer, UserSerializer
from .serializer import e_bookSerializer, profileSerializer
from .models import question,  answer, news, e_book, profile
from .models import AI_Chatroom, AI_Prompt
from .serializer import AI_ChatroomSerializer, AI_promptserializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from  rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from .permissions import isAdminUser, isTutorOrAdmin, owner_Tutor_Admin, isValidUser
from .permissions import isTutorOrAdminEdit, profilePermision, ownerOnly

# Group members list and info about them


@api_view(['POST'])
def register(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    confirm_password = request.data['confirm_password']
    print(username)
    print(email)
    print(password)
    if password == confirm_password:
        filter1 = User.objects.filter(email=email).first()
        print('filter1 successful...')
        if filter1 == None:
            filter2 = User.objects.filter(username=username).first()
            print('filter2 successful...')
            if filter2 == None:
                user = User.objects.create(username=username, email=email, password=password )
                print('user created successful...')

                tokens = Token.objects.create(user=user)

                print('Token created successful...')
                serializer = UserSerializer(user)
                print('serializered the data successful...')
                print(serializer.data)
                print(tokens)
                key = {
                    'user': serializer.data,
                    'ACCESS TOKEN': tokens.key,
                        }
                return Response(key)
            return Response({'message': 'the username already taken by another user'})
        return Response({'message': 'the email already taken by another user'})
    return Response({'message': 'the password dismarch....'})



@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    if email != None:
        if password != None:
            user = User.objects.get(email=email, password=password)
            if user:
                serializer = UserSerializer(user)
                user_login = authenticate(user)
                Access_token, created = Token.objects.get_or_create(user=user)
                key = {
                    'user': serializer.data,
                    'Access Token': Access_token.key,
                    }
                return Response(key)
            return Response({'message': 'such user doesnt exist with the informations provided'})
        return Response({'message': 'the password field cannot be empty'})
    return Response({'message': 'the email cannot be empty'})
    
    
    
from rest_framework.decorators import authentication_classes, permission_classes, renderer_classes

@api_view(['get'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def request_user_profile(request):
    obj_user = request.user
    user_profile = profile.objects.filter(user=request.user).first()
    if user_profile:
        serializer = profileSerializer(user_profile)
        print(serializer.data)
        return Response(serializer.data)
    return Response(serializer.errors)


from django.contrib.auth.models import Group

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, isAdminUser])
@renderer_classes([JSONRenderer])
def Adding_user_to_group(request, group_name, user_id):
    try:
        group_name = group_name.upper()
        user = user_id

        user_obj = User.objects.get(id=user)
        group = Group.objects.get(name=group_name)
        user_obj.groups.add(group)

        profile_obj = profile.objects.get(user=user_obj)
        if profile_obj:
            profile_obj.role = group_name
            profile_obj.save()

            serializer = profileSerializer(profile_obj)
            return Response(serializer.data)
        return Response({'message':'opps, the profile object not found.'})
    except:
        return Response({'message':'something went wrong, try again...'})



@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated, isAdminUser])
@renderer_classes([JSONRenderer])
def remove_user_to_group(request, group_name, user_id):
    try:
        group_name = group_name.upper()
        user = user_id

        user_obj = User.objects.get(id=user)
        group = Group.objects.get(name=group_name)
        user_obj.groups.remove(group)

        profile_obj = profile.objects.get(user=user_obj)
        if profile_obj:
            if  group_name == "STUDENT":
                profile_obj.role = "BANNED"
                profile_obj.save()
            else:
                profile_obj.role = "STUDENT"
                profile_obj.save()

            serializer = profileSerializer(profile_obj)
            return Response(serializer.data)
        return Response({'message':'opps, the profile object not found.'})
    except:
        return Response({'message':'something went wrong, try again...'})
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def logout(request):
    user = request.user
    try:
        user.auth_token.delete()
    except:
        return Response({'MESSAGE': 'user token not found..'})
    return Response({'MESSAGE': 'token deleted you are now log out..'})





@api_view(['GET'])
@permission_classes([isTutorOrAdmin])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def group_members(request, group_name):
    group_name = group_name.upper()
    group_obj = User.objects.filter(groups__name=group_name)
    profiles_list = []
    for user_obj in group_obj:
        profile_obj = profile.objects.get(user=user_obj)
        profiles_list.append(profile_obj)

    serializer = profileSerializer(profiles_list, many=True)
    return Response(serializer.data)

    


@api_view(['GET'])
@permission_classes([IsAuthenticated, isTutorOrAdmin])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def statistics(request):
    question_obj = question.objects.count()
    users = User.objects.count()
    answers = answer.objects.count()
    e_books = e_book.objects.count()
    admin = profile.objects.filter(role='ADMIN').count()
    tutor = profile.objects.filter(role='TUTOR').count()
    student = profile.objects.filter(role='STUDENT').count()
    data = {
        'USERS': users,
        'QUESTIONS': question_obj,
        'ANSWERS' : answers,
        'BOOKS' : e_books,
        'ADMINS' : admin,
        'TUTORS' : tutor,
        'STUDENT': student,
        }
    return Response(data)




class profileview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = profile.objects.all()
        serializer = profileSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = profileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [isTutorOrAdmin()]
        else:
            return [isAdminUser()]
        
    



class profileinstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        try:
            obj = profile.objects.get(id=pk)
        except:
            return Response({'MESSEGE':'the profile does not exists'})
        if obj:
            serializer = profileSerializer(obj)
            return Response(serializer.data)
        return Response({'MESSEGE':'the profile does not exists'})
    
    def put(self, request, pk):
        try:
            obj = profile.objects.get(id=pk)
        except:
            return Response({'MESSEGE':'the profile does not exists'})
        if obj.user == request.user:
            serializer = profileSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({'Messege': 'You have no permision to perform that action.'})
    
    def delete(self, request, pk):
        obj = profile.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [ownerOnly()]




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def userQs(request):
    user = request.user
    profile_obj = profile.objects.get(user=user)
    question_obj = question.objects.filter(profile=profile_obj)
    serializer = questionSerializer(question_obj, many=True)
    return Response(serializer.data)


class questionview(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_throttles(self):
        if self.request.method  == 'POST':
            self.throttle_scope = 'question_post'

        else:
            self.throttle_scope = 'default'

        return super().get_throttles()
    
    def get(self, request):
        obj = question.objects.all()
        serializer = questionSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = questionSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isValidUser()]
    
    
            

    



class questioninstanceview(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, pk):
        obj = question.objects.get(id=pk)
        serializer = questionSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = question.objects.get(id=pk)
        serializer = questionSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = question.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [owner_Tutor_Admin()]



@api_view(['GET'])
@permission_classes([IsAuthenticated, isTutorOrAdmin])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def adminAns(request):
    user = request.user
    answer_obj = answer.objects.filter(tutor_answered=user)
    serializer = answerSerializer(answer_obj, many=True)
    return Response(serializer.data)



class answeerview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = answer.objects.all()
        serializer = answerSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        q_id = request.query_params['id']
        serializer = answerSerializer(data=request.data, context={'request': request, "id":q_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]
        
    



class answerinstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        obj = answer.objects.get(id=pk)
        serializer = answerSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = answer.objects.get(id=pk)
        serializer = answerSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = answer.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]


from .models import notifiaction
from .serializer import notifiactionSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@renderer_classes([JSONRenderer])
def notifications(request):
    user = request.user
    try:
        notification_obj = notifiaction.objects.filter(reciever=user)
    except:
        return Response({'MESSAGE': 'user token not found..'})
    serializer = notifiactionSerializer(notification_obj)
    return Response(serializer.data)



class newsview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = news.objects.all()
        serializer = newsSerializer(obj, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = newsSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]
    





class newsinstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        obj = news.objects.get(id=pk)
        serializer = newsSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = news.objects.get(id=pk)
        serializer = newsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = news.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]
    




class e_bookview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = e_book.objects.all()
        serializer = e_bookSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = e_bookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]
    




class e_bookinstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        obj = e_book.objects.get(id=pk)
        serializer = e_bookSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = e_book.objects.get(id=pk)
        serializer = e_bookSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = e_book.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        else:
            return [isTutorOrAdminEdit()]
    


class AI_chatroomview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = AI_Chatroom.objects.filter(user=request.user)
        serializer = e_bookSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AI_ChatroomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    




class AI_chatroominstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        obj = AI_Chatroom.objects.get(id=pk)
        serializer = AI_ChatroomSerializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = AI_Chatroom.objects.get(id=pk)
        serializer = AI_ChatroomSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = AI_Chatroom.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    


class AI_promptview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        obj = AI_Prompt.objects.filter(user=request.user)
        serializer = AI_promptserializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AI_promptserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    




class AI_promptinstanceview(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        obj = AI_Prompt.objects.get(id=pk)
        serializer = AI_promptserializer(obj)
        return Response(serializer.data)
    
    def put(self, request, pk):
        obj = AI_Prompt.objects.get(id=pk)
        serializer = AI_promptserializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        obj = AI_Prompt.objects.get(id=pk)
        if obj:
            obj.delete()
            return Response({'mesage': 'object have been deleted'})
        return Response({'message': 'object does not found'})
    

