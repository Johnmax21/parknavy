from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.urls import reverse


# Create your models here.
class user_reg(models.Model):
    STATUS = (
    ('applied', 'Applied'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    )
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField()
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    age=models.IntegerField(null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    otp = models.IntegerField(null=True, blank=True)  # Store OTP for verification


    def generate_otp(self):
        self.otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        self.save()
        return self.otp

    def __str__(self):
        return self.first_name

    
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
        
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."
    
   



import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse
from django.db import models

class Add_areas(models.Model):
    space_name = models.CharField(max_length=100)
    size = models.IntegerField()
    availability = models.CharField(max_length=100)
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    space_type = models.CharField(max_length=100)
    feature = models.CharField(max_length=100)
    operating_hours = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=15)  # Changed to CharField to allow for phone formatting
    image = models.ImageField(upload_to='parking_images/', blank=True, null=True)
    slot_quantity = models.IntegerField()
    place = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    rentperday = models.IntegerField(null=True,blank=True)
    recurringquantity = models.IntegerField(null=True,blank=True)
    total_slot= models.IntegerField(null=True,blank=True)



    def __str__(self):
        return self.space_name

    def save(self, *args, **kwargs):
        # First, save the pet object if it does not have an ID yet
        if not self.id:
            super().save(*args, **kwargs)

        # Generate the QR code link using the pet detail page URL
        area_url = f"http://127.0.0.1:8000{reverse('area_list', args=[self.id])}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(area_url)  # Add the pet detail URL to the QR code
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code image to a file in memory
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)

        # Save the QR code image to the model's qr_code field
        self.qr_code.save(f'qr_code_{self.id}.png', File(buffer), save=False)

        # Call super().save() again to save the model with the QR code image
        super().save(*args, **kwargs)


class Slotfeedback(models.Model):
    slot=models.ForeignKey(Add_areas,on_delete=models.CASCADE)
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]   
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."

class book(models.Model):
    # area_id=models.IntegerField()

    space_name=models.CharField(max_length=100,null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True) 
    availability=models.CharField(max_length=100,null=True, blank=True)
    price=models.IntegerField(null=True, blank=True)
    location=models.CharField(max_length=100,null=True, blank=True)
    place=models.CharField(max_length=100,null=True, blank=True)
    space_type=models.CharField(max_length=100,null=True, blank=True)
    feature=models.CharField(max_length=100,null=True, blank=True)
    operating_hours=models.CharField(max_length=100,null=True, blank=True)
    contact_information=models.IntegerField(null=True, blank=True)
    area_email=models.EmailField(max_length=100,null=True, blank=True)
    slot_quantity=models.IntegerField()
    phone=models.IntegerField()
    carname=models.CharField(max_length=200)
    brandname=models.CharField(max_length=200)
    date=models.CharField(max_length=200) 
    idproof=models.ImageField(upload_to='idproof_images/', blank=True, null=True)
    time=models.CharField(max_length=20)
    name=models.CharField(max_length=100)
    carnumber=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    slot=models.IntegerField()
    tser=models.ForeignKey(Add_areas,on_delete=models.CASCADE,null=True,blank=True)
        

class pay(models.Model):
    
    price=models.IntegerField(null=True, blank=True)
    phone=models.IntegerField()
    space_name=models.CharField(max_length=100,null=True, blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    slot=models.IntegerField()
    time=models.IntegerField(null=True,blank=True)
    timei=models.TimeField(auto_now_add=True,null=True,blank=True)
    endtime=models.TimeField(null=True,blank=True)
    name=models.CharField(max_length=100)
    refund = models.CharField(max_length=10, choices=[('Requested', 'requested'),('Rejected', 'rejected') ,('Refunded', 'Refunded')], default='none')
    refundendtime=models.IntegerField(null=True,blank=True)
    refundendamount=models.IntegerField(null=True,blank=True)
    refundtime=models.TimeField(null=True,blank=True)


class favourites(models.Model):
    user=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    area=models.ForeignKey(Add_areas,on_delete=models.CASCADE)

class recurring(models.Model):
    space_name = models.CharField(max_length=100)
    size = models.IntegerField()
    availability = models.CharField(max_length=100)
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    space_type = models.CharField(max_length=100)
    feature = models.CharField(max_length=100)
    operating_hours = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=15)  # Changed to CharField to allow for phone formatting
    image = models.ImageField(upload_to='parking_images/', blank=True, null=True)
    area_email = models.EmailField(max_length=100)
    slot_quantity = models.IntegerField()
    place = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    recurringquantity = models.IntegerField(null=True,blank=True)





 

class icart(models.Model):
    user=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    products=models.ForeignKey(Add_areas,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    total_price=models.IntegerField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    start = models.DateField(null=True,blank=True)
    end = models.DateField(null=True,blank=True)
    


# Create your models here.

class Transaction(models.Model):
    user=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    products = models.ForeignKey(Add_areas,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    order_id= models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)







class YTRExtrapay(models.Model):
    email=models.EmailField(max_length=100,null=True,blank=True)
    Tpay = models.ForeignKey(pay,on_delete=models.CASCADE)
    Tamount=models.IntegerField(null=True, blank=True)
    Ttime=models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('failed', 'Failed'), ('Pending', 'pending')], default='Pending',null=True,blank= True)
