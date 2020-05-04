from django.shortcuts import render,redirect
from .models import User,Phone,Review,Cart
from django.core.mail import send_mail
import random
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import *
import stripe
from django.utils import timezone
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def index(request):
	finalPrice=0
	if request.method=="POST":
		finalPrice=request.POST['finalPrice']
		charge = stripe.Charge.create(amount=finalPrice,currency='inr',description='Product Charge',source=request.POST['stripeToken'])
		success=request.POST['success']
		user=User.objects.get(pk=request.session['userpk'])
		carts=Cart.objects.filter(user=user)
		for i in carts:
			print(i)
			i.status="inactive"
			i.buy_date=timezone.now()
			i.save()
		carts=Cart.objects.filter(user=user,status="active")
		finalPrice=0
		request.session['carts']=len(carts)
		for i in carts:
			finalPrice+=int(i.phone.price)
		return render(request,'myapp/mycart.html',{'carts':carts,'finalPrice':finalPrice,'success':success})
	else:
		return render(request,'myapp/index.html')

def iphone(request):
	iphones=Phone.objects.filter(brand="iPhone")
	return render(request,'myapp/iphone.html',{'iphones':iphones})

def redmi(request):
	redmi=Phone.objects.filter(brand="Redmi")
	return render(request,'myapp/redmi.html',{'redmi':redmi})

def samsung(request):
	samsung=Phone.objects.filter(brand="Samsung")
	return render(request,'myapp/samsung.html',{'samsung':samsung})

def sale(request):
	phone_sale=Phone.objects.filter(sale=True)
	for i in phone_sale:
		if i.sale==True:
			i.final_price=(int(i.price)-(int(i.price)*int(i.sale_price))/100)
			i.save()
	phone_sale=Phone.objects.filter(sale=True)
	return render(request,'myapp/sale.html',{'phone_sale':phone_sale})

def signup(request):
	return render(request,'myapp/signup.html')

def login(request):
	return render(request,'myapp/login.html')

def signup_user(request):
	fname=request.POST['fname']
	lname=request.POST['lname']
	email=request.POST['email']
	mobile=request.POST['mobile']
	address=request.POST['address']
	password=request.POST['password']
	cpassword=request.POST['cpassword']
	image=request.FILES['image']

	user=User.objects.filter(email=email)
	if user:
		error="Email Already Exist"
		return render(request,'myapp/signup.html',{'error':error})
	elif password==cpassword:
		print("Password & Confirm Password Matched")
		User.objects.create(fname=fname,lname=lname,email=email,mobile=mobile,address=address,password=password,cpassword=cpassword,image=image)
		rec=[email,]
		subject="OTP For Successfull Registration"
		otp=random.randint(1000,9999)
		message="Your OTP For Registration Is "+str(otp)
		email_from = settings.EMAIL_HOST_USER
		send_mail(subject, message, email_from, rec)
		task="signup"
		return render(request,'myapp/verify_otp.html',{'otp':otp,'email':email,'task':task})
	else:
		print("Password & Confirm Password Does Not Matched")
		return render(request,'myapp/signup.html')
def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']
	task=request.POST['task']

	if otp==uotp:
		if task=="signup":
			user=User.objects.get(email=email)
			user.status="active"
			user.save()
			return render(request,'myapp/login.html')
		elif task=="forgot":
			return render(request,'myapp/forgot_password.html',{'email':email})
	else:
		error="Entered OTP Is InCorrect Please Try Again."
		return render(request,'myapp/verify_otp.html',{'otp':otp,'email':email,'error':error})
def login_user(request):
	email=request.POST['email']
	password=request.POST['password']

	try:
		user=User.objects.get(email=email,password=password,status="active")
		if user:
			carts=Cart.objects.filter(user=user,status="active")
			print("Total Data In Carts : ",carts.count)
			request.session['fname']=user.fname
			request.session['lname']=user.lname
			request.session['userpk']=user.pk
			request.session['image']=user.image.url
			request.session['carts']=len(carts)
			return render(request,'myapp/index.html',{'user':user})
	except:
		error="Your Email Or Password Is Incorrect Or Status Is Inactive"
		return render(request,'myapp/login.html',{'error':error})
def logout(request):
	try:
		del request.session['fname']
		del request.session['lname']
		del request.session['userpk']
		return render(request,'myapp/login.html')
	except:
		pass
def detail(request,pk):
	phone=Phone.objects.get(pk=pk)
	reviews=Review.objects.filter(phone=phone)
	return render(request,'myapp/detail.html',{'phone':phone,'reviews':reviews})

def feedback(request,pk1,pk2):
	user=User.objects.get(pk=pk1)
	phone=Phone.objects.get(pk=pk2)
	flag=True
	reviews=Review.objects.filter(phone=phone)
	carts=Cart.objects.filter(user=user,status="active")
	request.session['carts']=len(carts)
	return render(request,'myapp/detail.html',{'phone':phone,'user':user,'flag':flag,'reviews':reviews})

def submit_feedback(request,pk1,pk2):
	user=User.objects.get(pk=pk1)
	phone=Phone.objects.get(pk=pk2)
	feedback=request.POST['feedback']
	Review.objects.create(user=user,phone=phone,feedback=feedback)
	reviews=Review.objects.filter(phone=phone)
	carts=Cart.objects.filter(user=user,status="active")
	request.session['carts']=len(carts)
	return render(request,'myapp/detail.html',{'phone':phone,'reviews':reviews})

def add_to_cart(request,pk1,pk2):
	user=User.objects.get(pk=pk1)
	phone=Phone.objects.get(pk=pk2)
	Cart.objects.create(user=user,phone=phone)
	carts=Cart.objects.filter(user=user,status="active")
	request.session['carts']=len(carts)
	return redirect('mycart')

def mycart(request):
	finalPrice=0
	user=User.objects.get(pk=request.session['userpk'])
	carts=Cart.objects.filter(user=user,status="active")
	request.session['carts']=len(carts)
	for i in carts:
		finalPrice+=int(i.phone.price)
	
	return render(request,'myapp/mycart.html',{'carts':carts,'finalPrice':finalPrice})

def remove_cart(request,pk):
	
	cart=Cart.objects.get(pk=pk)
	cart.delete()
	user=User.objects.get(pk=request.session['userpk'])
	carts=Cart.objects.filter(user=user,status="active")
	request.session['carts']=len(carts)
	return redirect('mycart')

def forgot_password(request):
	return render(request,'myapp/enter_email.html')

def verify_email(request):
	email=request.POST['email']
	try:
		user=User.objects.get(email=email)
		rec=[email,]
		subject="OTP For Forgot Password"
		otp=random.randint(1000,9999)
		message="Your OTP For Forgot Password Is "+str(otp)
		email_from = settings.EMAIL_HOST_USER
		send_mail(subject, message, email_from, rec)
		task="forgot"
		return render(request,'myapp/verify_otp.html',{'otp':otp,'email':email,'task':task})
		
	except:
		error="This email id is not available with us."
		return render(request,'myapp/enter_email.html',{'error':error})

def update_password(request):
	email=request.POST['email']
	password=request.POST['password']
	cpassword=request.POST['cpassword']

	try:
		user=User.objects.get(email=email)
		user.password=password
		user.cpassword=cpassword
		user.save()
		return render(request,'myapp/login.html')
	except:
		pass
def payment(request):
    finalPrice=request.POST['finalPrice']
    finalPrice1=int(finalPrice)*100
    key=settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'myapp/payment.html',{'finalPrice':finalPrice,'finalPrice1':finalPrice1,'key':key})

def myorder(request):
	user=User.objects.get(pk=request.session['userpk'])
	carts=Cart.objects.filter(user=user,status="inactive")
	return render(request,'myapp/myorder.html',{'carts':carts})