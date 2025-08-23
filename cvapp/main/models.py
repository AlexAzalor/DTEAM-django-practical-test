from django.db import models

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.id})"

class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=False, blank=False)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

class CV(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    role = models.CharField(max_length=64)
    skills = models.ManyToManyField(Skill, related_name="cvs")
    projects = models.ManyToManyField(Project, related_name="cvs")
    bio = models.TextField(null=False, blank=False)
    contacts = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"
