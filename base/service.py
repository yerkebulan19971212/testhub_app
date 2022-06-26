from PIL import Image
from rest_framework.exceptions import ValidationError


def validate_mb_image(value):
    size = value.size
    size_limit = 2.0
    if size > size_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный обьем фотографий {size_limit} MB")


def validate_size_image(value, width=500, height=500):
    wi, hei = Image.open(value).size
    if wi > width or hei > height:
        raise ValidationError("Размер фотографий должно быть не больше 500x500")
