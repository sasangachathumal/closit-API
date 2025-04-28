from database.init_db import create_database
from dataSets.init_dataset import create_dataset_csv_files

def initialize_application_data():
    create_database()
    create_dataset_csv_files()

