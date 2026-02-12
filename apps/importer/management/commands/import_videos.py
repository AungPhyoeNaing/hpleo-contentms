from django.core.management.base import BaseCommand
import asyncio
from apps.importer.services import CaobizyImporter

class Command(BaseCommand):
    help = 'Imports videos from Caobizy API'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=1, help='Number of pages to import')
        parser.add_argument('--url', type=str, default="https://www.caobizy.com/api.php/provide/vod/", help='API URL')

    def handle(self, *args, **options):
        pages = options['pages']
        url = options['url']
        
        self.stdout.write(f"Starting import from {url} for {pages} pages...")
        
        importer = CaobizyImporter(api_url=url)
        
        try:
            # Run async function in sync command
            log = asyncio.run(importer.run_import(pages=pages))
            
            self.stdout.write(self.style.SUCCESS(
                f"Import finished. Status: {log.status}. Success: {log.success_count}, Fail: {log.fail_count}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Import failed: {e}"))
