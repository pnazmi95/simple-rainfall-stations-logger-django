from django.db import models
from jalali_date import date2jalali


class Station(models.Model):
    class Meta:
        verbose_name = 'ایستگاه'
        verbose_name_plural = 'ایستگاه ها'

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام ایستگاه')

    def __str__(self):
        return f"{self.name}"


class Rainfall(models.Model):
    class Meta:
        verbose_name = 'بارندگی'
        verbose_name_plural = 'بارندگی ها'
    station = models.ForeignKey('Station', on_delete=models.CASCADE, verbose_name="نام ایستگاه")
    value = models.IntegerField(blank=True, null=True, verbose_name="مقدار بارش (به میلی متر )")
    submit_date = models.DateField(verbose_name='تاریخ')

    def __str__(self):
        return f"The rainfall value for {self.station} station in {self.submit_date} is : {self.value}"

    def get_jalali_date(self):
        return date2jalali(self.submit_date)

    def average(self):
        text = ''
        for station in Station.objects.all():
            avg = 0
            sum = 0
            counter = 0
            for rainfall in Rainfall.objects.all():
                if rainfall.station.id == station.id:
                    sum += rainfall.value
                    counter += 1
            if counter != 0:
                avg = sum / counter
            text += str(avg) + ","
        return text



