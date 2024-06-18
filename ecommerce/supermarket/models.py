from django.db import models
from user.models import User
from auditlog.registry import auditlog


class SuperMarket(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    localisation = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='supermarket')
    is_activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    @classmethod
    def filter_by_name(cls, name):
        return cls.objects.filter(name__icontains=name)

    @classmethod
    def filter_by_localisation(cls, localisation):
        return cls.objects.filter(localisation__icontains=localisation)
    
    @classmethod
    def filter_by_image(cls, image_path):
        return cls.objects.filter(photo__exact=image_path)

auditlog.register(SuperMarket)


