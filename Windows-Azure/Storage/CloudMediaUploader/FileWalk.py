import os,time
from AzureImpl import AzureImpl
from ConfigService import ConfigService
from subprocess import call

path_to_watch='/home/pi/PiCam/upload'


while 1:
    time.sleep(5)
    for filenames in os.walk(path_to_watch):
        for f in filenames:
            for file in f:
                if '.h264' in file:
                    fullfilepath=path_to_watch+'/'+file
                    print fullfilepath

                    #convert file to Mp4 before upload
                    command = 'MP4Box -add ' + fullfilepath + ' ' + fullfilepath.replace('h264','mp4')
                    print 'converting to mp4 ' + command
                    call (command,shell=True)
		    os.remove(fullfilepath)

    for filenames in os.walk(path_to_watch):
	    for file in f:	
		if '.mp4' in file: 
		    fullfilepath=path_to_watch+'/'+file                  
                    config = ConfigService()
                    config.loadConfig()
                    # call azure service to upload the data to the cloud
                    # 2 denotes the the uploaded file type is video. 1 is for images
                    azure = AzureImpl(config)
                    azure.addMonitoringData(fullfilepath, 2)
                    print 'file uploaded-' + fullfilepath

                    #after uploading the data to the cloud, we delete the file
                    os.remove(fullfilepath)
                    print 'file removed-' + fullfilepath 

    
