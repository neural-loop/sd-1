import subprocess
import os

model_name = 'v1-5-pruned-emaonly.ckpt'
s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!

# check variables for alphanumeric with dashes and underscores and periods
assert all(c.isalnum() or c in ['-', '_', '.'] for c in model_name)

i = 0

for filename in os.listdir("/tmp/samples_resized"):
  # get the line from prompts.txt that corresponds to the current filename
  prompt = subprocess.check_output(f'head -n {i+1} /var/meadowrun/machine_cache/prompts.txt | tail -n 1', shell=True).decode('utf-8')
  script_args = ' --skip_grid ' \
  '  --ddim_steps 90 '\
  f' --init-img /tmp/samples_resized/{filename} '\
  '  --n_samples 1 '\
  '  --n_iter 1 '\
  '  --scale 7.5 '\
  '  --strength 0.55 '\
  f' --prompt \'{prompt}\' '\
  f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
  '  --seed 1337 '\
  '  --precision autocast '\
  '  --outdir /tmp/img2img '
  i = i+1

subprocess.check_output('python scripts/img2img.py ' + script_args, shell=True).decode('utf-8')

