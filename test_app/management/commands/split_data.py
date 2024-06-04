# test_app/management/commands/split_data.py

import pandas as pd
import math
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Split data from Excel file into multiple CSV files'

    def handle(self, *args, **kwargs):
        data_frame = pd.read_excel("/Users/v2113269/Downloads/Keyword__Acronym and Abbreviation_20190805.xlsx")
        num_files = math.ceil(len(data_frame) / 5)

        directory = '/Users/v2113269/Desktop/quick_test_app/test_data/'
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                os.remove(os.path.join(directory, filename))

        for i in range(num_files):
            start_index = i * 5
            end_index = min((i + 1) * 5, len(data_frame))
            subset_data_frame = data_frame[start_index:end_index]
            new_data_frame = pd.DataFrame()
            new_data_frame['Question'] = 'What is ' + subset_data_frame['Acronym'] + '?'
            new_data_frame['Answer'] = subset_data_frame['Full Form']
            file_name = f'/Users/v2113269/Desktop/quick_test_app/test_data/file{i + 1}.csv'
            new_data_frame.to_csv(file_name, index=False)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {file_name}'))
