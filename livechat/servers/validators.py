from django.core.exceptions import ValidationError
import os

def validate_icon_for_channel(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg','.png','.webp','.jpeg']

    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported File extension. Allowed extension : " +str(valid_extensions))