from django.db import models

# Create your models here.

class IntrisicData(models.Model):
    tickerName = models.CharField(max_length=256)
    intrinsicValue = models.FloatField()
    marketValue = models.FloatField()
    PercentageIncreament = models.FloatField(blank=False,null=True)
    val_date_price = models.FloatField(blank=False,null=True)

    def __str__(self):
        return self.tickerName