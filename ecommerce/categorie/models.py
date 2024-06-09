from django.db import models
from PIL import Image
import io
import base64
import os
from auditlog.registry import auditlog


class Categories(models.Model):
    name = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name

    def photo_to_svg(self):
        if self.photo:
            image_path = self.photo.path

            # Charger l'image avec PIL
            with open(image_path, 'rb') as image_file:
                image = Image.open(image_file)

                # Convertir l'image en données base64
                image_bytes = image_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')

                # Créer le contenu SVG avec l'élément image
                svg_data = f'<svg xmlns="http://www.w3.org/2000/svg" width="{image.width}" height="{image.height}">'
                svg_data += f'<image xlink:href="data:image/png;base64,{image_base64}" width="{image.width}" height="{image.height}" />'
                svg_data += '</svg>'

                return svg_data
        return None


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Renommer le fichier SVG avec le nom de la catégorie
        if self.photo:
            image_path = self.photo.path

            # Obtenir le nom du fichier sans extension
            filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]

            # Renommer le fichier SVG avec le nom de la catégorie
            svg_filename = f"{filename_without_extension}_{self.name}.svg"
            svg_path = os.path.join(os.path.dirname(image_path), svg_filename)

            # Convertir l'image en SVG et enregistrer le fichier
            svg_data = self.photo_to_svg()
            if svg_data:
                with open(svg_path, 'w') as svg_file:
                    svg_file.write(svg_data)

    @classmethod
    def filter_by_name(cls, name):
        return cls.objects.filter(name__icontains=name)

    @classmethod
    def filter_by_image(cls, image_path):
        return cls.objects.filter(photo__exact=image_path)

auditlog.register(Categories)
