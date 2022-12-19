# if s3_bucket_name is not set, then set it to the default value
if [ -z "$s3_bucket_name" ]; then
  aws s3 sync s3://{s3_bucket_name} /var/meadowrun/machine_cache
        --exclude "*"
        --include {model_name}
         --include prompts.txt
fi
python custom-aimodels/createimage-small.py {model_name}
python custom-aimodels/resize.py
python custom-aimodels/img2img-upscale.py {model_name}
if [ -z "$s3_bucket_name" ]; then
  aws s3 sync /tmp/ s3://{s3_bucket_name}/img/{model_name}/
fi
