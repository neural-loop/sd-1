import subprocess
import os

model_name = 'v1-5-pruned-emaonly.ckpt'
s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!

# check variables for alphanumeric with dashes and underscores and periods
assert all(c.isalnum() or c in ['-', '_', '.'] for c in model_name)

i = 0

# get the line from prompts.txt that corresponds to the current filename
script_args = ' --skip_grid ' \
'  --ddim_steps 90 '\
f' --init-img /tmp/samples_resized/{filename} '\
'  --n_samples 1 '\
'  --n_iter 1 '\
'  --scale 15 '\
'  --strength 0.55 '\
f' --from-folder /tmp/samples_resized/ '\
f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
'  --seed 13371 '\
'  --precision autocast '\
'  --outdir /tmp/img2img '
i = i+1

subprocess.check_output('python scripts/img2img.py ' + script_args, shell=True).decode('utf-8')

