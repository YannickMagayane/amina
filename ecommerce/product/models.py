from django.db import models
from categorie.models import Categories
from supermarket.models import SuperMarket
import cv2
import os
from django.db.models import Q
from collections import defaultdict
from auditlog.registry import auditlog


class Products(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(SuperMarket, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='produit')
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    marque = models.CharField(max_length=1000,blank=True,null=True)
    modele = models.CharField(max_length=1000,blank=True,null=True)

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

            # Enregistrer l'image sans arrière-plan avec le nom du produit
            output_path = os.path.join(os.path.dirname(image_path), f"{filename_without_extension}_no_bg.png")
            cv2.imwrite(output_path, result)

            return output_path

        return None

    
    def compare_prices(self):
        """
        Compare les prix des produits entre différents supermarchés dans la même catégorie.
        Sélectionne le produit avec le meilleur prix dans chaque groupe de catégorie et supermarché.
        """
        comparison_data = defaultdict(list)

        # Regrouper les produits par catégories et supermarchés
        for product in Products.objects.filter(categories=self.categories):
            comparison_data[product.supermarket.name].append(product)

        # Comparer les prix et sélectionner le meilleur prix dans chaque groupe de supermarché
        for key, products in comparison_data.items():
            products.sort(key=lambda x: x.prix)  # Trier les produits par prix
            best_price_product = products[0]  # Sélectionner le produit avec le meilleur prix
            comparison_data[key] = best_price_product

        return comparison_data

    def suggest_best_price_products(self):
        """
        Suggère les produits avec les meilleurs prix économiques dans la même catégorie.
        Utilise l'algorithme de comparaison des prix pour obtenir les meilleurs produits.
        """
        comparison_data = self.compare_prices()  # Appel à la méthode de comparaison des prix
        best_price_products = list(comparison_data.values())
        best_price_products.sort(key=lambda x: x.prix)  # Trier les produits par prix
        return best_price_products

    @classmethod
    def filter_by_name(cls, name):
        return cls.objects.filter(name__icontains=name)

    @classmethod
    def filter_by_category(cls, category_name):
        return cls.objects.filter(categories__name__icontains=category_name)

    @classmethod
    def filter_by_supermarket(cls, supermarket_name):
        return cls.objects.filter(supermarket__name__icontains=supermarket_name)

    @classmethod
    def filter_by_price_range(cls, min_price, max_price):
        return cls.objects.filter(prix__gte=min_price, prix__lte=max_price)

    @classmethod
    def filter_by_description(cls, keywords):
        query = Q()
        for keyword in keywords.split():
            query |= Q(description__icontains=keyword)
        return cls.objects.filter(query)
    
    @classmethod
    def filter_by_marque(cls, marque):
        return cls.objects.filter(marque__icontains=marque)

    @classmethod
    def filter_by_modele(cls, modele):
        return cls.objects.filter(modele__icontains=modele)

    @classmethod
    def suggest_products(cls, category, name=None, min_price=None, max_price=None):
        suggested_products = cls.objects.filter(categories=category)

        if name:
            suggested_products = suggested_products.filter(name__icontains=name)

        if min_price is not None and max_price is not None:
            suggested_products = suggested_products.filter(prix__gte=min_price, prix__lte=max_price)
        elif min_price is not None:
            suggested_products = suggested_products.filter(prix__gte=min_price)
        elif max_price is not None:
            suggested_products = suggested_products.filter(prix__lte=max_price)

        return suggested_products


auditlog.register(Products)
