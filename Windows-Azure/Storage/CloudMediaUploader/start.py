from AzureImpl import AzureImpl
from ConfigService import ConfigService

config = ConfigService()
config.loadConfig()
config.whatsInside()

azure = AzureImpl(config.AccountName, config.AccountKey, config)

#get the media file that needs to be uploaded
file = "c:\\temp\\video\\wildlife.mp4"
azure.addMonitoringData(file, 2)




