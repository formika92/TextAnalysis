from django.db import (
    models,
)
from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import (
    receiver,
)


class TextFiles(models.Model):
    """
    Модель для хранения ссылки на файлы
    """
    file = models.FileField(
        upload_to='media',
        null=False,
        max_length=255,
        blank=False,
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        blank=False,
    )

    class Meta:
        verbose_name_plural = 'TextFiles'

    def __str__(self):
        if '/' in self.file.name:
            file_name = self.file.name.partition('/')[-1]
        else:
            file_name = self.file.name
        return file_name


@receiver(pre_delete, sender=TextFiles)
def delete_image(sender, instance, **kwargs):
    """
    Удаляет файл при удалении объекта
    """
    if instance.file:
        instance.file.delete(False)
