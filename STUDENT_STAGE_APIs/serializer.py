from .models import profile, question, answer, notifiaction, news, e_book
from .models import AI_Chatroom, AI_Prompt
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'id', 
                'username', 
                'email'
                ]

class profileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = profile
        fields = [
            'id',
            'user', 
            'full_name', 
            'image', 
            'address', 
            'role', 
            'date_joined', 
            'sector', 
            'marked_as'
            ]
        


class questionSerializer(serializers.ModelSerializer):
    profile = profileSerializer(read_only=True)
    class Meta:
        model = question
        fields = [
                'id', 
                'profile', 
                'tutor_assign', 
                'question_text', 
                'question_image', 
                'date', 
                'question_catagory', 
                'answer_id',
                'status'
                ]
        
    def create(self, validated_data):
        user = self.context['request'].user
        print('user:', user)
        obj_profile = profile.objects.filter(user=user).first()
        print('profile:', obj_profile)
        if obj_profile:
            created = question.objects.create(profile=obj_profile, **validated_data)
            return created
        
        


class answerSerializer(serializers.ModelSerializer):
    tutor_answered = UserSerializer(read_only=True)
    question = questionSerializer(read_only=True)
    class Meta:
        model = answer
        fields = [
                'id',
                'question', 
                'tutor_answered', 
                'answer_title',
                'answer_body', 
                'answer_image',
                'answer_feedback',
                ]
    def create(self, validated_data):
        user = self.context['request'].user
        q_id = self.context['id']
        print(q_id)
        obj_question = question.objects.get(id=q_id)
        if user:
            print('pass user getted')
            if obj_question:
                print('pass question getted')
                created = answer.objects.create(tutor_answered=user, question=obj_question, **validated_data)
                return created
        


class notifiactionSerializer(serializers.ModelSerializer):
    reciever = UserSerializer(read_only=True)
    class Meta:
        model = notifiaction
        fields = [
                'reciever', 
                'question', 
                'answer', 
                'status', 
                'feadback',
                'type',
                ]
        

class newsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = news
        fields = [
            'id',
            'author', 
            'news_title', 
            'news_body', 
            'news_images', 
            'news_clip', 
            'sector', 
            'reference', 
            'date_published', 
            'category_raleted'
            ]
    def create(self, validated_data):
        user = self.context['request'].user
        if user:
            created = news.objects.create(author=user, **validated_data)
            return created
        


class e_bookSerializer(serializers.ModelSerializer):
    user_posted = UserSerializer(read_only=True)
    class Meta:
        model = e_book
        fields = [
                'id',
                'book_name', 
                'book_price', 
                'book_publisher', 
                'book_category', 
                'book_origin', 
                'user_posted', 
                'free_version'
                ]
    def create(self, validated_data):
        user = self.context['request'].user
        created = e_book.objects.create(user_posted=user, **validated_data)
        return created
        

class AI_ChatroomSerializer(serializers.ModelSerializer):
    user = profileSerializer(read_only=True)
    class Meta:
        model = AI_Chatroom
        fields = [
            'id', 
            'user', 
            'room_name'
            ]
        
    def create(self, validated_data):
        user = self.context['request'].user
        obj_profile = profile.objects.get(user=user)
        if obj_profile:
            created = AI_Chatroom.objects.create(user=obj_profile,**validated_data)
        

class AI_promptserializer(serializers.ModelSerializer):
    class Meta:
        model = AI_Prompt
        fields = [
            'id', 
            'prompt', 
            'responce', 
            'AI_Chatroom_id'
                ]