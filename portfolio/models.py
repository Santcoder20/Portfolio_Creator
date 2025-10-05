from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    video = models.FileField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User


class Education(models.Model):
    CGPA = 'CGPA'
    PERCENTAGE = 'Percentage'
    SCORE_TYPE_CHOICES = [
        (CGPA, 'CGPA'),
        (PERCENTAGE, 'Percentage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)

    score_type = models.CharField(
        max_length=20,
        choices=SCORE_TYPE_CHOICES,
        default=CGPA  # default set to CGPA
    )
    score = models.FloatField(blank=True, null=True)  # stores either CGPA or Percentage

    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    def display_score(self):
        if self.score_type == self.CGPA:
            return f"CGPA: {self.score}"
        elif self.score_type == self.PERCENTAGE:
            return f"Percentage: {self.score}%"
        return ""


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} @ {self.company}"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    certificate_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return self.title

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_link = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume - {self.user.username}"

class BackGround(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_file = models.FileField(upload_to='backgrounds/',blank= True, null=True)
    sidebar_file = models.FileField(upload_to='backgrounds/',blank=True, null=True)