from django.db import models

# Create your models here.


class DemoModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()    



class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    published_date = models.DateField()

    def __str__(self):
        return self.title
    

