from django.core.management.base import BaseCommand
from blog.models import BlogCategory


class Command(BaseCommand):
    help = 'Load predefined blog categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Mental Health', 'description': 'Articles about mental health and wellness'},
            {'name': 'Heart Disease', 'description': 'Information about cardiovascular health'},
            {'name': 'COVID-19', 'description': 'Updates and information about COVID-19'},
            {'name': 'Immunization', 'description': 'Vaccination and immunization information'},
        ]

        for cat_data in categories:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all categories'))
