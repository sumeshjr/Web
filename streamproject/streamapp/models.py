from django.db import models 
from django.conf import settings

class UserReg(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=20,null=True)
    password=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    profileimage = models.ImageField(upload_to='profile/',blank=True)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image=models.ImageField(null=True, upload_to="cat/")

    def __str__(self):
        return self.name



class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumb_image = models.ImageField(null=True, upload_to='thumb_img/')
    fav = models.ManyToManyField(UserReg, related_name='favorite_videos', blank=True)
    like = models.ManyToManyField(UserReg, related_name='like', blank=True)

    def __str__(self):
        return self.title



class RecentUpdate(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='recent_update_images/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    email = models.EmailField(null=True)
    name = models.CharField(max_length=100,null=True)
    suggestion = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.email
    


class Comment(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    text = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Home(models.Model):
    image = models.ImageField(null=True, upload_to='images_home/')
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

