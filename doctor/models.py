from django.db import models
from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)
    my_doctors = models.ManyToManyField("doctor.Doctor", null=True, blank=True, related_name='categorys')
    def __str__(self):
        return f"{self.title} => {self.title}"


class ServiceListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.title} => {self.title}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='doctors')
    adress = models.CharField(max_length=255)
    image = models.ImageField(upload_to='doctors', null=True, blank=True)
    description = models.TextField()
    number = models.CharField(max_length=13)
    service_listing = models.ManyToManyField(ServiceListing, related_name='doctors', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} => {self.first_name}"

    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Entry(models.Model):

    TIMESLOT_LIST = (
        (0, '09:00 - 10:00'),
        (1, '10:00 - 11:00'),
        (2, '11:00 - 12:00'),
        (3, '12:00 - 13:00'),
        (4, '14:00 - 15:00'),
        (5, '15:00 - 16:00'),
        (6, '16:00 - 17:00'),
        (7, '17:00 - 18:00'),
    )

    doctor = models.ForeignKey(Doctor, related_name='entrys', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='entrys', on_delete=models.CASCADE)
    service_listing = models.ForeignKey(ServiceListing, related_name='entrys', on_delete=models.CASCADE)
    entrys_time = models.DateTimeField(auto_now_add=True)
    time_slot = models.IntegerField(choices=TIMESLOT_LIST)
    date = models.DateField(help_text="YYYY-MM-DD")

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.time_slot][1]


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='comments', on_delete=models.CASCADE)    
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment{self.user.username} -> {self.doctor.first_name} [{self.created_at}]"


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='likes', on_delete=models.CASCADE)
    def __str__(self):
        return f"Like{self.user.username} -> {self.doctor.first_name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='favorites', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.first_name}"


class Chat(models.Model):
    user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)
    sms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Chats{self.user.username} -> {self.sms.title} [{self.created_at}]"