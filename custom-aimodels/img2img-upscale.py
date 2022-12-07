import subprocess

model_name = 'v1-5-pruned-emaonly.ckpt'
s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!

# check variables for alphanumeric with dashes and underscores and periods
assert all(c.isalnum() or c in ['-', '_', '.'] for c in model_name)

# put each filename from /tmp/outputs/samples_resized/ into array
filenames = subprocess.check_output('ls -1 /tmp/samples_resized/samples/', shell=True).decode('utf-8').splitlines()
print(filenames)
# iterate through filenames with counter
for i, filename in enumerate(filenames):
  # get the line from prompts.txt that corresponds to the current filename
  prompt = subprocess.check_output(f'head -n {i+1} /var/meadowrun/machine_cache/prompts.txt | tail -n 1', shell=True).decode('utf-8')
  script_args = ' --skip_grid ' \
    ' --ddim_steps 90 '\
   f' --init-img /tmp/samples_resized/samples/{filename} '\
    ' --n_samples 1 '\
    ' --n_iter 1 '\
    ' --scale 7.5 '\
    ' --strength 0.55 '\
   f' --prompt \'{prompt}\' '\
   f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
    ' --seed 1337 '\
    ' --precision autocast '\
    ' --outdir /tmp/outputs/img2img '

subprocess.check_output('python scripts/img2img.py ' + script_args, shell=True).decode('utf-8')

