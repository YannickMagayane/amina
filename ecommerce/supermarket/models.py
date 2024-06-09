from django.db import models
import cv2
import os
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

    def remove_background(self):
        if self.photo:
            image_path = self.photo.path

            # Charger l'image avec OpenCV
            image = cv2.imread(image_path)

            # Convertir l'image en niveau de gris
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Appliquer un seuillage pour séparer l'avant-plan de l'arrière-plan
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

            # Trouver les contours de l'avant-plan
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Créer un masque pour l'avant-plan
            mask = cv2.drawContours(image.copy(), contours, -1, (255, 255, 255), thickness=cv2.FILLED)

            # Appliquer le masque pour supprimer l'arrière-plan
            result = cv2.bitwise_and(image, mask)

            # Obtenir le nom du fichier sans extension
            filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]

            # Enregistrer l'image sans arrière-plan avec le nom du supermarché
            output_path = os.path.join(os.path.dirname(image_path), f"{filename_without_extension}_no_bg.png")
            cv2.imwrite(output_path, result)

            return output_path

        return None

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


