from django.db import models
from django.contirb.auth.models import AbstractUser 
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signal import post_save
from django.utils.translation import gettext_lazy as _


# Create your models here.







class User(AbstractUser) :

    class Role(models.TextChoices) :
        MODERATOR = 'MD',_("moderator")
        JUDGE = "JD",_("judge")
        DELIGATE= "DT",_("deligate")

        
    username = models.CharField(max_length=255) 
    email =  models.EmailField(unique=True)
    role = models.CharField(max_length=30,
    choices=Role.choices,
    blank=True)



class Country(models.Model) :
    flag = models.ImageField(default='/media/country_flag',upload_to='/media/country/')
    name = models.CharField(max_length=255) 
    _id = models.CharField(max_length=255)


class Team(models.Model) ;
    name = models.CharField(max_length=255,blank=True)
    info = models.TextField(blank=True) 
    city = models.CharField(max_length=255,blank=True)
    leader= models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True,related_name='team')
    score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)





class DeligateProfile(models.Model) :
    user= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='deligate_profile')
    team = models.ForeignKey(Team,related_name='user',on_delete=models.CASCADE)
    country = models.OneToOneField(Country,related_name='deligate',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact = models.IntegerField(max_length=20)


    class Meta :
        verbose_name="deligateprofile"


@receiver(post_save,sender=settings.AUTH_USER_MODEL) 
def create_profile(sender,instance,created,**kwargs) :
   if created and instance.role=="DT":
       DeligateProfile.objects.create(user=instance,first_name=instance.username)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def update_profile(sender,instance,created,**kwargs) :
    try:
       if instance.role=="DT" :
             instance.deligate_profile.save()
    except:
        if instance.role=="DT" :
           DeligateProfile.objects.create(user=instance)





class Profile(models.Model) :
    user= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    contact = models.IntegerField(max_length=20)

    class Meta :
        verbose_name="judge_and_moderator_profile"


@receiver(post_save,sender=settings.AUTH_USER_MODEL) 
def create_profile(sender,instance,created,**kwargs) :
   if created and instance.role!="DT":
       Profile.objects.create(user=instance,Name=instance.username)

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def update_profile(sender,instance,created,**kwargs) :
    try:
       if instance.role!="DT" :
             instance.deligate_profile.save()
    except:
        if instance.role!="DT" :
           Profile.objects.create(user=instance)








