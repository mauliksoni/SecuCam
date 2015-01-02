__author__ = 'Kedar Subramanya'
__author__ = 'Maulik Soni'
import time
from datetime import datetime
from azure.storage import TableService
from azure.storage import BlobService
import uuid
import requests
import traceback
import json

url = 'https://sccam.azure-mobile.net/tables/TodoItem'
headers = {'Content-Type':'application/json','X-ZUMO-APPLICATION': ''}

class AzureImpl(object):
    def __init__(self, config):
        self.AccountName = config.AccountName
        self.AccountKey = config.AccountKey
        self.deviceId = config.DeviceId
        self.deviceDescription = config.DeviceDescription
        self.macAddress = config.MacAddress
        self.username = config.UserName
        self.email = config.Email
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

        # first insert
        # now insert the monitoring data to azure mobile services table
        p='https://sccam.blob.core.windows.net/videos/' + blobId + '.mp4'
        print p
        print url
        payload = {'text': str(p),'complete': False }
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            print r.text
            #print 'post'
        except Exception:
            print ('Error posting data')
            #print traceback.format_exc()
            pass
        
    #self.blob_service.set_blob_properties('videos','{0}.mp4',)
        self.blob_service.put_block_blob_from_path('videos', '{0}.mp4'.format(blobId), mediaPath,x_ms_blob_content_type='video/mp4')
