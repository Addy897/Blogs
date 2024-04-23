from django.db import models
from django.db import Error
import datetime,uuid
account_levels = ( 
    ("1", "Premium1"), 
    ("2", "Premium2"), 
    ("3", "Premium3"), 
) 
topics = ( 
    ("1", "Topic1"), 
    ("2", "Topic2"), 
    ("3", "Topic3"), 
    ("4", "Misc"), 
) 
access_levels = ( 
    ("1", "Read"), 
    ("2", "ReadWrite"), 
    ("3", "Admin"), 
)
status_levels=( 
    ("1", "Draft"), 
    ("2", "InReview"), 
    ("3", "Published"), 
)
# Create your models here.
class EUsers(models.Model):
    uid=models.TextField(unique=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    phone=models.CharField(unique=True,null=True,blank=True,max_length=12)
    name=models.CharField(max_length=24)
    password=models.CharField(max_length=100)
    account_level = models.CharField( 
        max_length = 20, 
        choices = account_levels, 
        default = '1'
        ) 
    access_level=models.CharField( 
        max_length = 20, 
        choices = access_levels, 
        default = '1'
        ) 
    pfPhoto=models.CharField(max_length=256,default="https://www.pngall.com/wp-content/uploads/5/Profile-PNG-Free-Download.png")
    likedPosts=models.JSONField(default=list,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.phone and self.email:
            self.phone = None
        elif not self.email and self.phone:
            self.email = None
        else:
             return
        super().save(*args, **kwargs)
    def __str__(self) -> str:
        display:str=self.name
        return display
    def toJson(self) -> dict:
        return {"user":{"uid":self.uid,"displayName": self.name,"email":self.email,"pfPhoto":self.pfPhoto,'access_level':access_levels[int(self.access_level)-1][1],'account_level':account_levels[int(self.account_level)-1][1],"likedPosts":self.likedPosts}}

class Blog(models.Model):
    uid=models.TextField()
    pfPhoto=models.TextField(default="",blank=True,null=True)
    
    level= models.CharField( 
        max_length = 20, 
        choices = account_levels, 
        default = '1'
        )
    topic= models.CharField( 
        max_length = 20, 
        choices = topics, 
        default = '1'
        )
    name=models.TextField()
    refId=models.TextField()
    title=models.TextField(unique=True)
    content=models.TextField()
    status=models.CharField( 
        max_length = 20, 
        choices = status_levels, 
        default = '1'
        )
    date=models.DateTimeField()
    views=models.IntegerField(default=0)
    likes=models.IntegerField(default=0)
    comments=models.JSONField(default=list,null=True,blank=True)
    md=models.TextField()

    def __str__(self):
        return self.title
    def toJson(self):
        return {"uid":self.uid,"name":self.name,"title":self.title,"refId":self.refId,"date":self.date,"content":self.content,"likes":self.likes,"comments":self.comments,'status':status_levels[int(self.status)-1][1],'level':account_levels[int(self.level)-1][1],"pfPhoto":self.pfPhoto,'views':self.views,'topic':topics[int(self.topic)-1][1]}

class Comment(models.Model):
    cid=models.UUIDField(unique=True)
    uid=models.TextField()
    name=models.TextField()
    pfPhoto=models.TextField()
    date=models.DateTimeField()
    comment=models.TextField()
    refId=models.TextField()
    reports=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.name + " : " +self.comment
    def toJson(self):
        return {"cid": self.cid,"uid": self.uid, "name":  self.name,"pfPhoto":  self.pfPhoto,"date":str(self.date),"comment":self.comment,"refId":self.refId}
