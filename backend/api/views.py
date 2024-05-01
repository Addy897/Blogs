
from django.http import HttpResponse,HttpRequest,JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.utils import IntegrityError
from .m2h import m2h
from django.utils.crypto import salted_hmac
from django.contrib.auth.hashers import make_password,check_password
import json,uuid
from .validate import parseLoginUser
from .models import EUsers,Blog,Comment
from django.utils import timezone


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
                description=data.get('description')
                content=data.get('content')
                cover=data.get('cover_photo')
                if(cover==None):
                    cover="https://flowbite.com/docs/images/blog/image-1.jpg"
                topic=data.get('topic')
                status=data.get('status')
                md=content

                content=m2h(content)
                BlogData=Blog.objects.filter(title=title);
                if(len(BlogData)==1):
                    raise ValueError("Blog with same Title!!")
                d=Blog(author=euser[0],title=title,description=description,content=content,status=status,md=md,topic=topic,cover_photo=cover)
                d.save()
                return JsonResponse({"error":False,"ref_id":d.ref_id,"status":status})
                
                
            except ValueError as e:
                print(e)
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
                    BlogData=Blog.objects.filter(status="Published",title=title)
                    if(len(BlogData)<1):
                        raise ValueError("No Blogs Found!!")
                    
                    
                    return JsonResponse({"response":BlogData[0].to_json()})
                
                
            except ValueError as e:
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
                    BlogData=Blog.objects.filter(status="Published",title__icontains=keyword)
                    if(len(BlogData)<1):
                        raise ValueError("No Blogs Found!!")
                    
                    
                    return JsonResponse({"response":[i.to_json() for i in BlogData.values()]})
                else:
                    BlogData=Blog.objects.filter(status="Published").order_by('-likes')
                    
                    return JsonResponse({"response":list(BlogData.values("title","description","cover_photo","date","likes","ref_id","views","topic"))})
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
        else:
            return JsonResponse({"error":True,"errorMessage":"Invalid Token"})
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
                    BlogData=Blog.objects.filter(author=user[0],title=title);
                    if(len(BlogData)>0):
                        return JsonResponse({"response":[i.to_json() for i in BlogData]})

                else:
                    BlogData=Blog.objects.filter(author=user[0]);
                    if(len(BlogData)>0):
                        return JsonResponse({"response":list(BlogData.values("title","description","cover_photo","date","likes","ref_id","views","status"))})
                return JsonResponse({"response":None})

            except ValueError as e:
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
                uid=uuid.uuid5(uuid.NAMESPACE_DNS,uid)

                user=EUsers.objects.filter(uid=uid)
                if(len(user)>0):
                    return JsonResponse(user[0].to_json())
                
                passHash=make_password(str(uid)+guser.get("email"))
                user=EUsers(uid=uid,email=guser.get("email"),name=guser.get("displayName"),password=passHash,pf_photo=guser.get('photoURL'),access_level="2")
                user.save()
            except IntegrityError as e:
                print(e)
                return(JsonResponse({"Error":True,"message":str(e)}))
            except ValueError as e:
                print(e)
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse({"user":user.to_json()})
        else:
            return JsonResponse({"Error":True,"message":"Invalid Token"})
    else:
        return HttpResponseNotFound()


@csrf_exempt
def register(request:HttpRequest):
    
    if(request.method=="POST"):
        if(request.headers.get("api-token")==settings.API_TOKEN):
            data:dict=json.loads(request.body.decode())
           
            try:
                passHash=make_password(data.get("password"))
                phone=data.get("phone")
                email=data.get("email")
                
                
                if (phone and email):
                    puser=EUsers.objects.filter(phone=phone)
                    euser=EUsers.objects.filter(email=email)
                    if(len(puser)>0 or len(euser)>0):
                        raise ValueError("User Already Exist")
                elif(phone):
                    
                    user=EUsers.objects.filter(phone=phone)
                    if(len(user)>0):
                        raise ValueError("User Already Exist")
                else:
                    user=EUsers.objects.filter(email=email)
                    if(len(user)>0):
                        raise ValueError("User Already Exist")
                

                user=EUsers(email=data.get("email"),phone=phone,name=data.get("name"),password=passHash)
                user.save()
            except IntegrityError as e:
                print(e)
                return(JsonResponse({"Error":True,"message":str(e)}))
            except ValueError as e:
                print(e)
                
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse(user.to_json())
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
                    raise ValueError("No User Found")
                user=user[0]
                passHash=user.password
                if(not check_password(data.get("password"),passHash)):
                    raise ValueError("Invalid Password!!")
                
            except ValueError as e:
                
                return(JsonResponse({"Error":True,"message":str(e)}))
            
            return JsonResponse(user.to_json())
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
                ref_id=data.get('ref_id')
                if(len(dbUser)):
                    if(len(dbUser.filter(likedPosts__icontains=ref_id))):
                        post=Blog.objects.filter(ref_id=ref_id)
                        if(post):
                            post=post[0]
                            if(post.likes>0):
                                post.likes-=1
                            post.save()
                            dbUser[0].likedPosts.remove(ref_id)
                            dbUser[0].save()
                    else:
                        post=Blog.objects.filter(ref_id=ref_id)
                        if(post):
                            post=post[0]
                            post.likes+=1
                            post.save()
                            dbUser[0].likedPosts.append(ref_id)
                            dbUser[0].save()
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].to_json())
            except Exception as e:
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def incView(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get('api-token')=='random'):
            data:dict=json.loads(request.body.decode())
            try:
                
                ref_id=data.get('ref_id')
                if(ref_id):
                        post=Blog.objects.filter(title=ref_id)
                        if(post):
                            post=post[0]
                            post.views+=1
                            post.save()
                        else:
                            raise ValueError("No Post Found!!")

                else:
                    raise ValueError("No Post Found!!")
                return JsonResponse({"error":False})
            except Exception as e:
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()

@csrf_exempt
def saveProfile(request:HttpRequest):
    if(request.method=="POST"):
        if(request.headers.get('api-token')=='random'):
            data:dict=json.loads(request.body.decode())
            try:
                user=data.get("user")
                dbUser=EUsers.objects.filter(uid=user.get('uid'))
                name=data.get('name')
                file=data.get('file')
                if(len(dbUser)):
                    
                    dbUser[0].name=name
                    if(file!=None):
                        dbUser[0].pf_photo=file
                    dbUser[0].save()
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].to_json())
            except Exception as e:
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
                        c=post[0].comments.filter(user=dbUser[0])
                        if(len(c)>=10):
                            raise ValueError("Maximum Comment Limit Reached")
                        post=post[0]
                        commentData=Comment(user=dbUser[0],comment=comment)
                        commentData.save()
                        post.comments.add(commentData)
                        post.save()
                    
                    
                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].to_json())
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
                    BlogData=Blog.objects.filter(author=user[0],title=title);
                    if(len(BlogData)<1):
                        raise ValueError("No Blog Given!!")
                    else:
                        res=BlogData[0].md
                else:
                    raise ValueError("No Blog Given!!")
                
                
                    
                return JsonResponse({"response":res})
                
                
            except ValueError as e:
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
                ref_id=data.get('ref_id')
                content=m2h(md)
                date=timezone.now()
                BlogData=Blog.objects.filter(author=euser[0],ref_id=ref_id);
                if(len(BlogData)<1):
                    raise ValueError("No Blog with Title!!")
                BlogData[0].md=md
                BlogData[0].date=date
                BlogData[0].content=content
                BlogData[0].save()
                
                return JsonResponse({"error":False,"ref_id":ref_id})
                
                
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
                ref_id=data.get('ref_id')
                if(euser[0].access_level=="Admin"):
                    bd=Blog.objects.filter(ref_id=ref_id);
                    if(len(bd)<1):
                        raise ValueError("No Blog with same Title!!")
                    bd[0].status="Published"
                    bd[0].save()
                    return JsonResponse({"error":False,"ref_id":ref_id})
                else:
                    BlogData=Blog.objects.filter(author=euser,ref_id=ref_id);
                    if(len(BlogData)<1):
                        raise ValueError("No Blog with same Title!!")
                
                    BlogData[0].status="InReview"

                    BlogData[0].save()
                    
                return JsonResponse({"error":False,"ref_id":ref_id})
                
                
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
                user=EUsers.objects.filter(uid=u.get('uid'))

                if(len(user)!=1 and user[0].access_level!="Admin"):
                    print(user[0])
                    raise ValueError("No EUsers Found")
                title=data.get('title')
                
                if(title!="null"):
                    BlogData=Blog.objects.filter(status="InReview",title=title)
                    if(len(BlogData)>0):
                        return JsonResponse({"response":BlogData[0].to_json()})
                    else:
                        raise ValueError("No Blog Found")
                   
                else:
                    BlogData=Blog.objects.filter(status="InReview");
                    if(len(BlogData)>0):
                        return JsonResponse({"response":list(BlogData.values("title","description","cover_photo","date","likes","ref_id","views","status"))})
                    else:
                        raise ValueError("No Blog Found")
                
               
                    
                
                
            except ValueError as e:
                print(e)
                return(JsonResponse({"error":True,"errorMessage":str(e)}))
            except Exception as e:
                print(f"\n\nError: {str(e)} \n\n")
            
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
                    
                    cmnt=Comment.objects.filter(user=dbUser[0],cid=cid)
                    if(cmnt):
                        cmnt=cmnt[0]
                        cmnt.delete()
                        return JsonResponse({"error":False})

                else:
                    raise ValueError("No Users Found!!")
                return JsonResponse(dbUser[0].to_json())
            except Exception as e:
                print(e)
                return JsonResponse({"error":True,"errorMessage":str(e)})
    else:
        return HttpResponseNotFound()

