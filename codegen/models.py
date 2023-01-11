from django.db import models
from django.contrib.auth.models import User

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tanya = models.TextField()
    jawab = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tanya
