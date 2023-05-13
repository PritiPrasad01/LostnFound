from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

CATEGORY_CHOICES = (
    ('L','Lost'),
    ('F','Found')
)
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    location = models.CharField(max_length=30)
    color = models.CharField(max_length=30,blank=True)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(null=True,blank = True,upload_to='productimg')
    created_at = models.DateTimeField(default=timezone.now)

GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer Not to Say','Prefer Not to Say'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=10)
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES)
    profile_pic = models.ImageField(null=True,blank = True,upload_to='profilepic')
    birth_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
@receiver(post_save, sender=User)
def update_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class UserOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.created_at)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.created_at)