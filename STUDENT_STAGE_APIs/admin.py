from django.contrib import admin
from .models import profile, question, answer, notifiaction, e_book, AI_Chatroom
from .models import news, AI_Prompt



admin.site.register(profile)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(notifiaction)
admin.site.register(news)
admin.site.register(e_book)
admin.site.register(AI_Prompt)
admin.site.register(AI_Chatroom)
