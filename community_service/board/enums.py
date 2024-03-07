from django.db import models

class ForumChoices(models.IntegerChoices):
    DUGOUT  = 1, "덕아웃"
    RECRUIT = 2, "모집"
    MARKET  = 3, "장터"
