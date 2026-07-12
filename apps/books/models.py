from django.db import models


# class TimeStampedModel(models.Model):
#     __abstract__ = True
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#class Author(models.Model, TimeStampedModel):
class Author(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return self.full_name

#class Book(models.Model, TimeStampedModel):
class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Books's title", help_text='Введите полное название')    # VARCHAR(100)
    author = models.CharField(max_length=100, verbose_name="Author(s)")   # VARCHAR(100)
    published_date = models.DateField(verbose_name="Date of publish")         # DATE
    count = models.IntegerField(verbose_name="Book's count")





    def __repr__(self):
        return self.title

    def __str__(self):
        return f'{self.title}: {self.author}: {self.published_date}'


