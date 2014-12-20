from AzureImpl import AzureImpl
from ConfigService import ConfigService

config = ConfigService()
config.loadConfig()
config.whatsInside()

azure = AzureImpl(config)

#get the media file that needs to be uploaded
file = "c:\\temp\\video\\1.mp4"
azure.addMonitoringData(file, 2)




