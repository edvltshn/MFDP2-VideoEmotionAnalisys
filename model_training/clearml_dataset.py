import os
from clearml import StorageManager, Dataset


os.environ['CLEARML_WEB_HOST'] = 'https://app.clear.ml'
os.environ['CLEARML_API_HOST'] = 'https://api.clear.ml'
os.environ['CLEARML_FILES_HOST'] = 'https://files.clear.ml'
os.environ['CLEARML_API_ACCESS_KEY'] = 'insert_access_key'
os.environ['CLEARML_API_SECRET_KEY'] = 'insert_secret_key'


# Create a dataset with ClearML`s Dataset class
dataset = Dataset.create(
    dataset_project="MyFirstDataProject", dataset_name="Augmented_dataset"
)

# add the dataset folder
dataset.add_files(path='./dataset')

# Upload dataset to ClearML server (customizable)
dataset.upload()

# commit dataset changes
dataset.finalize()