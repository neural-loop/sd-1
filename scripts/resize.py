from PIL import Image
import os, sys

# for each image in /tmp/outputs/samples resize image to 1152x640 and save to /tmp/outputs/samples_resized
for filename in os.listdir("/tmp/outputs/samples"):
    if filename.endswith(".png"):
        im = Image.open("/tmp/outputs/samples/" + filename)
        imResize = im.resize((1024,576), Image.ANTIALIAS)
        imResize.save("/tmp/outputs/samples_resized/" + filename, 'PNG', quality=90)


# // upload resized images to s3
# os.system("aws s3 sync /tmp/outputs/samples_resized s3://visioninit-sd/1920x1080/")
