from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# models.Model 대신 AbstractUser 사용
class UsersDB(AbstractUser): # AbstractUser에 name, password, email 필드가 존재, 따로 만들 필요 없음, 이거 이용해서 구현하면 됨
    #user_id = models.CharField(max_length = 50, primary_key=True) # 사용자 ID
    #user_password = models.CharField(max_length = 50) # 사용자 비밀번호
    #user_name = models.CharField(max_length = 50) # 사용자 이름
    user_birth = models.DateField(null=True) # 생년월일

    def __str__(self):
        return self.username

