import pyinotify
import os
from AzureImpl import AzureImpl
from ConfigService import ConfigService

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):

        #print "Creating:", event.pathname
        # load the configuration details
        config = ConfigService()
        config.loadConfig()

        # call azure service to upload the data to the cloud
        # 2 denotes the the uploaded file type is video. 1 is for images
        azure = AzureImpl(config)
        azure.addMonitoringData(event.pathname, 2)

        #after uploading the data to the cloud, we delete the file
        os.remove(event.pathname)

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home/pi/Desktop/dev/tmp', mask, rec=True)

notifier.loop()