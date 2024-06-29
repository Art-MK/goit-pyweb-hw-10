from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=255, default='Unknown Author')
    born_date = models.CharField(max_length=255, blank=True, null=True)
    born_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    tags = models.JSONField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField()  # Изменено на 'text'

    def __str__(self):
        return self.text
