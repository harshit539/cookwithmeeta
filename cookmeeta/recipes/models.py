from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=300)
    video_id = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    thumbnail = models.URLField(blank=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title