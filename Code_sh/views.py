import requests
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Problems,Solved
from django.core.paginator import Paginator
from django.db.models import Sum,Count
import random
#from django.views.decorators.csrf import csrf_exempt

#Sending  to Login page

Request_url ="https://ide.geeksforgeeks.org/main.php"
Result_url = "https://ide.geeksforgeeks.org/submissionResult.php"

def Home(request):
    return render(request,'Code_sh/Home.html')

def Login(request):
    return render(request,'Code_sh/Login.html')

#Sending to Registration page

def Register(request):
    return render(request,'Code_sh/register.html')

#Handeling Login Request

def Login_user(request): 
    Questions = Problems.objects.all();
    
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           
           
           auth.login(request, user)
           return render(request,'Code_sh/Home.html',{'Questions': Questions}) 
       else:
            
           return render(request,'Code_sh/Login.html',{'msg':'Please Retry '}) 
       
#Logout the user

def Logout(request):
    
    auth.logout(request)
    return render(request,'Code_sh/Home.html') 
        

#Handeling Registration Request

def Register_user(request):
    
   
    if request.method == 'POST':
        First_name = request.POST['first_name']
        Last_name  = request.POST['last_name']
        Username   = request.POST['username']
        Email      = request.POST['email']
        Password   = request.POST['password']
        CPassword  = request.POST['confirm_password']
        
        if Password==CPassword:
            if User.objects.filter(email=Email).exists():
     
                return render(request,'Code_sh/register.html',{'msg':'Email Already Exist'})
            
            elif User.objects.filter(username=Username).exists():
          
                return render(request,'Code_sh/register.html',{'msg':'username Already Exist'}) 
            
            else :
                
                user = User.objects.create_user(username=Username,password=Password,email=Email,first_name=First_name,last_name=Last_name)
                
                user.save();
               
                return render(request,'Code_sh/Login.html',{'msg2':'Welcome '+ First_name + "Please sign-in"})
        else:
             
              
             return render(request,'Code_sh/register.html',{'msg':'Please Re-enter Password'})
        
    else:
        
        return  redirect('/')

#Sending to Contribute page

def Contribution(request):
    return render(request,'Code_sh/Contribute.html')

#Handeling Contribution Request

def Review_Contribution(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        description=request.POST['Description']
        language=request.POST['language']
        Input=request.POST['input']
        output=request.POST['output']
        tag=request.POST['tag']
        #p=code.split('\n')
        Result = Judge(code, language, Input,output)
        if Result == 1:
            
            if Problems.objects.filter(Problem_Name = name).exists():
                
                return render(request,'Code_sh/Contribute.html',{'msg':'Please change problem name ...try with language name  '})
            else:
                
                Filterd = Preprocessing(code)
                
                description = description +'\n'+'input : ' + Input +'\n\n' +'Output : '+output + '\n'
                
                problem = Problems(Problem_Name = name,Problem_Description=description,Problem = Filterd[0] ,
                                   Language=language,Problem_Tags=tag,Problem_level=Filterd[1],Problem_Setter=request.user.username)
                problem.save()
                return render(request,'Code_sh/Contribute.html',{'msg':'Your code is under Evaluation!! till then happy coding'})
        
        elif Result == 0:
            return render(request,'Code_sh/Contribute.html',{'msg':'Given output is differs from compilers output'})
        else:
            return render(request,'Code_sh/Contribute.html',{'msg1':Result})
    else:
        return  redirect('/')

#Judging the contribution

def Judge(code,language,Input,output):
    
    data={'lang':language,
              'code':code,
              'input':Input,
              'save':False
              }
    r = requests.post(Request_url,data)

    p=r.json()
    data = {'sid': p['sid'],
            'requestType':'fetchResults'
            }

    status='IN-QUEUE'
    
    while status =='IN-QUEUE':
        r = requests.post(Result_url,data)
        p=r.json()
        status = p['status'] 
        
    print(r.json())  
    Garbage=['valid','compResult','memory','time','id','hash','status']
    for key in Garbage:
        if key in p.keys():
            del p[key]
        
    if 'output' in p.keys():
        result=''
        uresult=''
        
        for i in (p['output']):
            if i.isalnum():
                result+=i
        
        for i in output:
            if i.isalnum():
                uresult+=i 
        
        return result==uresult 
    else:
        error='Please fix this issues \n'
        for key in p.keys():
            error += p[key]
            error +="\n"
        return error   
               
#To Filter code

def Preprocessing(code):
    lis = code.split('\n')
    code=''
    count=0
    for i in lis:
        i=i.strip()
        if(len(i)):
            count += 1
            code += i
            code +='\n'
    level='Easy'       
    if count > 10 and count < 30:
        level = "Medium"
    elif count >=30:
        level = "Hard"
    else:
        level = "Easy"
    return (code ,level)     
#problems Page
def Questions(request):
     Questions = Problems.objects.all()
     Ans=Solved.objects.filter(user_name = request.user.username).aggregate(total = Sum('Number'),que = Count('user_name'))
     cont = Problems.objects.filter(Problem_Setter = request.user.username).aggregate(con = Count('Problem_Setter'))
     paginator = Paginator(Questions, 8)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     
     return render(request,'Code_sh/Question.html',{'Questions':page_obj,'User':request.user.username,'Total':Ans['total'],'Que':Ans['que'],'Contribute':cont['con']})
def Editor(request,problem=""):
    Question = Problems.objects.filter(Problem_Name = problem).first()
    code =  Question.Problem
    lis =code.split('\n') 

    
    
    x=len(lis)
    Shuffle=[]
    
    for i in range(x):
        y = random.choice(lis)
        Shuffle.append(y)
        lis.remove(y)

    
    return render(request,'Code_sh/Editor.html',{'Questions':Question,'code':Shuffle})

def User_Request(request):
   
    
    if request.method == 'POST':
        user_code = request.POST['Input']
        problem = request.POST['problem'] 
        Questions = Problems.objects.filter(Problem_Name=problem).first()
        code =  Questions.Problem
        user_code=user_code.replace("&lt;", "<") 
        user_code=user_code.replace("&gt;", ">")    
        user_code=user_code.replace("&amp;", "&") 
        lis =code.split('\n')
        z = user_code.split('$/$')
       
        y=''
        u=''
        for i in lis:
            x = i.rstrip()
            y += x
        for i in z:
            if len(i):
                x = i.strip()
                u += x    
           
         
        if u==y:
            print(u==y)
            if not(Solved.objects.filter(Problem = problem, user_name = request.user.username).exists()):
                
                Questions.Total_Accepted += 1
                
                if Questions.Problem_level =='Medium':
                    m = 30
                elif Questions.Problem_level =='Easy':
                    m = 10
                else:
                    m = 50
                solve = Solved(user_name =request.user.username,Problem=problem,Number=m )
                solve.save()
                Questions.save()
            return render(request,'Code_sh/Editor.html',{'Questions':Questions,'code':lis,'Msg':'Accepted !!!!'})
        else:
            print(u,y)
            Questions.Total_submission += 1
            Questions.save()
            return render(request,'Code_sh/Editor.html',{'Questions':Questions,'code':z,'Msg':'Please Check your Code'})
    return render(request,'Code_sh/Editor.html')
   