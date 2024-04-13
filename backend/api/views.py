from django.http import HttpResponse,HttpRequest,JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.utils import IntegrityError
import datetime
from .m2h import m2h
from django.utils.crypto import salted_hmac
from django.contrib.auth.hashers import make_password,check_password
import json,uuid
from .validate import parseLoginUser
from .models import EUsers,Blog,Comment


@csrf_exempt
def setUserBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                user=data.get('user') 
                euser=EUsers.objects.filter(email=user.get("email"))
                if(len(euser)!=1):
                    raise ValueError("No EUsers Found")
                title=data.get('title')
                content=data.get('content')
                status=data.get('status')
                md=content

                content=m2h(content)
                date=datetime.datetime.now()
                BlogData=Blog.objects.filter(title=title);
                if(len(BlogData)==1):
                    raise ValueError("Blog with same Title!!")
                
                refId=salted_hmac(settings.HASH_KEY,str(user.get('uid'))+title).hexdigest()
                email=user.get('email',None)
                if(not email):
                    email=user.get('providerData',[{}])[0].get('email')
                
                d=Blog(uid=user.get("uid"),title=title,name=user.get('displayName'),refId=refId,date=date,content=content,status=status,md=md,pfPhoto=euser[0].pfPhoto,level=euser[0].account_level)
                d.save()
                return JsonResponse({"error":False,"refId":refId,"status":status})
                
                
            except ValueError as e:
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def getBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                title=data.get('title')
                if(title):
                    BlogData=Blog.objects.filter(status="3",title=title)
                    if(len(BlogData)<1):
                        raise ValueError("No Blogs Found!!")
                    
                    
                    return JsonResponse({"response":BlogData.values()[0]})
                
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def getAllBlogs(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                keyword=data.get('title')
                if(keyword and keyword!='null'):
                    BlogData=Blog.objects.filter(status="3",title__icontains=keyword).order_by('-likes')
                    if(len(BlogData)<1):
                        raise ValueError("No Blogs Found!!")
                    
                    
                    return JsonResponse({"response":list(BlogData.values())})
                else:
                    BlogData=Blog.objects.filter(status="3").order_by('-likes')
                    
                    return JsonResponse({"response":list(BlogData.values())})
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def addGoogle(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
            try:
                guser=data.get('guser')
                uid=guser.get('uid')
                user=EUsers.objects.filter(uid=uid)
                if(len(user)>0):
                    return JsonResponse(user[0].toJson())
                
                passHash=make_password(guser.get('uid')+guser.get("email"))
                user=EUsers(uid=guser.get('uid'),email=guser.get("email"),name=guser.get("displayName"),password=passHash,pfPhoto=guser.get('photoURL'),access_level="2")
                user.save()
            except IntegrityError as e:
                return(JsonResponse({"Error":True,"message":str(e)}))
            except ValueError as e:
                
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse(user.toJson())
        else:
            return JsonResponse({"Error":True,"message":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def getUserBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                user=EUsers.objects.filter(email=data.get("email"))
                if(len(user)!=1):
                    raise ValueError("No EUsers Found")
                title=data.get('title')
                
                if(title!="null"):
                    BlogData=Blog.objects.filter(uid=user[0].uid,title=title);
                else:
                    BlogData=Blog.objects.filter(uid=user[0].uid);
                
                if(len(BlogData)<1):
                    res=None
                else:
                    res=[]
                    for i in BlogData:
                        res.append(i.toJson())
                    
                return JsonResponse({"response":res})
                
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def register(request:HttpRequest):
    
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                passHash=make_password(data.get("password"))
                uid=str(uuid.uuid5(uuid.NAMESPACE_DNS,data.get('name')+str(datetime.datetime.now(datetime.UTC))+passHash))
                phone=data.get("phone")
                user=EUsers(uid=uid,email=data.get("email"),phone=phone,name=data.get("name"),password=passHash)
                user.save()
            except IntegrityError as e:
                return(JsonResponse({"Error":True,"message":str(e)}))
            except ValueError as e:
                
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse(user.toJson())
        else:
            return JsonResponse({"Error":True,"message":"Invalid Token"})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def login(request:HttpRequest): 
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
            if(not parseLoginUser(data)):
                return JsonResponse({"Error":True,"message":"Invalid Data"})
            try:
                phone=data.get("phone")
                email=data.get("email")
                
                if(phone):
                    
                    user=EUsers.objects.filter(phone=phone)
                else:
                    user=EUsers.objects.filter(email=email)
                if(len(user)!=1):
                    raise ValueError("No EUsers Found")
                user=user[0]
                passHash=user.password
                if(not check_password(data.get("password"),passHash)):
                    raise ValueError("Invalid Password!!")
                
            except ValueError as e:
                
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse(user.toJson())
        else:
            return JsonResponse({"Error":True,"message":"Invalid Token"})
    else:
        return HttpResponse("Invalid Method")
  
def index(request:HttpRequest):
    if(request.method=="POST"):
        return HttpResponse("Hello World")
    
@csrf_exempt
def updateLikes(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get('api-token')=='random'):
            data:dict=json.loads(request.body.decode())
            try:
                user=data.get("user")
                dbUser=EUsers.objects.filter(uid=user.get('uid'))
                refId=data.get('refId')
                if(len(dbUser)):
                    if(len(dbUser.filter(likedPosts__icontains=refId))):
                        post=Blog.objects.filter(refId=refId)
                        if(post):
                            post=post[0]
                            if(post.likes>0):
                                post.likes-=1
                            post.save()
                            dbUser[0].likedPosts.remove(refId)
                            dbUser[0].save()
                    else:
                        post=Blog.objects.filter(refId=refId)
                        if(post):
                            post=post[0]
                            post.likes+=1
                            post.save()
                            dbUser[0].likedPosts.append(refId)
                            print(dbUser[0].likedPosts)
                            dbUser[0].save()
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].toJson())
            except Exception as e:
                print(e)
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def addComment(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get('api-token')=='random'):
            data:dict=json.loads(request.body.decode())
            try:
                user=data.get("user")
                dbUser=EUsers.objects.filter(uid=user.get('uid'))
                comment=data.get('comment')
                title=data.get('title')
                if(len(dbUser)):
                    
                    post=Blog.objects.filter(title=title)
                    if(post):
                        c=Comment.objects.filter(refId=post[0].refId,uid=dbUser[0].uid)
                        if(len(c)>=10):
                            raise ValueError("Maximum Comment Limit Reached")
                        post=post[0]
                        commentData=Comment(uid=dbUser[0].uid,name=dbUser[0].name,pfPhoto=dbUser[0].pfPhoto,comment=comment,refId=post.refId)
                        commentData.save()
                        post.comments.append(commentData.toJson())
                        post.save()
                    
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].toJson())
            except Exception as e:
                print(e)
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def getUserDraft(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                u=data.get("user")

                user=EUsers.objects.filter(email=u.get('email'))
                if(len(user)!=1):
                    raise ValueError("No EUsers Found")
                title=data.get('title')
                if(title!="null"):
                    BlogData=Blog.objects.filter(uid=user[0].uid,title=title);
                    if(len(BlogData)<1):
                        res=None
                    else:
                        res=BlogData[0].md
                else:
                    raise ValueError("No Blog Given!!")
                
                
                    
                return JsonResponse({"response":res})
                
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def editUserBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                user=data.get('user') 
                euser=EUsers.objects.filter(email=user.get("email"))
                if(len(euser)!=1):
                    raise ValueError("No EUsers Found")
                md=data.get('md')
                refId=data.get('refId')
                content=m2h(md)
                date=datetime.datetime.now()
                BlogData=Blog.objects.filter(uid=euser[0].uid,refId=refId);
                if(len(BlogData)<1):
                    raise ValueError("No Blog with same Title!!")
                BlogData[0].md=md
                BlogData[0].date=date
                BlogData[0].content=content
                BlogData[0].save()
                
                return JsonResponse({"error":False,"refId":refId})
                
                
            except ValueError as e:
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def publishUserBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                user=data.get('user') 
                euser=EUsers.objects.filter(email=user.get("email"))
                if(len(euser)!=1):
                    raise ValueError("No EUsers Found")
                refId=data.get('refId')
                if(euser[0].access_level=="3"):
                    bd=Blog.objects.filter(refId=refId);
                    if(len(bd)<1):
                        raise ValueError("No Blog with same Title!!")
                    bd[0].status="3"
                    print(bd[0].status)
                    bd[0].save()
                    return JsonResponse({"error":False,"refId":refId})
                else:
                    BlogData=Blog.objects.filter(uid=euser[0].uid,refId=refId);
                    if(len(BlogData)<1):
                        raise ValueError("No Blog with same Title!!")
                
                    BlogData[0].status="2"

                    BlogData[0].save()
                    
                return JsonResponse({"error":False,"refId":refId})
                
                
            except ValueError as e:
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def getForReviewBlog(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                u=data.get('user')
                user=EUsers.objects.filter(email=u.get('email'),uid=u.get('uid'))

                if(len(user)!=1 and user[0].access_level!="3"):
                    raise ValueError("No EUsers Found")
                title=data.get('title')
                
                if(title!="null"):
                    BlogData=Blog.objects.filter(status="2",title=title);
                else:
                    BlogData=Blog.objects.filter(status="2");
                
                if(len(BlogData)<1):
                    res=None
                else:
                    res=[]
                    for i in BlogData:
                        res.append(i.toJson())
                    
                return JsonResponse({"response":res})
                
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def removeComment(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get('api-token')=='random'):
            data:dict=json.loads(request.body.decode())
            try:
                cid=data.get("cid")
                dbUser=EUsers.objects.filter(uid=data.get('cuid'))
                if(len(dbUser)):
                    
                    cmnt=Comment.objects.filter(uid=dbUser[0].uid,cid=cid)
                    if(cmnt):
                        cmnt=cmnt[0]
                        post=Blog.objects.filter(refId=cmnt.refId)
                        it=[]
                        for v in post[0].comments:
                            if(str(v.get('cid'))==str(cmnt.cid)):
                                continue
                            it.append(v)
                        post=list(Blog.objects.filter(refId=cmnt.refId).all())

                        post[0].comments=it
                        post[0].save()
                        cmnt.delete()
                        

                        


                        return JsonResponse({"error":False})


                        
                    '''else:
                        post=Blog.objects.filter(refId=refId)
                        if(post):
                            post=post[0]
                            post.likes+=1
                            post.save()
                            dbUser[0].likedPosts.append(refId)
                            print(dbUser[0].likedPosts)
                            dbUser[0].save()'''
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].toJson())
            except Exception as e:
                print(e)
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()

