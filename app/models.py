from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, Avg

User = get_user_model()


class Content(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    user_scores = models.ManyToManyField(User, through='UserScoreContent')

    @property
    def scores_stat(self):
        stat = self.user_score_contents.aggregate(
            sum_scores=Sum('score'),
            mean_scores=Avg('score')
        )
        return {
            "sum_scores": stat["sum_scores"],
            "mean_scores": stat["mean_scores"]
        }


class UserScoreContent(models.Model):
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='user_score_contents', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])

    class Meta:
        unique_together = ["user", "content"]
