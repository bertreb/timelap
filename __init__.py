import os
import imageio
import urllib.request
import time
import datetime
import shutil

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "timelap"

def setup(hass: HomeAssistant, config: ConfigType) -> bool:

    def make_timelap(call):

        snapshots_folder = "/"+call.data.get("snapshot_folder", 0).strip("/")+"/"
        timelap_folder = "/"+call.data.get("timelap_folder", 0).strip("/")+"/"
        camera_url = call.data.get("camera_url", 0)
        duration = int(call.data.get("duration", 0))

        # delete the snapshot directory
        if os.path.exists(snapshots_folder):
            shutil.rmtree(snapshots_folder, ignore_errors=False, onerror=None)

        # create the snapshot directory
        os.mkdir(snapshots_folder)

        # if timelapfolder doesn't exist create the timelap directory
        if !os.path.exists(timelap_folder):
            os.mkdir(timelap_folder)


        #get camera images and save them in the snapshot directory
        for x in range(duration):
            now =datetime.datetime.now()
            timestamp = now.strftime("%y%m%d_%H%M%S")
            urllib.request.urlretrieve(camera_url, snapshots_folder+timestamp+".jpg")
            time.sleep(1)

        #collect the jpg's
        images = []
        for file_name in sorted(os.listdir(snapshots_folder)):
            if file_name.endswith('.jpg'):
                file_path = os.path.join(snapshots_folder, file_name)
                images.append(imageio.v2.imread(file_path))

        # merge to a gif
        now =datetime.datetime.now()
        timestamp = now.strftime("%y%m%d_%H%M%S")
        imageio.mimsave(timelap_folder+timestamp+"_timelap.gif", images, fps = 1)

    hass.services.register(DOMAIN, "make_timelap", make_timelap)

    return True
