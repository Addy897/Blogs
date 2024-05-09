from django.db import models
from django.utils import timezone
import uuid

ACCOUNT_LEVELS = [("Premium 1","Premium1"),("Premium 2","Premium2"),("Premium 3","Premium3")]
TOPICS = [("Topic 1","Topic 1"),("Topic 2","Topic 2"),("Topic 3","Topic 3"),("Misc","Misc")]
ACCESS_LEVELS = (
    ("Read","Read"),
    ( "ReadWrite","ReadWrite"),
    ("Admin", "Admin"),
)
STATUS_LEVELS = [
    ("Draft", "Draft"),
    ("InReview", "InReview"),
    ("Published", "Published"),
]
TAGS = [
    ("All", "All"),
    ("Mens", "Mens"),
    ("Female", "Female"),
    ("LGBTQ", "LGBTQ"),
]

class EUsers(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(unique=True, null=True, blank=True, max_length=12)
    name = models.CharField(max_length=24)
    password = models.CharField(max_length=100)
    account_level = models.TextField(max_length=20, choices=ACCOUNT_LEVELS, default=ACCOUNT_LEVELS[0][0])
    access_level = models.TextField(max_length=20, choices=ACCESS_LEVELS, default=ACCESS_LEVELS[0][0])
    pf_photo = models.CharField(max_length=256, default="https://www.pngall.com/wp-content/uploads/5/Profile-PNG-Free-Download.png")
    likedPosts=models.JSONField(default=list,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.phone and self.email:
            self.phone = None
        elif not self.email and self.phone:
            self.email = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "uid": str(self.uid),
            "displayName": self.name,
            "email": self.email,
            "phone": self.phone,
            "pf_photo": self.pf_photo,
            'access_level': self.access_level,
            'account_level': self.account_level,
            "likedPosts":self.likedPosts,
        }

class Comment(models.Model):
    cid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(EUsers, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    reports = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.name}: {self.comment}"

    def to_json(self):
        return {
            "cid": str(self.cid),
            "uid": str(self.user.uid),
            "name": self.user.name,
            "pf_photo": self.user.pf_photo,
            "date": str(self.date),
            "comment": self.comment,
        }
   
class Blog(models.Model):
    ref_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(EUsers, on_delete=models.CASCADE, related_name='authored_blogs')
    cover_photo = models.TextField(default="https://flowbite.com/docs/images/blog/image-1.jpg")
    topic = models.TextField(max_length=20, choices=TOPICS, default=TOPICS[0][0])
    title = models.TextField(unique=True)
    tag = models.TextField(max_length=20, choices=TAGS, default=TAGS[0][0])
    description = models.TextField()  
    domain = models.CharField(max_length=64,blank=True,null=True)  
    status = models.TextField(max_length=20, choices=STATUS_LEVELS, default=STATUS_LEVELS[0][0])
    date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, related_name='blogs', blank=True)  # M2M relationship with Comment model
    delta = models.TextField()

    def __str__(self):
        return self.title

    def to_json(self):
        author_info = {
            "name": self.author.name,
            "pf_photo": self.author.pf_photo,
            "uid": str(self.author.uid),
            "account_level": self.author.account_level
        } if self.author else None

        # Serialize comments associated with this blog
        blog_comments = [comment.to_json() for comment in self.comments.all()]

        return {
            "ref_id": str(self.ref_id),
            "author": author_info,
            "cover_photo": self.cover_photo,
            "topic": self.topic,
            "title": self.title,
            "tag": self.tag,
            "delta": self.delta,
            "description": self.description,
            "domain": self.domain,
            "status": self.status,
            "date": str(self.date),
            "views": self.views,
            "likes": self.likes,
            "comments": blog_comments,
        }
    def delete(self, *args, **kwargs):
        for blog in self.comments.all():
            blog.remove(self)
        super().delete(*args, **kwargs)
