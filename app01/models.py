from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name=models.CharField(verbose_name="用户名称",max_length=32)
    def __str__(self):
        return self.name
class UserType(models.Model):
    name=models.CharField(verbose_name="类型名称",max_length=32)
    def __str__(self):
        return self.name
class Role(models.Model):
    xxx=models.CharField(verbose_name="角色名称",max_length=32)
    def __str__(self):
        return self.xxx

class Host(models.Model):
    ip=models.GenericIPAddressField(verbose_name="IP",protocol='ipv4')
    hostname=models.CharField(verbose_name='主机名',max_length=32)
    port=models.IntegerField(verbose_name='端口')