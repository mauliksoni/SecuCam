from AzureImpl import AzureImpl
from ConfigService import ConfigService

config = ConfigService()
config.loadConfig()
config.whatsInside()

azure = AzureImpl(config.AccountName, config.AccountKey)




