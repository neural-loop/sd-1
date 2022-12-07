import subprocess
import sys

model_name = sys.argv[1]
s3_bucket_name = sys.argv[2]

script_args = ' --skip_grid ' \
  ' --ddim_steps 30 '\
  ' --H 320 '\
  ' --W 576 '\
  ' --n_samples 1 '\
  ' --n_iter 1 '\
  ' --scale 8 '\
  ' --from-file custom-aimodels/prompts.txt '\
 f' --ckpt /var/meadowrun/machine_cache/{model_name} '\
  ' --seed 1330 '\
  ' --precision autocast '\
  ' --outdir /tmp/outputs '

subprocess.check_output('python scripts/txt2img.py ' + script_args, shell=True).decode('utf-8')

