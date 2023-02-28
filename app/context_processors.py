from .models import Category


def extra_categories(request):
    print(request)
    categories = Category.objects.all()
    return {"categories": categories}

#tesseract OCR




