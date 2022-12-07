import subprocess

model_name = 'v1-5-pruned-emaonly.ckpt'
s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!

# check variables for alphanumeric with dashes and underscores and periods
assert all(c.isalnum() or c in ['-', '_', '.'] for c in model_name)


script_args = ' --skip_grid ' \
  ' --ddim_steps 30 '\
  ' --H 320 '\
  ' --W 576 '\
  ' --n_samples 1 '\
  ' --n_iter 1 '\
  ' --scale 8 '\
  ' --from-file custom-aimodels/prompts.txt '\
 f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
  ' --seed 1331 '\
  ' --precision autocast '\
  ' --outdir /tmp/outputs '

subprocess.check_output('python scripts/txt2img.py ' + script_args, shell=True).decode('utf-8')

