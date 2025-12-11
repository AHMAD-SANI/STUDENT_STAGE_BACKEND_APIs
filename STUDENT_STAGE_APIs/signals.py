from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import profile, answer, question
from django.contrib.auth.models import User
from .models import notifiaction
from django.contrib.auth.models import Group
from .models import question


@receiver(post_save, sender=User)
def profile_signal(instance, created, sender, **kwargs):
    if created:
        obj = profile.objects.create(user=instance, role='STUDENT')
        obj.save()
        print('about to Add to the student group ')
        group = Group.objects.get(name="STUDENT")
        user = User.objects.get(username=instance.username)
        user.groups.add(group)
        print('Added to the student group successfully')


@receiver(post_save, sender=answer)
def answer_signal(instance, created, sender, **kwargs):
    if created:
        print('congrat your signals trigered successfully....')
        #NOTIFICATION UPDATE
        receiver = instance.question.profile.user
        questions = instance.question
        answer = instance
        status = True
        if instance.answer_feedback:
            feed_back = instance.answer_feedback
        notifiaction_type = 'Qusetion answered successfully.'
        send_notificatin = notifiaction.objects.create(
                                                reciever=receiver, 
                                                question=questions, 
                                                answer=answer, 
                                                status=status,
                                                type=notifiaction_type,
                        
                                                )
        send_notificatin.save()
        print('congrat your signals successfully....')

        #QUESTION UPDATE
        question_update = question.objects.get(id=instance.question.id)
        question_update.status = 'Answered'
        question_update.answer_id = instance.id
        question_update.save()
        print('congrat your question model updated successfully....')

        




