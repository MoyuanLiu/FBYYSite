from django.db import models

# Create your models here.
class TbCts(models.Model):
    idtb_cts = models.AutoField(primary_key=True)
    tb_cts_product_num = models.CharField(max_length=100)
    tb_cts_cal_date = models.CharField(max_length=45)
    tb_cts_sell_count = models.IntegerField()
    tb_cts_cal_depart = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tb_cts'