from django.db import models

# Create your models here.

class VideosDB(models.Model):

    HIGH = "상"
    MIDDLE = "중"
    LOW = "하"

    LEVEL_CHOICES = (
        (HIGH, "상"),
        (MIDDLE, "중"),
        (LOW, "하"),
    )

    objects = models.Manager()
    #video_id = models.CharField(max_length=10,primary_key=True) # 비디오 id
    title = models.TextField(blank=False) # 제목
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="") #video file
    video_img = models.ImageField(upload_to="") # 영상이미지
    views = models.PositiveIntegerField(default=0) # 조회수 - PositiveIntegerField를 이용
    level = models.CharField(choices=LEVEL_CHOICES, max_length=5, default=LOW) # 난이도
    start_date = models.DateTimeField(auto_now_add=True) # 개시일

    def __str__(self):
        return self.title + ": " + str(self.videofile)