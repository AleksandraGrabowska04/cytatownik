import csv
from django.core.management.base import BaseCommand
from quote.models import Quote
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Importuje cytaty z pliku CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ścieżka do pliku CSV')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        user = User.objects.first()  # domyślnie przypisz pierwszy dostępny user

        if not user:
            self.stdout.write(self.style.ERROR("Brak użytkownika – stwórz najpierw użytkownika.")) 
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            imported = 0

            for row in reader:
                Quote.objects.create(
                    author=row['author'],
                    text=row['text'],
                    category=row['category'],
                    user=user
                )
                imported += 1

        self.stdout.write(self.style.SUCCESS(f'Sukces! Zaimportowano {imported} cytatów.'))
