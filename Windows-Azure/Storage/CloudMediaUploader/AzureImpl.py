__author__ = 'Kedar Subramanya'
from azure.storage import TableService
from datetime import datetime
ts = TableService("kkpicam", "")
ts.create_table('tasktable')
ts.insert_entity(
     'tasktable',
     {
        'PartitionKey' : 'tasksSeattle',
        'RowKey': '1',
        'Description': 'Take out the trash',
        'DueDate': datetime(2011, 12, 14, 12)
    }
)

class AzureImpl(object):
    def __init__(self, accountName, accountKey):
        self.AccountName = accountName
        self.AccountKey = accountKey
    def checkIfAccountExists(self):
        """check if account exists in azure"""
        return False

