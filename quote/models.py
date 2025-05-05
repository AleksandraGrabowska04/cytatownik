from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Quote(models.Model):
    author = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    @property
    def vote_counts(self):
        return {
            vote_type.label: self.votes.filter(typ=vote_type).count()
            for vote_type in VoteType
        }

    def __str__(self):
        return f"{self.author}: {self.text[:30]}..."

class Comment(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.content[:30]}"

class VoteType(models.TextChoices):
    HEART = 'HR', _('Heart')
    CURIOUS = 'CR', _('Curious')
    SKULL = 'SK', _('Skull')

class Vote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typ = models.CharField(max_length=2, choices=VoteType.choices, default=VoteType.HEART)
    class Meta:
        unique_together = ('quote', 'user')

    def __str__(self):
        return f"{self.user.username} {self.typ} - Quote Author: {self.quote.author}"