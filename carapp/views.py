from django.shortcuts import render,redirect,Http404,get_object_or_404,HttpResponse
from .import models
from . models import user_reg,Feedback,Add_areas,book,pay,Slotfeedback,recurring,icart,Transaction
import razorpay
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))




from smtplib import SMTPException




# Create your views here.
def index(request):
    return render(request,'index.html')
def ride(request):
    return render(request,'ride.html')
def solo(request):
    return render(request,'solo-ride.html')


      
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        
        # Use .first() to retrieve the first matching object or None
        cr = user_reg.objects.filter(email=email, password=password).first()
        
        if cr:  # Check if cr is not None
            userd = models.user_reg.objects.get(email=email, password=password)
            id = userd.id
            email = userd.email
            password = userd.password
            request.session['id'] = id
            request.session['email'] = email
            request.session['password'] = password

            if cr.status == 'approved': 
                # Set session and redirect to the index page 
                request.session['email'] = cr.email 
                return redirect('user_home') 
            else: 
                # If not approved, redirect back with a waiting message 
                return render(request, 'login.html', {'error': 'Your account is not yet approved. Please wait until the admin approves your registration.'}) 
        else:
            # Handle case where credentials are incorrect
            return render(request, 'login.html', {'error': 'Invalid email or password.'})

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user_reg

from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import logging

# Set up logging
logger = logging.getLogger(__name__)

def register_user(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        age = request.POST.get('age')
        image = request.FILES.get('image')

        # Check if the email already exists
        if user_reg.objects.filter(email=email).exists():
            alert = "<script>alert('User Already Exists!');window.location.href = '/register_user/';</script>"
            return HttpResponse(alert)

        # Validate that passwords match
        if password != confirm_password:
            alert = "<script>alert(' Exists!');window.location.href = '/register_user/';</script>"
            return HttpResponse(alert)

        # Create and save the user record
        user = user_reg(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            password=password,  # Remember to hash the password in production
            age=age, 
            image=image,
            status='applied'  # Ensure this matches your model definition
        )

        try:
            user.save()

            # Send the registration success email
            send_mail(
                subject='Registration Successful - Welcome!',
                message=(
                    f'Dear {user.first_name} {user.last_name},\n\n'
                    f'Thank you for registering! Your account has been created successfully.\n'
                    f'You can now log in using your email: {user.email}\n\n'
                    f'Best regards,\nYour Application Team'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],  # Send to the registered user's email
            )
            
            messages.success(request, 'Registration successful! You can now log in.')

            return redirect('login')  # Redirect to login page after successful registration

        except Exception as e:
            # Log the error for debugging
            logger.error(f"Failed to send registration email: {e}")
            # Display a message to the user if email fails
            messages.error(request, 'Registration successful, but we couldn\'t send you a confirmation email.')
            return redirect('login')  # Redirect to login page after registration

    return render(request, 'register_user.html')



def mytrans(request):
    email = request.session.get('email')
    user = pay.objects.filter(email=email)
    return render(request,'mytrans.html',{'user':user})


def userlist(request):
    user = user_reg.objects.all()
    return render(request,'userlist.html',{'user':user})

def delete_user(request, id):
    try:
        user = user_reg.objects.get(id=id)
        # Add your deletion logic here
        user.delete()
        return redirect('userlist')  # Redirect to a list of users or another page
    except user_reg.DoesNotExist:
        raise Http404("User not found")
    

def user_profile(request):
    # Fetch user email from session
    email = request.session.get('email')
    
    # Handle the case where the email is not found in session
    if not email:
        return render(request, 'user_profile.html', {'error': 'User not logged in'})
    
    # Fetch user information from the database
    cr = get_object_or_404(user_reg, email=email)
    
    # Prepare user information for rendering
    user_info = {
        'first_name': cr.first_name,
        'last_name': cr.last_name,
        'age': cr.age,
        'address': cr.address,
        'phone': cr.phone,
        'email': cr.email,
        'password': cr.password,
        'image': cr.image# Handle the case where image might be None
    }
    
    return render(request, 'user_profile.html', user_info)

def update_profile(request):
    email=request.session['email']
    cr =user_reg.objects.get(email=email)
    if cr:
        user_info = {
            'first_name':cr.first_name,
            'last_name':cr.last_name,
            'age':cr.age,
            'address':cr.address,
            'phone':cr.phone,
            'email':cr.email,
            'password':cr.password,
            'image':cr.image
        }
        return render(request,'update_profile.html',user_info)
    else:
        return render(request,'update_profile.html')
def proupdate(request):
    email = request.session.get('email')
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        new_email = request.POST.get('email')
        password = request.POST.get('password')
     
        image = request.FILES.get('image')  # Handle file upload

        # Fetch the user object using the session email
        user = user_reg.objects.get(email=email)

        # Check if passwords match
       

        # Update user information
        user.first_name = first_name
        user.last_name = last_name
        user.age = age
        user.address = address
        user.phone = phone
        user.email = new_email
        user.password = password
      

        # Update image if a new one is provided
        if image:
            user.image = image

        # Save the updated user object
        user.save()

        # Fetch the updated user object
        cr = user_reg.objects.get(email=new_email)

        # Prepare user info for rendering
        user_info = {
            'first_name':cr.first_name,
            'last_name':cr.last_name,
            'age':cr.age,
            'address':cr.address,
            'phone':cr.phone,
            'email':cr.email,
            'password':cr.password,
            'image':cr.image
        }
        return render(request,'update_profile.html',user_info)
    else:
        return render(request, 'update_profile.html')

def user_home(request):
    return render(request,'user_home.html')

def admin_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        a='admin@gmail.com'
        b='admin12'
        if email==a:
            if password==b:
                return render(request,'admin_home.html')
    return render(request,'admin_login.html')        

def admin_home(request):
    return render(request,'admin_home.html')

def feedback_rate(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            # Handle missing fields
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)

        # Create and save the Feedback instance
        feedback = Feedback(
            feedback_text=feedback_text,
            rating=rating
        )
        feedback.save()

        # Redirect to a success page
        return redirect('feedback_success')
    
    else:
        # Render the feedback form
        return render(request, 'feedback_rate.html')
    
def feedback_success(request):
    return render(request, 'feedback_success.html')

def feedbacklist(request):
    feed = Feedback.objects.all()
    return render(request,'feedbacklist.html',{'feed':feed})

def delete_feedback(request, id):
    try:
        feed = Feedback.objects.get(id=id)
        # Add your deletion logic here
        feed.delete()
        return redirect('feedbacklist')  # Redirect to a list of users or another page
    except Feedback.DoesNotExist:
        raise Http404("Feedback not found")

from django.shortcuts import render
from .models import Add_areas

def area(request):
    if request.method == 'POST':
        # Collect form data from POST request
        size = request.POST.get('size')
        
        availability = request.POST.get('availability')
        price = request.POST.get('price')
        location = request.POST.get('location')
        place = request.POST.get('place')
        space_type = request.POST.get('space_type')
        feature = request.POST.get('feature')
        operating_hours = request.POST.get('operating_hours')
        contact_information = request.POST.get('contact_information')
        image = request.FILES.get('image')
        space_name = request.POST.get('space_name')
        slot_quantity = request.POST.get('slot_quantity')
        rentperday = request.POST.get('rentperday')
        recurring = request.POST.get('recurring')

        print(f"Received data: size={size}, availability={availability}, price={price}, "
              f"location={location}, place={place}, space_type={space_type}, feature={feature}, "
              f"operating_hours={operating_hours}, contact_information={contact_information}, "
              f"image={image}, space_name={space_name}, "
              f"slot_quantity={slot_quantity}, rentperday={rentperday}")

        # Check if all required fields are provided
  
        try:

        # Create new Add_areas instance and save it to the database
            new_area = Add_areas(
                size=size,
                total_slot=slot_quantity,
                availability=availability,
                price=price,
                location=location,
                place=place,
                space_type=space_type,
                feature=feature,
                operating_hours=operating_hours,
                contact_information=contact_information,
                image=image,
                space_name=space_name,
                slot_quantity=slot_quantity,
                rentperday=rentperday,
                recurringquantity=recurring,

            )

            new_area.save()  # Save and generate QR code

            return render(request, 'admin_home.html', {'message': 'Area added successfully'})
        except Exception as e:
            print(e)

    else:
        return render(request, 'area.html')
    
def update_area(request,id):
    cr =Add_areas.objects.get(id=id)
    if cr:
        area_info = {
            'size':cr.size,
            'total_slot':cr.total_slot,
            'availability':cr.availability,
            'price':cr.price,
            'location':cr.location,
            'place':cr.place,
            'space_type':cr.space_type,
            'feature':cr.feature,
            'operating_hours':cr.operating_hours,
            'contact_information':cr.contact_information,
            'image':cr.image,
            
            'space_name':cr.space_name,
            'slot_quantity':cr.slot_quantity
        }
        return render(request,'update_area.html',area_info)
    else:
        return render(request,'update_area.html')

def editarea(request,id):
    cr = Add_areas.objects.get(id=id)
    if cr:
        area_info = {
            'size':cr.size,
            'total_slot':cr.total_slot,
            'availability':cr.availability,
            'price':cr.price,
            'location':cr.location,
            'place':cr.place,
            'space_type':cr.space_type,
            'feature':cr.feature,
            'operating_hours':cr.operating_hours,
            'contact_information':cr.contact_information,
            'image':cr.image,
            
            'space_name':cr.space_name,
            'slot_quantity':cr.slot_quantity
        }
        
    
    if request.method == 'POST':
        # Collect form data from POST request
        size = request.POST.get('size')
        total_slot = request.POST.get('total_slot')
        availability = request.POST.get('availability')
        price = request.POST.get('price')
        location = request.POST.get('location')
        place = request.POST.get('place')
        space_type = request.POST.get('space_type')
        feature = request.POST.get('feature')
        operating_hours = request.POST.get('operating_hours')
        contact_information = request.POST.get('contact_information')
        image = request.FILES.get('image')
      
        space_name = request.POST.get('space_name')
        slot_quantity = request.POST.get('slot_quantity')

        # Check if all required fields are provided
        
        try:

   

            cr.size=size
            cr.total_slot=total_slot
            cr.availability=availability
            cr.price=price
            cr.location=location
            cr.place=place
            cr.space_type=space_type
            cr.feature=feature
            cr.operating_hours=operating_hours 
            cr.contact_information=contact_information  
            if image:
                cr.image=image
        
            cr.space_name=space_name
            cr.slot_quantity=slot_quantity 
            cr.save()

            obj_info = {
            'size':cr.size,
            'total_slot':cr.total_slot,
            'availability':cr.availability,
            'price':cr.price,
            'location':cr.location,
            'place':cr.place,
            'space_type':cr.space_type,
            'feature':cr.feature,
            'operating_hours':cr.operating_hours,
            'contact_information':cr.contact_information,
            'image':cr.image,
            
            'space_name':cr.space_name,
            'slot_quantity':cr.slot_quantity
            }
        except Exception as e:
            print(e)

            return render(request,'editarea.html',obj_info)     
    return render(request,'editarea.html',area_info)


def area_list(request, id):
    area = get_object_or_404(Add_areas, id=id)
    return render(request, 'area_list.html', {'area': area})

def delete_area(request, id):
    try:
        space = Add_areas.objects.get(id=id)
        # Add your deletion logic here
        space.delete()
        return redirect('arealist')  # Redirect to a list of users or another page
    except Add_areas.DoesNotExist:
        raise Http404("Area not found")


# def area_list(request):
#     areas = Add_areas.objects.all()  # Fetch all Add_areas objects from the database
#     return render(request, 'area_list.html', {'areas': areas})

def arealist(request):
    areas = Add_areas.objects.all()  # Fetch all Add_areas objects from the database
    return render(request, 'arealist.html', {'areas': areas})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Slotfeedback, Add_areas
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def slotfeedback(request, id):
    if request.method == "POST":
        area = id
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback_text')

        # Validate and create the feedback entry
        if rating and feedback_text:
            try:
                feedback = Slotfeedback.objects.create(
                    slot=area,
                    rating=int(rating),
                    feedback_text=feedback_text
                )
                return JsonResponse({'status': 'success', 'message': 'Feedback saved successfully'})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid rating value'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing feedback data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




    

def addbook(request,id):
    email=request.session['email']
    dt=Add_areas.objects.get(id=id) 
    j=dt.slot_quantity
    b=dt.size
    c=dt.availability
    d=dt.price
    e=dt.location
    f=dt.space_type
    g=dt.feature
    h=dt.operating_hours
    i=dt.contact_information
    k=dt.space_name
    
    z=dt.place
    return render(request,"addbook.html",{'j':j,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'h':h,'i':i,'k':k,'m':email,'z':z})

import os
import qrcode
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse

def add_book(request):
    if request.method == 'POST':
        # Collect form data
        size = request.POST.get('size')
        availability = request.POST.get('availability')
        price = request.POST.get('price')
        location = request.POST.get('location')
        place = request.POST.get('place')
        space_type = request.POST.get('space_type')
        feature = request.POST.get('feature')
        operating_hours = request.POST.get('operating_hours')
        contact_information = request.POST.get('contact_information')
        slot_quantity = int(request.POST.get('slot_quantity'))
        
        space_name = request.POST.get('space_name')
        print(space_name)

        phone = request.POST.get('phone')
        carname = request.POST.get('carname')
        brandname = request.POST.get('brandname')
        date = request.POST.get('date')
        idproof = request.FILES.get('idproof')
        time = request.POST.get('time')
        name = request.POST.get('name')
        carnumber = request.POST.get('carnumber')
        email = request.POST.get('email')
        slot = int(request.POST.get('slot'))  # Number of slots the user wants to book

        # Retrieve the area data
        car_data = Add_areas.objects.get(space_name=space_name)
        existing_booking = book.objects.filter(space_name=space_name, date=date).exists()

        if existing_booking:
            # If a booking already exists for the same space and date, render error.html
            alert = "<script>alert('Booking already exists!');window.location.href = '/add_book/';</script>"
            return HttpResponse(alert)
        else:
            # Check if there are enough slots available
            if car_data.slot_quantity >= slot:
                # Update slot_quantity after booking
                car_data.slot_quantity -= slot
                car_data.save()

                # Proceed with the booking
                user_email = request.session.get('email')
                user_info = user_reg.objects.get(email=user_email)
                phone = user_info.phone
                email = user_info.email

                # Create and save the booking object
                booking_obj = book(
                    slot_quantity=slot_quantity,
                    slot=slot,
                    size=size,
                    availability=availability,
                    price=price,
                    location=location,
                    place=place,
                    space_type=space_type,
                    feature=feature,
                    operating_hours=operating_hours,
                    contact_information=contact_information,
                    space_name=space_name,
                    phone=phone,
                    carname=carname,
                    brandname=brandname,
                    date=date,
                    idproof=idproof,
                    time=time,
                    name=name,
                    carnumber=carnumber,
                    email=email
                )
                booking_obj.save()
                import qrcode
                                # Create a string with the booking details (name, car number, and email)
                qr_data = "Name: {name}\nCar Number: {carnumber}\nEmail: {email}"
                qr_img = qrcode.make(qr_data)
                print('qr data is',qr_data)
                #type(img)  # qrcode.image.pil.PilImage
                #img.save("some_file.png")



                # Generate QR code containing the details (text data, not just URL)
                #qr_img = qrcode.make(qr_data)

                # Define the directory where the QR code will be saved
                qr_code_directory = os.path.join(settings.BASE_DIR, 'static', 'qrcodes')

                # Ensure the directory exists
                os.makedirs(qr_code_directory, exist_ok=True)

                # Save the QR code image to the directory
                qr_code_filename = f"booking_{carnumber}.png"
                qr_code_path = os.path.join(qr_code_directory, qr_code_filename)
                qr_img.save(qr_code_path)

                # Provide the file path or URL to access the saved QR code
                qr_code_url = f"/static/qrcodes/{qr_code_filename}"
                return redirect('user_home')
                # Render the page and pass the QR code URL and booking data
                return render(request, 'user_home.html', {'qr_code_url': qr_code_url, 'booking': booking_obj})
            else:
                # Not enough slots available
                return redirect('payment')

    else:
        return render(request, 'addbook.html')


def update_status(request):
    if request.method=="POST":
        email = request.POST.get('email')
        status = request.POST.get('status')
    if not email or not status:
        return redirect('userlist')
    if status not in['applied','approved','rejected']:
        return redirect('userlist')
    constr=get_object_or_404(user_reg,email=email)
    constr.status=status 
    constr.save()
    return redirect('userlist')                    


def book_list(request):
    email = request.session.get('email')
    print(email)
    if email:
        books = book.objects.filter(email=email)
        return render(request, 'book_list.html', {'books': books})
    else:
        return redirect('login') 
    
#booking list of all users in admin interface    
def userbookings(request):
    booklist=pay.objects.all()
    return render(request,'userbookings.html', {'booklist': booklist})



from django.utils import timezone
from datetime import timedelta
def payment(request):
    email = request.session['email']
    print(email)
    cr = book.objects.filter(email=email).first()
    
    print(cr)
    pr=cr.space_name
    print(pr)
    # print(cr)
    # lp=cr.space_name
    # print(lp)
    totalprice = 0
    p=Add_areas.objects.get(space_name=pr)
    print(p)
    q = int(p.slot_quantity) - 1
    print (q)
    p.slot_quantity=q
    p.save()
    time_value = int(cr.time)
    print(time_value)  # Convert to integer (hours or minutes)
                
                # Get current time
    current_time = timezone.now()
    print(f"Current time: {current_time}")
    end_time = current_time + timedelta(hours=time_value)
    print(f"End time: {end_time}")


        # Multiply the price by the slot
    calculated_price = int(cr.price) * int(cr.slot) * int(cr.time)

        # Save the payment crnformatcron wcrth the calculated prcrce
    pay(
        phone=cr.phone,
        price=calculated_price,  # Use calculated price here
        name=cr.name,
        email=cr.email,
        space_name=cr.space_name,
        slot=cr.slot,
        time=time_value,
        
        timei=current_time, 
        endtime=end_time
    ).save()

        # Accumulate the total price
    totalprice += calculated_price

        # Delete the booking entry after processing
    

    # Convert the total price for payment processing (e.g., Razorpay expects amount in paise)
    totalprice = int(totalprice * 100)  # Convert to paise (100 paise = 1 INR)
    amount = totalprice

    print('Total amount is', str(amount))
    currency = 'INR'

    # Create a Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

    # Extract Razorpay order ID for the new payment
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Pass necessary details to the template for Razorpay payment integration
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'payment.html', context=context)


@csrf_exempt
def paymenthandler(request):

    if request.method=="POST":
        try:
            payment_id= request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = {
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment':payment_id,
                'razorpay_signature':signature
            }
            result=razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount=20000
                try:
                    razorpay_client.payment.capture(payment_id,amount)
                    email = request.session['email']
                    print(email)
                    cr = book.objects.filter(email=email).first()
                    cr.delete()

                    alert = "<script>alert('Booking Confirmed!');window.location.href = '/pay_success/';</script>"
                    return HttpResponse(alert)
                except:

                    return render(request, 'pay_failed.html')
            else:

                return render(request, 'pay_failed.html')
        except Exception as e:

            return redirect('user_home')
        
    else:
        return redirect('user_home')


def delete_booking(request, booking_id):
    if request.method == 'POST':
        # Retrieve the booking
        booking = get_object_or_404(book, id=booking_id)
        
        # Retrieve the associated parking area (Add_areas) based on the space_name
        parking_area = Add_areas.objects.get(space_name=booking.space_name)
        
        # Increment the slot_quantity by the number of slots that were booked
        parking_area.slot_quantity += booking.slot
        parking_area.save()

        # Delete the booking
        booking.delete()
        
        # Notify the user of the successful deletion
        messages.success(request, 'Booking has been deleted and slots have been released.')
        
        # Redirect to user's home page or booking list
        return redirect('user_home')


from django.shortcuts import render
from .models import Add_areas

def area_details(request):
    # Handle search query
    if request.method == 'POST':
        location = request.POST.get('location')
        # Filter the areas based on location
        areas = Add_areas.objects.filter(location__icontains=location)
    else:
        # If no search, display all areas
        areas = Add_areas.objects.all()

    return render(request, 'area_details.html', {'areas': areas})


def view_details(request, id):
    # Fetch the specific parking area by its ID or return a 404 if not found
    area = get_object_or_404(Add_areas, id=id)
    feedback=Slotfeedback.objects.filter(slot__id=id)
    
    # Pass the 'area' object to the template
    return render(request, 'view_details.html', {'area': area,'feedback':feedback})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Slotfeedback, Add_areas
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Slotfeedback, Add_areas
from django.http import HttpResponse

def save_feedback(request, slot_id):
    if request.method == "POST":
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback_text')

        if rating and feedback_text:
            try:
                # Fetch the specific slot using the slot_id passed to the view
                slot = Add_areas.objects.get(id=slot_id)
                feedback = Slotfeedback(
                    slot=slot,
                    rating=int(rating),
                    feedback_text=feedback_text
                )
                feedback.save()
                messages.success(request, "Feedback submitted successfully!")
            except Add_areas.DoesNotExist:
                messages.error(request, "Selected slot not found.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

            return redirect('feedback_success')  # Redirect to a success page or show a message
        else:
            messages.error(request, "Please fill out all fields.")
            return redirect('save_feedback', slot_id=slot_id)  # Redirect back to the feedback form

    else:
        try:
            slot = Add_areas.objects.get(id=slot_id)
            return render(request, 'slotfeedback.html', {'slot': slot})
        except Add_areas.DoesNotExist:
            messages.error(request, "Slot not found.")
            return redirect('feedback_success')  # Redirect to the success page if slot is not found
        

def feedback_success(request):
    return HttpResponse("Thank you for your feedback!")


from django.http import JsonResponse

def add_favourites(request, id):
    area = models.Add_areas.objects.get(id=id)
    semail = request.session.get('email')
    
    if not semail:
        return redirect('login')  
    
    user = models.user_reg.objects.get(email=semail)
    data, created = models.favourites.objects.get_or_create(area=area, user=user)
    
    if created:
        response = {'success': True}
    else:
        response = {'success': False}
    
    if request.is_ajax():
        return JsonResponse(response)
    else:
        if created:
            return redirect('wishlist')  
        else:
            alert = "<script> alert('You already added');window.location.href='/wishlist/'</script>"
            return HttpResponse(alert)



def wishlist(request):
    semail = request.session.get('email')
    user = models.user_reg.objects.get(email=semail)
    favourite_areas =models.favourites.objects.filter(user=user)
    return render(request, 'wishlist.html',{'areas':favourite_areas})

def slotfeed(request):

    user = models.Slotfeedback.objects.all()

    return render(request, 'slotfeed.html',{'feed':user})



def remove_wishlist(request,id):
    wishlist=models.favourites.objects.get(id=id)
    wishlist.delete()
    return redirect('wishlist')

def get_liked_areas(user):
    return models.favourites.objects.filter(user=user).values_list('area', flat=True)

def some_view(request):
    semail = request.session.get('email')
    if semail:
        user = models.user_reg.objects.get(email=semail)
        liked_areas = get_liked_areas(user)  # List of areas the user has liked
        areas = models.Add_areas.objects.all()  # Or whatever queryset you're displaying
        
        for area in areas:
            area.is_liked = area.id in liked_areas  # Add a property to check if area is liked
            
    else:
        areas = models.Add_areas.objects.all()

    return render(request, 'area_details.html', {'area': areas})


def recurring(request):
    if request.method == 'POST':
            # Collect form data from POST request
            size = request.POST.get('size')
            availability = request.POST.get('availability')
            price = request.POST.get('price')
            location = request.POST.get('location')
            place = request.POST.get('place')
            space_type = request.POST.get('space_type')
            feature = request.POST.get('feature')
            operating_hours = request.POST.get('operating_hours')
            contact_information = request.POST.get('contact_information')
            image = request.FILES.get('image')
            area_email = request.POST.get('area_email')
            space_name = request.POST.get('space_name')
            slot_quantity = request.POST.get('slot_quantity')

            # Check if all required fields are provided
            if not all([size, availability, price, location, place, space_type, feature, operating_hours, contact_information, image, area_email, space_name, slot_quantity]):
                return render(request, 'area.html', {'error': 'All fields are required'})

            # Create new Add_areas instance and save it to the database
            new_area =recurring(
                size=size,
                availability=availability,
                price=price,
                location=location,
                place=place,
                space_type=space_type,
                feature=feature,
                operating_hours=operating_hours,
                contact_information=contact_information,
                image=image,
                area_email=area_email,
                space_name=space_name,
                slot_quantity=slot_quantity
            ).save()  # Save and generate QR code
            return render(request,'admin_home.html',{'message': 'Area added successfully'})

    else:
        return render(request,'recurring.html')
            

import requests
from django.shortcuts import render
from .models import Add_areas

# Function to get coordinates from OpenStreetMap's Nominatim API
import requests
import logging

# Initialize logging
logger = logging.getLogger(__name__)

import requests
import logging

# Initialize logging
logger = logging.getLogger(__name__)

def get_coordinates(city_name):
    # Clean the city name to ensure it's URL safe
    city_name = city_name.replace(" ", "+")
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&addressdetails=1"

    headers = {
        'User-Agent': 'YourAppName/1.0 (your@email.com)'  # Replace with your app name and contact email
    }

    try:
        # Send request to Nominatim API with the User-Agent header
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            logger.error(f"No data returned for city: {city_name}")
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for city {city_name}: {e}")
        return None, None
    except ValueError as e:
        logger.error(f"JSON decoding error for city {city_name}: {e}")
        return None, None



# View to render the parking spaces map
def parking_spaces_map(request):
    # Fetch all parking areas
    areas = Add_areas.objects.all()

    # List to store coordinates for all areas
    area_locations = []

    for area in areas:
        lat, lon = get_coordinates(area.location)
        print('lati',lat)
        print('longi',lon)  # Get coordinates for the location
        if lat and lon:
            area_locations.append({
                'name': area.space_name,
                'lat': lat,
                'lon': lon,
                'place': area.place,
                'image': area.image.url if area.image else '',
            })

    return render(request, 'map_view.html', {'area_locations': area_locations})


import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from math import radians, sin, cos, sqrt, atan2

def get_nearby_locations(location_name, radius_km=30):
    """Get nearby locations using OpenStreetMap Nominatim API"""
    try:
        # Get coordinates for the input location
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": location_name,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }
        headers = {
            "User-Agent": "YourApp/1.0"  # Required by Nominatim
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        
        if not data:
            return []
            
        base_lat = float(data[0]['lat'])
        base_lon = float(data[0]['lon'])
        
        # Get area around the location
        area_url = f"https://nominatim.openstreetmap.org/reverse"
        area_params = {
            "lat": base_lat,
            "lon": base_lon,
            "format": "json",
            "zoom": 100,  # Administrative level for nearby areas
            "addressdetails": 1
        }
        
        area_response = requests.get(area_url, params=area_params, headers=headers)
        area_data = area_response.json()
        
        # Extract nearby areas from address details
        nearby_areas = []
        if 'address' in area_data:
            for key, value in area_data['address'].items():
                if key in ['city', 'town', 'village', 'suburb', 'neighbourhood',]:
                    nearby_areas.append(value.lower())
        
        return nearby_areas
        
    except Exception as e:
        print(f"Error fetching locations: {str(e)}")
        return []

@csrf_exempt
def get_nearby_shops(request):
    
    if request.method == "POST":
        user_location = request.POST.get("location", "").lower()
        
        try:
            # Get nearby areas using the API
            nearby_areas = get_nearby_locations(user_location)
            print(nearby_areas)
            
            # Include user's location in search
            search_locations = [user_location] + nearby_areas
            print(search_locations)
            
            # Find shops in these locations
            nearby_shops = []
            for location in search_locations:
                shops = Add_areas.objects.filter(location__icontains=location)
                for shop in shops:
                    if shop.id not in [s['shop_id'] for s in nearby_shops]:  # Avoid duplicates
                        nearby_shops.append({
                            "shop_id": shop.id,
                            "shop_name": shop.space_name,
                            "shop_location": shop.location,
                            "shop_phone": shop.contact_information,
                            "recurr": shop.recurringquantity,
                           

                        })
                        print(f"Nearby shops: {nearby_shops}") 
            
            return JsonResponse({"shops": nearby_shops})
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return render(request, 'display_products_loc.html')



def cart_list(request):
    # Fetch the user's cart items
    if 'email' in request.session:
        email = request.session['email']
        juser = user_reg.objects.get(email=email)
        print(juser)
        cart_items = icart.objects.filter(user=juser)

        return render(request, 'cart_list.html', {'cart_items': cart_items})
    else:
        return redirect('login')

def add_cart(request,pid):
    if 'email' in request.session:
        email=request.session.get('email')
        us=user_reg.objects.get(email=email)
        products=Add_areas.objects.get(id=pid)
    
    
        
        

        if request.method == "POST":
            quantity = request.POST.get('quantity')
            quantity=int(quantity)
            total_price = Decimal(request.POST.get('total'))
            start = request.POST.get('start')
            end = request.POST.get('end')
            cart_item,created=icart.objects.get_or_create(user=us,products=products,defaults={'quantity':quantity,'total_price':total_price} )
            if not created:
                cart_item.quantity = quantity
                cart_item.total_price=total_price
                cart_item.start=start
                cart_item.end=end
                cart_item.save()

                return redirect('cart_list')
            
        else:
            return render(request,'cart.html',{'prd':products})
    else:
        return redirect('cart_list')
    
from django.contrib.auth import logout
import razorpay # type: ignore
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt

# from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt







def initiate_payment(request,cid):
    email = request.session['email']
    if email:
        crt=icart.objects.get(id=cid)
        am=crt.total_price
        amount = int(am)*100 
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        order_id = payment_order['id']
        juser = user_reg.objects.get(email=email)
        buyer_data = {
            'buyer': {
                'id': juser.id,
                'name': juser.first_name,
                'email': juser.email,
                'phone': juser.phone,
                # Add other fields as needed
            }
        }
        response_data = {'order_id': order_id, 'amount': amount}
        response_data.update(buyer_data)
        return JsonResponse(response_data, encoder=DjangoJSONEncoder)
    else:
        return redirect('log')
    

from decimal import Decimal   
@csrf_exempt
def confirm_payment(request, order_id, payment_id,crti_id):
    print('Confirm payment')
    try:
        print('Payment ID:', payment_id)
        print('order_id:', order_id)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        print('Payment:', payment['order_id'])
        print('payment', payment)
        if payment['order_id'] == order_id and payment['status'] == 'captured':
            pemail = payment.get('email')
            amount = payment.get('amount')
            amount_in_rupees = Decimal(amount) / Decimal(100)  

            if pemail:
                usr = user_reg.objects.get(email=pemail)
                crts=icart.objects.get(id=crti_id)
                prd=crts.products
                p=Add_areas.objects.get(id=crts.products.id)
                q = int(p.recurringquantity) - 1

                p.recurringquantity=q
                print(q)
                p.save()

                prd=crts.products
                trns=Transaction(user=usr,products=prd,amount=amount_in_rupees,quantity=crts.quantity,order_id=order_id)
                trns.save()

                crts.delete()
                return redirect('user_home')

            else:
               return JsonResponse({'status': 'failure', 'error': 'User email not found'})
        else:
            print(payment['status'])
            return JsonResponse({'status': 'failure', 'error': 'Payment status not captured'})
    except Exception as e:
        print('Error:', str(e))
        return redirect('user_home')


from django.shortcuts import render
from .models import pay

def trans_history(request):
    # Get the user's email from the session
    email = request.session.get('email')
    
    
    # Fetch all transactions related to the email
    user = pay.objects.filter(email=email)
    recurring=Transaction.objects.filter(user__email=email)
    
    
    # Render the 'mytrans.html' template and pass the user data
    return render(request, 'transaction_history.html', {'user': user,'recurring':recurring})

def xrepay(request):
    email = request.session.get('email')
    user = YTRExtrapay.objects.filter(user__email=email)
    return render(request, 'xrepay.html', {'user': user})




def transhistory(request):
    user = pay.objects.all()
    recurring=Transaction.objects.all()
    
    # Render the 'mytrans.html' template and pass the user data
    return render(request, 'transactionhistory.html', {'user': user,'recurring':recurring})


from django.shortcuts import render
from .models import Add_areas  # Ensure the correct model import

def recur_list(request):
    recurring_areas = Add_areas.objects.all()  # Fetch all areas
    return render(request, 'recur_list.html', {'recurring_areas': recurring_areas})







def show_map(request):
    return render(request, 'mapp.html')  # 'map.html' is the template to render the map
def logout(request):
    # Log out the user


    # Optional: Flush the session (remove all session data)
    request.session.flush()

    # Redirect to the index (homepage)
    return redirect('index')  # Ensure 'index' is the name of your URL pattern


def about(request):
    return render(request,'about.html')



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import YTRExtrapay, Transaction
from django.contrib import messages

def xtrapay(request, transaction_id):
    transaction = pay.objects.get(id=transaction_id)
    print(transaction)
    
  
    
     # Fetch the transaction based on its ID
    space=transaction.space_name
    print(space)
    std=Add_areas.objects.get(space_name=space)
    

    if request.method == "POST":
        # Get the amount and time from the POST request
        
        time = int (request.POST.get('time'))
        amount=std.price
        totalm=amount * time
        print(totalm)
        print(amount)
        emal=transaction.email
        print(emal)
        # Check if both amount and time are provided
        if time:
            try:
            # Save the data to the Extrapay model
                lop = pay.objects.get(id=transaction_id)
                print(lop)
                extrapa = YTRExtrapay(email=emal,Tpay=lop, Tamount=int(totalm), Ttime=int(time))
                extrapa.save()
                send_mail(
                subject='hello - Welcome!',
                message=(
                    f'Dear {transaction.name},\n\n'
                    f'space: {transaction.space_name},\n\n'
                    f'you have an extrapayment of {totalm}.\n'
                    f'for time: {time} hours \n\n'
                    f'Best regards,\nYour Application Team'
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[emal],  # Send to the registered user's email
            )
          

                messages.success(request, 'Extrapay details saved successfully!')
                return redirect('transhistory')  # Redirect to a success page (or wherever you want)
            except Exception as e:
                print("error",e)
        else:
            messages.error(request, 'Please provide both amount and time.')

    return render(request, 'extrapay_form.html', {'transaction': transaction})



from django.shortcuts import render
from .models import YTRExtrapay
from django.conf import settings

from django.conf import settings

def xrepay(request):
    email = request.session.get('email')
    user = YTRExtrapay.objects.filter(email=email)

    return render(request, 'xrepay.html', {
        'user': user,
        'RAZOR_KEY_ID': settings.RAZOR_KEY_ID  # Ensure it's available in settings.py
    })

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import YTRExtrapay

@csrf_exempt
def update_payment_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get("payment_id")
        razorpay_payment_id = data.get("razorpay_payment_id")

        try:
            payment = YTRExtrapay.objects.get(id=payment_id)
            payment.status = "paid"
            payment.save()
            return JsonResponse({"success": True})
        except YTRExtrapay.DoesNotExist:
            return JsonResponse({"success": False, "error": "Payment not found"}, status=400)
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



   
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import pay

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import pay

def request_refund(request, transaction_id):
    if request.method == "POST":
        refund_hours = request.POST.get("refund_hours")
        print(refund_hours)
        refund_hours = int(refund_hours)
        print(f"Refund Hours: {refund_hours}")
        transaction = pay.objects.get(id=transaction_id)
        print(transaction)  # Fetch the transaction based on its ID
        space=transaction.space_name
        print(space)
        std=Add_areas.objects.get(space_name=space)
        amount=std.price
        totalm=amount * refund_hours

        if refund_hours:  # Ensure input is a valid number
            transaction.refund = "Requested"
            transaction.refundendtime = refund_hours
            transaction.refundendamount=totalm
            transaction.refundtime = timezone.now() 
            transaction.save()
            return JsonResponse({"success": True, "message": "Refund request submitted successfully."})
        else:
            return JsonResponse({"success": False, "message": "Invalid refund hours. Please enter a valid number."})

    return JsonResponse({"success": False, "message": "Invalid request."})



def refund_requests(request):
    requested_refunds = pay.objects.filter(refund="Requested")  # Fetch only "Requested" refunds
    return render(request, "refundrequests.html", {"transactions": requested_refunds})


def update_refund_status(request, transaction_id, status):
    transaction = get_object_or_404(pay, id=transaction_id)

    if status in ["Approved", "Rejected"]:
        transaction.refund = status
        transaction.save()
        messages.success(request, f"Refund {status.lower()} successfully.")
        return redirect("refund_requests")  # Redirect back to the refund page

    messages.error(request, "Invalid action.")
    return redirect("refund_requests")



def approvedrequests(request):
    requested_refunds = pay.objects.filter(refund="Approved")  # Fetch only "Requested" refunds
    return render(request, "approvedrequests.html", {"transactions": requested_refunds})


import razorpay
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import pay

# Razorpay client setup
razorpay_client = razorpay.Client(auth=("rzp_test_X5OfG2jiWrAzSj", "SsCovWWZSwB1TGd1rSoIiwF3"))

def payment_success(request):
    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")
        payment_id = request.POST.get("razorpay_payment_id")

        transaction = get_object_or_404(pay, id=transaction_id)
        transaction.razorpay_payment_id = payment_id
        transaction.refund = "Refunded"  # Automatically update refund status
        transaction.save()

        return JsonResponse({"status": "success", "message": "Payment successful, refund processed."})
    
    return JsonResponse({"status": "failed", "message": "Invalid request."})
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import icart

def delete_cart_item(request, id):
    
    cart_item = get_object_or_404(icart, id=id)
    cart_item.delete()
    return redirect('cart_list')  



from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

import random
import time

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_reg.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            request.session['reset_email'] = email
            request.session['otp_timestamp'] = time.time()

            return redirect('verify_otp')
        except user_reg.DoesNotExist:
            return HttpResponse("<script>alert('Email not found'); window.location.href='/forgot-password/';</script>")
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')
        otp_timestamp = request.session.get('otp_timestamp', 0)

        if not email:
            return redirect('forgot_password')

        if time.time() - otp_timestamp > 300:  # OTP expires in 5 minutes
            return HttpResponse("<script>alert('OTP expired! Request a new one.'); window.location.href='/forgot-password/';</script>")
        try:
            user = user_reg.objects.get(email=email)
            if str(user.otp) == otp_entered:
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                return HttpResponse("<script>alert('Invalid OTP'); window.location.href='/verify-otp/';</script>")
        except user_reg.DoesNotExist:
            return redirect('forgot_password')
    return render(request, 'verify_otp.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_verified = request.session.get('otp_verified', False)
        new_password = request.POST.get('new_password')

        if not email or not otp_verified:
            return redirect('forgot_password')
        try:
            user = user_reg.objects.get(email=email)
            user.password = new_password
            user.otp = None
            user.save()

            del request.session['reset_email']
            del request.session['otp_verified']
            del request.session['otp_timestamp']
            
            return HttpResponse("<script>alert('Password reset successful!'); window.location.href='/login/';</script>")
        except user_reg.DoesNotExist:
            return redirect('forgot_password')
    return render(request, 'reset_password.html')