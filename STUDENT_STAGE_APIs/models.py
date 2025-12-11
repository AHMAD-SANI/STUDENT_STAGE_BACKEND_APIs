from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='media/profile_images', blank=True)
    address = models.TextField(blank=True)
    role  = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now=True)
    sector = models.CharField(max_length=100, blank=True)
    marked_as = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, default='000000000')

    def __str__(self):
        return self.user.username


class question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(profile, on_delete=models.CASCADE, null=False)
    tutor_assign = models.ForeignKey(User, related_name='tutor_assign', blank=True, null=True, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='media/questions_images', blank=True)
    date = models.DateTimeField(auto_now=True)
    question_catagory = models.CharField(max_length=100)
    answer_id = models.IntegerField(blank=True, default=0)
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.question_text


class answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    tutor_answered = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_title = models.TextField(blank=True)
    answer_body = models.TextField()
    answer_image = models.ImageField(upload_to='media/answer_images', blank=True)
    answer_feedback = models.TextField(blank=True)

    def __str__(self):
        return self.answer_body


class notifiaction(models.Model):
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer = models.ForeignKey(answer, blank=True,  on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    feadback = models.TextField(null=True)
    type = models.TextField(blank=True, null=True)





class e_book(models.Model):
    book_name = models.CharField(max_length=200)
    book_file  = models.FileField(upload_to='media/e_books_files', blank=True, null=True)
    book_poster  = models.FileField(upload_to='media/e_books_posters', blank=True, null=True)
    book_price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    book_publisher = models.CharField(max_length=200)
    book_summery = models.TextField(blank=True)
    year_published = models.DateField(blank=True, null=True)
    book_category = models.CharField(max_length=100)
    book_origin = models.TextField(blank=True)
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    free_version = models.BooleanField(default=False)

    def __str__(self):
        return self.book_name



class news(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    news_title = models.TextField(blank=True)
    news_body = models.TextField()
    news_images = models.ImageField(upload_to='media/news_images', blank=True)
    news_clip = models.FileField(upload_to='media/news_clips', blank=True)
    sector = models.CharField(max_length=100, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    date_published = models.DateTimeField(auto_now=True)
    category_raleted = models.CharField(max_length=100)

    def __str__(self):
        return self.news_title
    



class AI_Prompt(models.Model):
    prompt = models.TextField()
    responce = models.TextField()
    AI_Chatroom_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt



class AI_Chatroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=200)
    prompt = models.ManyToManyField(AI_Prompt)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name
    


    