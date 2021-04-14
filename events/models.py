from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=data['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(data['email']) < 4:
            errors['email'] = "email must contain 4 or more characters"
        if len(data['fname']) < 2:
            errors['fname'] = "needs 2 or more characters for First Name"
        if len(data['lname']) < 2:
            errors['lname'] = "needs 2 or more characters for Last Name"
        if len(data['password']) < 8:
            errors['password'] = "Password must contain 8 or more characters"
        if data['password'] != data['confirm']:
            errors['password'] = "Passwords do not match"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    
class EventManager(models.Manager):
    def event_validator(self, data):
        errors = {}
        if len(data['event']) < 5:
            errors['event'] = "Event needs 5 or more characters"
        if len(data['location']) < 5:
            errors['location'] = "Location needs 5 or more characters"
        if len(data['time']) < 3:
            errors['time'] = "Time needs 3 or more characters"
        if len(data['date']) < 3:
            errors['date'] = "Date needs 3 or more characters"
        if len(data['head_count']) < 1:
            errors['head_count'] = "Needs 1 or more heads"
        return errors
    
class Event(models.Model):
    event = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True, null=True)
    time = models.CharField(max_length=20)
    head_count = models.CharField(max_length=20)
    user_event = models.ForeignKey(User, related_name="event_poster", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()