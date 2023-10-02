from django.db import models

class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user_id_pk = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ['-upload_date']

class Image(Media):
    image_file = models.ImageField(upload_to='images/')

    class Meta:
        db_table = "image"
        db_table_comment = "Table for storing images. 이미지 저장을 위한 테이블입니다."
        # constraints = () 추후에, 용량 제한을 위한 제약조건 추가

class Video(Media):
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True)
    # duration = models.DurationField()

    class Meta:
        db_table = "video"
        db_table_comment = "Table for storing videos. 비디오 저장을 위한 테이블입니다."
        # constraints = () 추후에, 용량 제한이나 길이 제한을 위한 제약조건 추가
