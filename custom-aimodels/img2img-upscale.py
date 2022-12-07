import subprocess
import sys

model_name = sys.argv[1]
s3_bucket_name = sys.argv[2]

# get the line from prompts.txt that corresponds to the current filename
script_args = ' --skip_grid ' \
'  --ddim_steps 400 '\
'  --n_samples 1 '\
'  --n_iter 1 '\
'  --scale 8 '\
'  --strength 0.45 '\
f' --from-folder /tmp/samples_resized/ '\
f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
'  --seed 1330 '\
'  --precision autocast '\
'  --outdir /tmp/img2img '

subprocess.check_output('python scripts/img2img.py ' + script_args, shell=True).decode('utf-8')
