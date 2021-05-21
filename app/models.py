from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.
class Section(models.Model):
    section = models.CharField(max_length = 200,default ="")
    faculty = models.ForeignKey(User, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.section} {self.faculty}'

class Student_link(models.Model):
    section = models.ForeignKey(Section, null=True, on_delete = models.CASCADE)
    roll_number = models.CharField(max_length = 200,null = True)
    email = models.EmailField(max_length=400,null = True)

    def __str__(self):
        return f'{self.email}. {self.section.section}'

class Room(models.Model):
    ROOM_CATEGORIES = (
        ("PHY","Physics"),
        ("IT","Information Technology"),
        ("CHEM","Chemistry"),
        ("EEE","Electronic"),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=5, choices = ROOM_CATEGORIES)

    def __str__(self):
        return f'{self.number}. {self.category}'

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    room = models.ForeignKey(Room,on_delete = models.CASCADE)
    section = models.ForeignKey(Section,on_delete = models.CASCADE,null=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'

    def get_cancel_booking_url(self):
            return reverse_lazy('CancelBookingView', args = [self.pk,])

class resource(models.Model):
    ROOM_CATEGORIES = (
        ("PHY","Physics"),
        ("IT","Information Technology"),
        ("CHEM","Chemistry"),
        ("EEE","Electronic"),
    )
    category = models.CharField(max_length=5, choices = ROOM_CATEGORIES)
    resource_name=models.CharField(max_length=122,null = True)
    resource_id=models.CharField(max_length=122,null = True)
    #quantity=models.IntegerField()

    def __str__(self):
        #return self.lab_id,self.resource_id,self.resource_name,self.quantity
        #return self.resource_id
        return '%s' % (self.resource_name)

class resource_booking(models.Model):
    status_category=(("Pending","Pending"),
                      ("Accepted","Accepted"),
                      ("Declined","Declined"))
    select_booking=models.ForeignKey(Booking,on_delete = models.CASCADE)
    select_resource=models.ForeignKey(resource,on_delete = models.CASCADE)
    quantity=models.IntegerField()
    status=models.CharField(max_length=12,choices=status_category,default='Pending')
    def __str__(self):
        return '%s %s %s %s'%(self.select_booking,self.select_resource,self.quantity,self.status)
