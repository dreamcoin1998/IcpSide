"""
访问日志models

Creator: Gao Junbin
Update: 2021-07-01
"""

from django.db import models
from auth_user.models import User


class AccessLog(models.Model):

    ip = models.CharField(max_length=50, verbose_name="IP")
    url = models.CharField(max_length=256, verbose_name="访问地址")
    datetime = models.DateTimeField(verbose_name="访问日期", auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True)

    @property
    def username(self):
        """获取访问日志关联的username"""
        if self.user:
            return self.user.username
        else:
            return "未登录用户"

    class Meta:
        verbose_name = "访问日志"
        verbose_name_plural = verbose_name
