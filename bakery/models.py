from django.db import models
from PIL import Image
import os


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='ชื่อสินค้า')
    price = models.PositiveIntegerField(verbose_name='ราคา (บาท)')
    description = models.TextField(blank=True, verbose_name='รายละเอียด')
    image = models.ImageField(upload_to='products/', verbose_name='รูปภาพ')
    is_available = models.BooleanField(default=True, verbose_name='เปิดขาย')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'สินค้า'
        verbose_name_plural = 'สินค้าทั้งหมด'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Compress รูปหลัง save
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            # แปลงเป็น RGB ถ้าเป็น RGBA/PNG
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            # ย่อขนาดถ้ากว้างเกิน 1200px
            if img.width > 1200:
                ratio = 1200 / img.width
                new_size = (1200, int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            # บันทึกกลับด้วย quality 80
            img.save(img_path, 'JPEG', quality=80, optimize=True)
