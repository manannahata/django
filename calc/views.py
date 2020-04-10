from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import feedback_entry
import pickle
import io
import base64
import numpy as np
from cv2 import cv2
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img








def viewfb(request):
    userid2=request.POST["userid2"]
    all_feedback=feedback_entry.objects.filter(userid=userid2)
    return render(request,'fb.html',{'feedb':all_feedback})



def uploadfeedback(request):
    name=request.POST["user"]
    feedback=request.POST["feedback"]
    userid=request.POST["userid"]

    feed=feedback_entry(name=name,feedback=feedback,userid=userid)
    feed.save()
    messages.info(request,"THANK YOU FOR YOUR RESPONSE")
    return render(request,'home.html')

def logout(request):
    auth.logout(request)
    return redirect('/')  

def home(request):
    return render(request,'home.html')

def logi(request):
    if request.method=='POST':
        username=request.POST['user']
        password=request.POST['pass']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.info(request,username)
            return render(request,'home.html')
        else:
            messages.info(request,'invalid credential')
            return redirect('logi')
    

    else:
        return render(request,'logi.html')

def sign(request):
    return render(request,'sign.html')


def main1(request):
    first_name=request.POST['fname']
    last_name=request.POST['lname']
    email=request.POST['email']
    username=request.POST['user']
    phone=request.POST['phone']
    password=request.POST['pass']
    
    if User.objects.filter(username=username).exists():
        messages.info(request,'USERNAME ALREADY EXISTS')
        print('user taken')
        return redirect('sign')
    elif User.objects.filter(email=email).exists():
        messages.info(request,'EMAIL ALREADY EXISTS')
        print('email taken')
        return redirect('sign')

    else:
        user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,phone=phone)
        user.save()
        return render(request,'logi.html')

        
# load the image


default_image_size = tuple((256, 256))

def convert_image(image_data):
    try:
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        if image is not None :
            image = image.resize(default_image_size, Image.ANTIALIAS)   
            image_array = img_to_array(image)
            return np.expand_dims(image_array, axis=0), None
        else :
            return None, "Error loading image file"
    except Exception as e:
        return None, str(e)

# Create your views here.
def uploadimage(request):    
    p = request.FILES['image']
    from .models import User
    user=User(pic=p)
    user.save()
    try:
        if request.method == "GET" :
            messages.info(request,'built')
            
        else:
            #image = cv2.resize(load_img('00f2e69a-1e56-412d-8a79-fdce794a17e4___JR_B.Spot 3132.jpg'), default_image_size)  
            image_array = img_to_array(load_img('00f2e69a-1e56-412d-8a79-fdce794a17e4___JR_B.Spot 3132.jpg'))
            image_array= np.expand_dims(image_array, axis=0)
            model_file = f"cnn_model.pkl"
            saved_classifier_model = pickle.load(open(model_file,'rb'))
            prediction = saved_classifier_model.predict(image_array) 
            label_binarizer = pickle.load(open(f"label_transform.pkl",'rb'))
            messages.info(request,f"{label_binarizer.inverse_transform(prediction)[0]}")
          
             #messages.info(request,"try other way")
            
            #if request.body:
                #request_data = 
                #image_data = user.save()#request_data#.sdplit(';base64,')
                #image_array, err_msg = convert_image(image_data)
               
               # if err_msg == None :
                    
               # else :     
                    #messages.info(request,f"Error1 : {err_msg}")

           # else :
                #messages.info(request,'request body is empty')

    except Exception as e:
        messages.info(request,f"Error : {str(e)}")
    return render(request,'home.html')

