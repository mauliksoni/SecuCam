__author__ = 'Kedar Subramanya'
import time
from datetime import datetime
from azure.storage import TableService
from azure.storage import BlobService
import uuid

class AzureImpl(object):
    def __init__(self,config):
        self.AccountName = config.AccountName
        self.AccountKey = config.AccountKey
        self.deviceId = config.DeviceId
        self.deviceDescription = config.DeviceDescription
        self.macAddress = config.MacAddress
        self.username = config.UserName
        self.email = config.Email
        #self.tableService = TableService("kkpicam", "R2K8UWnE9mWqnWIScuLHMNaXQR1W7KUE9bTDxIza/X94K+x2+EtouAVE9V8BmUaaK3HQQMZLY5MGcvkzuMTmCA==")
        self.tableService = TableService(self.AccountName, self.AccountKey)
        self.tableService.create_table('monitoring')

        self.blob_service = BlobService(self.AccountName, self.AccountKey)
        self.blob_service.create_container('images')
        self.blob_service.create_container('videos')

    def checkIfAccountExists(self):
        """check if account exists in azure"""
        return False

    def addMonitoringData(self, mediaPath, mediaType):
        currentDate = datetime.today()
        currentDateTime = datetime.now()
        partitionKey = "{0}-{1}-{2}".format(currentDate.year, currentDate.month, currentDate.isocalendar()[1])
        rowKey = "{0}".format(uuid.uuid1())
        blobId = "{0}".format(uuid.uuid1())

        # first insert the blob
        self.blob_service.put_block_blob_from_path('videos', '{0}.h264'.format(blobId), mediaPath)

        # now insert the monitoring data
        self.tableService.insert_entity(
         'monitoring',
         {
            'PartitionKey' : partitionKey,
            'RowKey': rowKey,
            "macAddress":self.macAddress,
            "deviceid":self.deviceId,
            "devicedescriptoin":self.deviceDescription,
            "username":self.username,
            "blobid":blobId,
            "mediatype": mediaType,
            "timestamp":currentDateTime,
        }
    )





