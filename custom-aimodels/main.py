import asyncio
import sys

import meadowrun

# get command line argument as model_name default to v1-5-pruned-emaonly.ckpt
model_name = sys.argv[1] if len(sys.argv) > 1 else 'v1-5-pruned-emaonly.ckpt'
# get command line argument as bucket name default to visioninit-sd
s3_bucket_name = sys.argv[2] if len(sys.argv) > 2 else 'visioninit-sd'

def main():
    # check variables for alphanumeric with dashes and underscores and periods
    assert all(c.isalnum() or c in ['-', '_', '.'] for c in model_name)
    assert all(c.isalnum() or c in ['-', '_', '.'] for c in s3_bucket_name)

    asyncio.run(
        meadowrun.run_command(
            'bash -c \''
            f'aws s3 sync s3://{s3_bucket_name} /var/meadowrun/machine_cache '
            '       --exclude "*" '
            f'      --include {model_name} '
            '       --include prompts.txt '
            f'&&  python custom-aimodels/createimage-small.py {model_name}'
            '&&  python custom-aimodels/resize.py '
            f'&&  python custom-aimodels/img2img-upscale.py {model_name}'
            f'&& aws s3 sync /tmp/ s3://{s3_bucket_name}/img/{model_name}/'
            f'\'',
            meadowrun.AllocCloudInstance("EC2"),
            meadowrun.Resources(
                logical_cpu=1, memory_gb=8, max_eviction_rate=80, gpu_memory=16, flags="nvidia"
            ),
            meadowrun.Deployment.git_repo(
                "https://github.com/visioninit/stable-diffusion",
                branch="meadowrun",
                interpreter=meadowrun.CondaEnvironmentFile("environment.yaml", additional_software="awscli"),
                environment_variables={"TRANSFORMERS_CACHE": "/var/meadowrun/machine_cache/transformers"}
            )
        )
    )

if __name__ == "__main__":
    main()