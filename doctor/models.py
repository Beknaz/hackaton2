from unicodedata import category
from django.db import models
from account.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)


class Service_listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    Categories = models.ManyToManyField(Category, related_name='doctors')
    adress = models.CharField(max_length=255)
    image = models.ImageField(upload_to='rooms', null=True, blank=True)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='doctors')
    number = models.CharField(max_length=13)
    service_listing = models.ManyToManyField(Service_listing, related_name='doctors', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} => {self.title}"
    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Entry(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='entrys', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='entrys', on_delete=models.CASCADE)
    service_listing = models.ForeignKey(Service_listing, related_name='entrys', on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(auto_now_add=True)
    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()


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








