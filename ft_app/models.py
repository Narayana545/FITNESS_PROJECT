from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Goal(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    target_value = models.IntegerField()
    current_value = models.IntegerField(default=0)
    achieved = models.BooleanField(default=False)
    date_set = models.DateTimeField(auto_now_add=True)
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return (self.current_value / self.target_value) * 100  # Calculate progress as a percentage

    def __str__(self):
        return f'{self.user.username} - {self.goal_name}'

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    value = models.IntegerField()
    date_achieved = models.DateTimeField(auto_now_add=True)

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_achievements = models.IntegerField(default=0)

