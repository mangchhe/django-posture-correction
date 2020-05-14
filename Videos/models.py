from django.db import models

# Create your models here.

class VideosDB(models.Model):

    #objects = models.Manager()
    video_id = models.CharField(max_length=10,primary_key=True) # 비디오 id
    title = models.TextField(blank=False) # 제목
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="") #video file
    video_img = models.ImageField(upload_to="") # 영상이미지
    views = models.IntegerField(default=0) # 조회수
    level = models.CharField(max_length=5) # 난이도
    start_date = models.DateTimeField(auto_now_add=True) # 개시일

    def __str__(self):
        return self.video_id + ": " + self.title + ": " + str(self.videofile)