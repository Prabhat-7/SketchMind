
from django.db import models

class EquationSolution(models.Model):
    equation = models.CharField(max_length=255)
    solution = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equation} = {self.solution}"
