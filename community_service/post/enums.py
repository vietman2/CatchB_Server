from django.db import models

class ForumChoices(models.IntegerChoices):
    DUGOUT  = 1, "덕아웃"
    RECRUIT = 2, "드래프트"
    MARKET  = 3, "장터"
    STEAL   = 4, "스틸"
