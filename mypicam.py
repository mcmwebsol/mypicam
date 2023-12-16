from time import sleep
from picamera import PiCamera
import datetime as dt
import os as os
import requests
import json
from base64 import b64encode

camera = PiCamera()
camera.resolution = (800, 600)
#camera.start_preview()
# Camera warm-up time
sleep(2)

myDateTime = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
filename = 'capture_'+myDateTime+'.jpg'
filenameWPath = '/enter/full/path/here/'+filename  # TODO - ENTER FULL PATH HERE
camera.capture(filenameWPath)

# use WP REST API to upload file (need to change directory though to secured one? - TODO!)
user = 'USER' # TODO - ENTER USERNAME FOR WP REST API HERE
pythonapp = 'ENTER WP REST API KEY HERE' # TODO - ENTER WP REST API KEY (APPLICATION PASSWORD) HERE
#token = base64.standard_b64encode(user + ':' + pythonapp)
token = b64encode('{}:{}'.format(user,pythonapp))
headers = {'Authorization': 'Basic ' + token}

url = 'https://my-wp-website-here.com/wp-json/wp/v2/media/'; # TODO - replace my-wp-website-here.com with your website URL

data = open(filenameWPath, 'rb').read()
fileName = os.path.basename(filenameWPath)
res = requests.post(url=url,
                    data=data,
                    headers={ 'Content-Type': 'image/jpg','Content-Disposition' : 'attachment; filename=%s'% fileName},
                    auth=(user, pythonapp))
#print(res.json()) # debug - response from WP as JSON
newDict=res.json()
newID= newDict.get('id')
link = newDict.get('guid').get("rendered")
print newID, link

os.remove(filenameWPath) # DELETE THE FILE
