from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title
