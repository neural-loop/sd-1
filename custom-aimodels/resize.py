from PIL import Image
import os

# for each image in /tmp/outputs/samples resize image to 1152x640 and save to /tmp/outputs/samples_resized
for filename in os.listdir("/tmp/outputs/samples"):
    if filename.endswith(".png"):
        im = Image.open("/tmp/outputs/samples/" + filename)
        imResize = im.resize((1024,576), Image.ANTIALIAS)
        # if samples_resized folder does not exist, create it
        if not os.path.exists("/tmp/outputs/samples_resized"):
            os.makedirs("/tmp/outputs/samples_resized")
        imResize.save("/tmp/outputs/samples_resized/" + filename, 'PNG', quality=90)
