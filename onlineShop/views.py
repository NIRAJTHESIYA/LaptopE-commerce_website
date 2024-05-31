from django.shortcuts import render,redirect, HttpResponse
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.db.models import Q
from .models import *
import re 
from django.contrib import messages
from django.core.mail import send_mail
import random
from datetime import date,datetime



# Create your views here.

def isFirstThreeCharacterLetter(subUname):
    count = 0
    firstThreeCharacter = subUname[0:3]
    for i in range(0,len(firstThreeCharacter)):
        if((subUname[i] >= "A" and subUname[i] <= "Z") or (subUname[i] >= "a" and subUname[i] <= "z")):
            count += 1
        else:
            pass
        
    return count

def isStringContainsNumberorNot(userFullName):
    flag = 1
    for i in range(0,len(userFullName)):
        if((userFullName[i] >= "A" and userFullName[i] <= "Z") or (userFullName[i] >= "a" and userFullName[i] <= "z")):
            flag = 0
        elif(userFullName[i] == " "):
            flag = 0
        else:
            flag = 1
            break
        
    if(flag == 1):
        return True
    else:
        pass
    
def isContainsSpace(username, character):
    res = None
    for i in range(0, len(username)):
        if username[i] == character:
            res = i + 1
            break
        
    if res == None:
        pass
    else:
        return True


def userNameValidation(uName):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_name == uName):
            error_message = "Username already taken!"
            break

    return error_message

def userEmailValidation(uEmail):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_email == uEmail):
            error_message = "Email ID already taken!"
            break

    return error_message

def userMobileValidation(uMobile):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_mobile == uMobile):
            error_message = "Mobileno already taken!"
            break

    return error_message

def userImageValidation(puserImage):
    error_message = None
    userImage = str(puserImage)

    if(not(userImage.lower().endswith(('.png','.jpg','.jpeg')))):
        error_message = "Choose only image!"

    return error_message

def validationUserProfile(puserName,puserEmail,puserMobile,puserFullname,count):
    regxEmail = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regxMobile = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    mycharacter = " "

    if(not puserName):
        error_message = "Username is must!"
    elif(puserName):
        if (len(puserName) < 6 or len(puserName) > 15):
            error_message = "Username atleast 6 character long and maximum 15 character!"
        elif (isContainsSpace(puserName,mycharacter)):
            error_message = "Username does not contain space!"
        elif (count < 3):
            error_message = "First three character of username must be in letter!"
        elif (not puserEmail):
            error_message = "Email is required!"
        elif puserEmail:
            if(not(re.fullmatch(regxEmail,puserEmail))):
                error_message = "Invalid email!"
            elif(not puserFullname):
                pass
            elif puserFullname:
                if(isStringContainsNumberorNot(puserFullname)):
                    error_message = "First name not contains number or special character!"
                elif(not puserMobile):
                    error_message = "Mobile no required!"
                elif(puserMobile):
                    if(len(puserMobile) > 10):
                        error_message = "Enter valid mobile no!"
                    elif(not(re.fullmatch(regxMobile,puserMobile))):
                        error_message = "Enter valid mobile"
    
    return  


# valdation for sign_up(registration)
def validationSignup(userFullName,userName,userPassword,userConformPassword,userEmail,userPhoneNumber,user,count,myCharacter):
    regularex_email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regularex_phone = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    
    if(not userFullName):
        error_message = "Full name Required!"
    elif userFullName:
        if(isStringContainsNumberorNot(userFullName)):
            error_message = "Full name Not Contains Number."
        elif(not userName):
            error_message = "User name Required!"
        elif userName:
            isUserExixstorNot = user.isUsernameexists()
            if (len(userName) < 5 or len(userName) > 10):
                error_message = "User Name atleast 5 character long and Maximum 10 character!"
            elif (isContainsSpace(userName, myCharacter)):
                error_message = "User Name not contains Space"
            elif (count < 3):
                error_message = "User name first three character must be letter!"
            elif isUserExixstorNot:
                error_message = "User name is already taken!"
            elif (not userEmail):
                error_message = "E-mail is required!"
            elif userEmail:
                isemailexistotnot = user.isEmailexists()
                if isemailexistotnot:
                    error_message = " This E-mail ID is already taken"
                elif(not(re.fullmatch(regularex_email,userEmail))):
                    error_message = "Invalid E-mail"
                elif(not userPhoneNumber):
                    error_message = "Phone Number is required!"
                elif userPhoneNumber:
                    isphonenoexistornot = user.isphoneNumberexists()
                    if isphonenoexistornot:
                        error_message = "Mobile number is already taken"
                    elif(len(userPhoneNumber)>10):
                        error_message = "Enter valid Phone number"
                    elif(not(re.fullmatch(regularex_phone,userPhoneNumber))):
                        error_message = "Enter valid phone Number"
                    elif(not userPassword):
                        error_message = "Password is required!"
                    elif userPassword:
                        if (len(userPassword) < 5 or len(userPassword) > 10):
                            error_message = "User Password atleast 5 character long and Maximum 10 character!"
                        elif(userPassword != userConformPassword):
                            error_message = "Both Password is not match!"
                            
    return error_message  


# validation for sign_in(login)
def validationSignin(username,password,username1,password1):
    error_message = None
    if not username:
        error_message = "Please enter username!"
    elif username:
        if not password:
            error_message = "Please enter password!"
        elif(username != username1 or password != password1):
            error_message = "Invalid username or password!"
            
    return error_message

#validation for change password
def validationChangepassword(myuserpassword,Password, newpassword, samepassword):
    error_message = None
    if(not Password):
        error_message = 'Please Enter current passeword'
    elif Password:
        if(Password != myuserpassword):
            error_message = 'Your current password is invalid'
        elif(not newpassword):
            error_message = 'Please enter your new password'
        elif newpassword:
            if(len(newpassword) < 5 or len(newpassword) > 10):
                error_message = 'Your password atleast 5 character long and Maximum 10 character!'
            elif(newpassword != samepassword):
                error_message = 'Your new password and  new same password did not match'
                
    return error_message 

#validation for forgot password
def validationforgotpassword(email,myuseremail):
    error_massage = None
    if(not email):
        error_massage = "Please enter E-mail address"
    elif email:
        if(email != myuseremail):
            error_massage = "Please enter valid E-mail address"
            
    return error_massage

 
def index(request):
    b1 = Brand.objects.all()
    # a1 = Accesories.objects.all()
    randomeProduct = Product.objects.order_by('?')[:12]
    randomeProduct2 = Product.objects.order_by('?')[:3]
    storeData = Store.objects.all().first()
    param = {
        'brand1':b1,
        'randomeProduct':randomeProduct,
        'randomeProduct2':randomeProduct2,
        # 'accessories':a1,
        'storeData':storeData
    }
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        param = {
            'cuser':current_user,
            'brand1':b1,
            'randomeProduct':randomeProduct,
            'randomeProduct2':randomeProduct2,
            # 'accessories':a1,
            'storeData':storeData
        }
        return render(request,'home.html',param)
    
    return render(request,'home.html',param)

def sign_up(request):
    if request.method == 'POST':
        postData = request.POST
        userFullName = postData.get('fname')
        userName = postData.get('uname')
        userEmail = postData.get('email')
        userPhoneNumber = postData.get('pnumber')
        userPassword = postData.get('password')
        userConformPassword = postData.get('cpassword')
        myCharacter = " "
        try:
            firstArea = Area.objects.first()
        except:
            firstArea = None
        count = isFirstThreeCharacterLetter(userName)
        
        #validation
        
        error_message = None
        success_message = None
        
        # value dictionary
        
        value = {
            'ufullname': userFullName,
            'uname':userName,
            'uemail':userEmail,
            'uphone':userPhoneNumber
        }
        
        if(firstArea):
            user = User(user_fullname=userFullName,
                    user_name=userName,
                    user_password=userPassword,
                    user_email=userEmail,
                    user_mobile=userPhoneNumber,
                    is_admin=0,
                    store_idstore=Store.objects.get(idstore=1),
                    area_pincode=Area.objects.get(pincode=firstArea.pincode))
        else:
            user = User(user_fullname=userFullName,
                    user_name=userName,
                    user_password=userPassword,
                    user_email=userEmail,
                    user_mobile=userPhoneNumber,
                    is_admin=0,
                    store_idstore=Store.objects.get(idstore=1))
        
        error_message = validationSignup(userFullName,userName,userPassword,userConformPassword,userEmail,userPhoneNumber,user,count,myCharacter)
        
        
        if not error_message:
            success_message = "Registration is Done"
            data = {
                'success' : success_message
            }   
            user.register()
            request.session['user_name'] = userName
            return render(request,'home.html',data)
        
        else:
            data = {
                'error':error_message,
                'values':value
            }
            return render(request,'reg.html',data) 
           
    return render(request,'reg.html')

def sign_in(request):
    if request.method == 'POST':
        postData = request.POST
        username=postData.get('uname')
        password=postData.get('upassword')
        
        # validation
        
        error_message = None
        username1 = None
        password1 = None
        c1 = User.objects.all()
        
        for item in c1:
            if(username == item.user_name):
                password1 = item.user_password
                username1 = item.user_name
                
        # value dictionary
        
        value = {
            'uname':username
        }
        
        error_message = validationSignin(username,password,username1,password1)
        if not error_message:
            data = {
            }
            request.session['user_name'] = username
            return redirect('home')
        else:
            data = {
                'error':error_message,
                'values':value
            }
            return render(request,'login.html',data)
        
    return render(request,'login.html')

def c_password(request):
    if request.method =="POST":
        Password = request.POST.get('cpassword')
        newpassword = request.POST.get('npassword')
        samepassword = request.POST.get('cnpassword')
        
        #validation
        myuserpassword = None
        error_message = None
        success_message = None
        
        current_user = request.session['user_name']
        
        u1 = User.objects.all()
        
        for item in u1:
            if(item.user_name == current_user):
                myuserpassword = item.user_password
                break
        
        #value dictionary
        
        value = {
            'upassword':Password
        }
        error_message = validationChangepassword(myuserpassword,Password, newpassword, samepassword)
        
        if not error_message:
            success_message = 'Successfully password changed.!'
            data = {
                'success': success_message
            }
            User.objects.filter(user_name = current_user).update(user_password = newpassword)
            return render(request,'c_password.html',data)
        
        else:
            data ={
                'error':error_message,
                'values':value
            }
            
            return render(request,'c_password.html',data)
        
    return render(request,'c_password.html')

def f_password(request):
    if request.method == "POST":
        uEmail = request.POST.get('email')
    

        #validation
        myuseremail = None
        mypassword = None
        error_message = None
        success_message = None
    
        c1 = User.objects.all()

        for item in c1:
            if(item.user_email == uEmail):
                myuseremail = item.user_email
                mypassword = item.user_password
                break
    
        #value Dictionary
        value = {
        'email':uEmail
        }
        error_message = validationforgotpassword(uEmail,myuseremail)
    
        if not error_message:
            success_message = "Your password is sent to your email ID"
            subject = "Welcome to "
            mymessage = f"Hello User Your password is: {mypassword}, thank you for visiting our site"
            email_from = "njthesiya111@gmail.com"
            recipient_list = [myuseremail,]
            data = {
            'success' :success_message
            }
            send_mail(subject, mymessage ,email_from, recipient_list)
            return render(request, 'f_password.html',data)
    
        else:
            data = {
            'error': error_message,
            'values':value
            }
            return render(request, 'f_password.html',data)
    
    return render(request,'f_password.html')

def profile(request):
    u1 = User.objects.filter(user_name=request.session['user_name'])
    u3 = User.objects.get(user_name=request.session['user_name'])
    data = {
        'user1':u1
    }

    if request.method == "POST":
        puserName = request.POST.get('update_userName')
        puserEmail = request.POST.get('update_email')
        puserMobile = request.POST.get('update_mobile_no')
        puserFullName = request.POST.get('update_fName')
        error_message = None
        error_message1 = None
        success_message = None
        count = isFirstThreeCharacterLetter(puserName)

        error_message = validationUserProfile(puserName,puserEmail,puserMobile,puserFullName,count)

        if not error_message:
            success_message = "Profile updated successfully!"

            for i in u1:
                if(i.user_name != puserName):
                    error_message1 = userNameValidation(puserName)
                    break
                elif(i.user_email != puserEmail):
                    error_message1 = userEmailValidation(puserEmail)
                    break
                elif(i.user_mobile != puserMobile):
                    error_message1 = userMobileValidation(puserMobile)
                    break
                elif(len(request.FILES) != 0):
                    puserImage = request.FILES['update_image']
                    error_message1 = userImageValidation(puserImage)
                    break

            if not error_message1:
                u3.user_name = puserName
                u3.user_email = puserEmail
                u3.user_fullname = puserFullName
                u3.user_mobile = puserMobile
                if(len(request.FILES) != 0):
                    u3.user_image = request.FILES['update_image']
                
                u3.save()
                request.session['user_name'] = puserName
                u1 = User.objects.filter(user_name = request.session['user_name'])
                data = {
                    'user1':u1,
                    'success':success_message
                }

                return render(request,'profile.html',data)

            else:
                data = {
                    'user1':u1,
                    'error1':error_message1
                }
                return render(request,'profile.html',data)
        else:
            data = {
                'user1':u1,
                'error':error_message
            }

            return render(request,'profile.html',data) 

    return render(request,'profile.html',data)

def logout(request):
    try:
        del request.session['user_name']
    except:
        return redirect('home')
    return redirect('home')

class productPageListView(ListView):
    model = Product
    template_name = 'product.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = Brand.objects.get(idbrand=self.kwargs['brand_id'])
        if self.kwargs.get('brand_id'):
            object_list = Product.objects.filter(brand_brand_idbrand=getCategory.idbrand)
            if q:
                object_list = Product.objects.filter((Q(product_name__icontains=q) | Q(product_description__icontains=q) | Q(price__icontains=q)),brand_brand_idbrand=getCategory.idbrand)
            else:
                object_list = Product.objects.filter(brand_brand_idbrand=getCategory.idbrand)

        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["brand"] = Brand.objects.get(idbrand=self.kwargs['brand_id'])
        return context

def productview(request,pro_id):
    current_user = None
    b1 = Brand.objects.all()
    if 'user_name' in request.session:
        current_user = request.session['user_name']
    productview = Product.objects.get(idproduct=pro_id)
    data = {
        'productViewData':productview,
        'currentUser':current_user,
        'brand1':b1,
    }
    return render(request,'prodcutview.html',data)

# def accesoriesPage(request,accesories_id):
#     accProductPage = Accesories_Pro.objects.filter(accesories_accesories_idaccesories=accesories_id)
#     data = {
#         'accProductData':accProductPage,
#     }
#     return render(request,'accessoriesProduct.html',data)

# def accessoriesProductview(request,acc_id):
#     current_user = None
#     if 'user_name' in request.session:
#         current_user = request.session['user_name']
#     accessoriesProductview = Accesories_Pro.objects.get(idaccesories=int(acc_id))
#     data = {
#         'accproductViewData':accessoriesProductview,
#         'currentUser':current_user
#     }
#     return render(request,'accessoriesProductview.html',data) 

def addtocart(request):
    if request.method == 'POST':
        if 'user_name' in request.session:
           u1 = User.objects.get(user_name=request.session['user_name'])
           userId = u1.iduser
           prod_id = int(request.POST.get('product_id')) 
           product_check = Product.objects.get(idproduct=prod_id)
           if(product_check):
               if(cart.objects.filter(user=userId, product=prod_id)):
                   return JsonResponse({'data' : "Product Already in cart"})
               else:
                   prod_qty = int(request.POST.get('product_qty'))
                   userCart = cart.objects.create(user=User.objects.get(iduser=userId), product=Product.objects.get(idproduct=prod_id), product_qty=prod_qty)
                   userCart.save()
                   return JsonResponse({'status' : "Product added successfully"})
           else:
               return JsonResponse({'data' : "No such product found"})       
        else:
            return JsonResponse({'data': "Login to continue"})
    return redirect('home')

# def addtocart_accessory(request):
#     if request.method == 'POST':
#         if 'user_name' in request.session:
#            u1 = User.objects.get(user_name=request.session['user_name'])
#            userId = u1.iduser
#            acce_id = int(request.POST.get('accessory_id')) 
#            accessory_check = Accesories_Pro.objects.get(idaccesories=acce_id)
#            if(accessory_check):
#                if(cart.objects.filter(user=userId, accessories=acce_id)):
#                    return JsonResponse({'data' : "Accessory Already in cart"})
#                else:
#                    acce_qty = int(request.POST.get('accessory_qty'))
#                    userCart = cart.objects.create(
#                        user=User.objects.get(iduser=userId), 
#                        accessories=Accesories_Pro.objects.get(idaccesories=accessory_check.idaccesories), 
#                        accessories_qty=acce_qty
#                     )
#                    userCart.save()
#                    return JsonResponse({'status' : "Accessory added successfully"})
#            else:
#                return JsonResponse({'data' : "No such Accessory found"})       
#         else:
#             return JsonResponse({'data': "Login to continue"})
#     return redirect('home')

def viewcart(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    cart1 = cart.objects.filter(user=userId)
    b1 = Brand.objects.all()
    context = {'cart1':cart1,
               'brand1':b1,
               }
    return render(request,"cart.html",context)

def viewallproduct(request):
    allproduct= Product.objects.all()
    b1 = Brand.objects.all()
    data = {
        'allproduct' : allproduct,
        'brand1':b1,
    }
    return render(request,"alllaptop.html",data)

def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(cart.objects.filter(user=userId, product=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            usercart=cart.objects.get(product=prod_id,user=userId)
            usercart.product_qty = prod_qty
            usercart.save()
            return JsonResponse({'status':"Quantity update..."})
    return redirect('home')

def deletecartproduct(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(cart.objects.filter(user=userId, product=prod_id)):
            usercart=cart.objects.get(product=prod_id,user=userId)
            usercart.delete()
        return JsonResponse({'status':"Product Removed"})
    return redirect('home')

def viewwishlist(request):
    wishlist1 = User.objects.get(user_name=request.session['user_name'])
    userId = wishlist1.iduser
    wishlist1 = wishlist.objects.filter(user=userId)
    b1 = Brand.objects.all()
    context = {'wishlist1':wishlist1, 'brand1':b1,}
    return render(request,"wishlist.html",context)

def addtoWishlist(request):
    if request.method == 'POST':
        if 'user_name' in request.session:
           wishlist1 = User.objects.get(user_name=request.session['user_name'])
           userId = wishlist1.iduser
           prod_id = int(request.POST.get('product_id')) 
           product_check = Product.objects.get(idproduct=prod_id)
           if(product_check):
               if(wishlist.objects.filter(user=userId, product=prod_id)):
                   return JsonResponse({'data' : "Product Already in whishlist"})
               else:
                   userwishlist = wishlist.objects.create(user=User.objects.get(iduser=userId), product=Product.objects.get(idproduct=prod_id))
                   userwishlist.save()
                   return JsonResponse({'status' : "Product added to wishlist successfully"})
           else:
               return JsonResponse({'data' : "No such product found"})      
        else:
            return JsonResponse({'data': "Login to continue"})
    return redirect('home')

def deletewishlistproduct(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(wishlist.objects.filter(user=userId, product=prod_id)):
            userwishlist=wishlist.objects.get(product=prod_id,user=userId)
            userwishlist.delete()
        return JsonResponse({'status':"Product Removed"})
    return redirect('home')

def checkout1(request):
    user1 = User.objects.get(user_name=request.session['user_name'])
    city1 = City.objects.all()
    area1 = Area.objects.all()
    area2 = Area.objects.get(pincode=user1.area_pincode.pincode)
    deliverycharges = area2.delivery_charges
    userId = user1.iduser
    cartproduct = cart.objects.filter(user=userId)
    b1 = Brand.objects.all()
    # cartaccessory = cart.objects.filter(user=userId)
    grand_total = 0
    total_price = 0
    
    for Product in cartproduct:
        total_price = total_price + (Product.product.price * Product.product_qty)

    # for Accesories_Pro in cartproduct:
    #     total_price = total_price + (Accesories_Pro.accessories.price * Accesories_Pro.accessories_qty)

    grand_total = (total_price) 
    grand_total_inr = grand_total/80
    context = {'cartproduct':cartproduct,'total_price':total_price, 'city':city1, 'area':area1,'current_user':user1,'delArea':deliverycharges,'grandTotal':grand_total,'grand_total_inr':grand_total_inr, 'brand1':b1,}
    return render(request,'checkout.html',context)


def changecharges(request):
    if request.method == "POST":
        areaname = request.POST.get('areaname')
        a1 = Area.objects.get(area_name=areaname)
        return JsonResponse({'status':a1.delivery_charges})
    return redirect('home')

def placedorder(request):
    if request.method == "POST":
        user1 = User.objects.get(user_name=request.session['user_name'])
        userId = user1.iduser
        neworder = Order()
        neworder.user_iduser = User.objects.get(iduser=userId)
        neworder.orderfullname = request.POST.get('fname')
        neworder.orderemail = request.POST.get('email')
        neworder.ordermobile = request.POST.get('mobile')
        neworder.order_delivery_address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        a1 = Area.objects.get(area_name=request.POST['area1'])
        neworder.pincode = Area.objects.get(pincode=a1.pincode)
        neworder.order_payment_method = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cartproduct = cart.objects.filter(user=userId)
        # cartOfferproduct = cart.objects.filter(user=userId,offer_record=1)
        # total_offer_price = 0
        # for i in cartOfferproduct:
        #     total_offer_price = total_offer_price + i.product_qty.offer_price * i.item_qty
        cart_total_price = 0
        for item in cartproduct:
            cart_total_price = cart_total_price + (item.product.price * item.product_qty)
      
        neworder.total_amount = cart_total_price + a1.delivery_charges
        trackno = 'hariPriya'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'hariPriya'+str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno

        currentDateTime2 = datetime.now()
        neworder.created_at = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
        neworder.save()

        neworderitem = cart.objects.filter(user=userId)
        for item in neworderitem:
            OrderedItem.objects.create(
                order_idorder = neworder,
                productid = item.product,
                price = item.product.price,
                quantity = item.product_qty
            )

        cart.objects.filter(user=userId).delete()

        payMode = request.POST.get('payment_mode')
        if(payMode == "Paid by Razorpay" or payMode == "paid by paypal"):
            return JsonResponse({'status':"Your order has been placed successfully!"})
        else:
            messages.success(request,"Your order has been placed successfully!")
    
    return redirect('my_orders')

def myorder(request):
    user1 = User.objects.get(user_name=request.session['user_name'])
    userId = user1.iduser
    order = Order.objects.filter(user_iduser=userId)
    b1 = Brand.objects.all()
    context = {'order':order, 'brand1':b1,}
    return render(request,'myorder.html',context)

def vieworder(request, t_no):
    user1 = User.objects.get(user_name=request.session['user_name'])
    userId = user1.iduser
    order = Order.objects.filter(tracking_no=t_no).filter(user_iduser=userId).first()
    orderitems = OrderedItem.objects.filter(order_idorder=order)
    b1 = Brand.objects.all()
    context = {'order':order, 'orderitems':orderitems, 'brand1':b1,}
    return render(request,'userOrderDetails.html',context)

def aboutus_page(request):
    b1 = Brand.objects.all()
    data = {
        'brand1':b1,
    }
    return render(request, 'about_us.html', data)

def find_store(request):
    b1 = Brand.objects.all()
    data = {
        'brand1':b1,
    }
    return render(request, 'find.html', data)

def deletecartaccessory(request):
    if request.method == "POST":
        acce_id = int(request.POST.get('accessory_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(cart.objects.filter(user=userId, accessory=acce_id)):
            usercart=cart.objects.get(accesories=acce_id,user=userId)
            usercart.delete()
        return JsonResponse({'status':"Accessory Removed"})
    return redirect('home')


# def ProjectadminPanel(request):
#     # if 'admin' not in request.session:
#     #     messages.error(request,"Request denied!")
#     #     return redirect('home')
#     restrorant = Store.objects.first()
#     # u3 = User.objects.get(user_name=request.session['admin'])
#     totalAdmin = User.objects.filter(is_admin=1).count()
#     totalUser = User.objects.filter(is_admin=0).count()
#     totalItems = Product.objects.all().count()
#     totalOffer = Offer.objects.all().count()
#     data = {'restrorant':restrorant,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
#     return render(request,'adminPanel.html',data)