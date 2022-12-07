import subprocess

model_name = 'v1-5-pruned-emaonly.ckpt'
s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!


# assert model_name.isalnum() and model_name.endswith(".ckpt")
# assert s3_bucket_name.isalnum() and s3_bucket_name.endswith("-sd")
# print('xss checks done')

script_args = ''\
  ' --skip_grid ' \
  ' --ddim_steps 30 '\
  ' --H 320 '\
  ' --W 576 '\
  ' --n_samples 1 '\
  ' --n_iter 1 '\
  ' --scale 7.5 '\
  ' --from-file /var/meadowrun/machine_cache/prompts.txt '\
 f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
  ' --seed 1337 '\
  ' --precision autocast '\
  ' --outdir /tmp/outputs '

# run python scripts/txt2img.py to create images from text files
subprocess.call(['python', f'../scripts/txt2img.py {script_args}'])

