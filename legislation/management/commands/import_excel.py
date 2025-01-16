from django.core.management.base import BaseCommand
import pandas as pd
from legislation.models import Category, Jurisdiction, Legislation

class Command(BaseCommand):
    help = 'Import legislation data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)

    def clean_text(self, text):
        """Clean text fields by removing extra whitespace and newlines"""
        if pd.isna(text):
            return ''
        return str(text).strip().replace('\r\n', ' ').replace('\n', ' ')

    def handle(self, *args, **options):
        self.stdout.write('Starting import...')
        
        try:
            # Read Excel file
            df = pd.read_excel(options['excel_file'])
            
            # Counter for tracking
            created_count = 0
            error_count = 0
            
            # Process each row
            for index, row in df.iterrows():
                try:
                    # Skip if essential fields are missing
                    if pd.isna(row['Category']) or pd.isna(row['Obligation']):
                        continue
                    
                    # Process category
                    category_parts = str(row['Category']).split(' - ', 1)
                    if len(category_parts) == 2:
                        category_code, category_name = category_parts
                    else:
                        category_code = category_parts[0]
                        category_name = category_parts[0]
                    
                    category, _ = Category.objects.get_or_create(
                        code=category_code.strip(),
                        defaults={'name': category_name.strip()}
                    )
                    
                    # Process jurisdiction - standardize to uppercase
                    jurisdiction_code = str(row['Jurisdiction']).strip().upper()
                    jurisdiction, _ = Jurisdiction.objects.get_or_create(
                        code=jurisdiction_code,
                        defaults={'name': self.get_jurisdiction_full_name(jurisdiction_code)}
                    )
                    
                    # Create or update legislation
                    legislation, created = Legislation.objects.update_or_create(
                        title=self.clean_text(row['Obligation']),
                        jurisdiction=jurisdiction,
                        defaults={
                            'description': self.clean_text(row['Description']),
                            'tier': str(row['Tier']),
                            'category': category,
                            'compliance_owner': self.clean_text(row['Compliance Owner']),
                            'business_owner': self.clean_text(row['Process / Business Owner']),
                            'admin_department': self.clean_text(row['Administering department']),
                            'administering_body': self.clean_text(row['pe'])
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f'Created: {legislation.title}')
                    else:
                        self.stdout.write(f'Updated: {legislation.title}')
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Error processing row {index + 2}: {str(e)}'
                        )
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed successfully:\n'
                    f'Created: {created_count} entries\n'
                    f'Errors: {error_count} entries'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to import data: {str(e)}'
                )
            )

    def get_jurisdiction_full_name(self, code):
        """Map jurisdiction codes to full names"""
        jurisdiction_map = {
            'TAS': 'Tasmania',
            'CTH': 'Commonwealth',
            'NSW': 'New South Wales',
            'VIC': 'Victoria',
            'INT': 'International'
        }
        return jurisdiction_map.get(code, code)