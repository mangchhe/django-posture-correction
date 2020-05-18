from django.db import models

# Create your models here.

class EdusDB(models.Model): # 학습 디비 클래스

    NON_SHARED = "공유 안함"
    SHARED = "공유 함"

    IS_SHARED = (
        (NON_SHARED , "공유 안함"),
        (SHARED, "공유 함"),
    )

    objects = models.Manager()
    video_description = models.TextField(blank=False)
    views = models.PositiveIntegerField(default=0)
    is_shared = models.CharField(choices=IS_SHARED, max_length=5, default=NON_SHARED)
    edu_days = models.DateTimeField(auto_now_add=True)                  # 학습일, auto_now_add : insert 시에만 현재 날짜로 갱신됨
    video_id = models.ForeignKey("Videos.VideosDB", on_delete = models.CASCADE)  # 영상 번호, models.CASCADE : 주키 삭제 시 외래키 같이 삭제(연쇄 삭제)
    user_id = models.ForeignKey("Users.UsersDB", on_delete = models.CASCADE)    # 사용자 번호
    recode_video = models.FileField(upload_to='edus/', null=True, verbose_name="")     # 녹화 영상, upload_to : 파일 저장 경로 지정
    score = models.IntegerField(default=0)                              # 점수, default = 기본 값