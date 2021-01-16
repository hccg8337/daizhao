from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    name = models.CharField(null=False, blank=False, max_length=1024, verbose_name='名称')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    tags = ArrayField(
        models.CharField(max_length=64, null=False, blank=False),
        default=list, null=False, verbose_name='标签',
    )
    img = models.ImageField(null=False, upload_to='uploads/%Y/%m/%d/', verbose_name='缩略图')
    url = models.URLField(null=False, max_length=1024, verbose_name='链接')
    uv = models.BigIntegerField(null=False, default=0)
    priority = models.IntegerField(default=0, null=False, verbose_name='优先级')
    is_active = models.BooleanField(default=True, null=False, verbose_name='是否启用')

    class Meta:
        ordering = ['-is_active', '-priority', '-uv', '-updated_at']

    def __str__(self):
        return self.name
