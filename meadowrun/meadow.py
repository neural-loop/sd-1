import asyncio
import meadowrun

def main():
    s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!
    model_name = 'v1-5-pruned-emaonly.ckpt'

    asyncio.run(
        meadowrun.run_command(
            'bash -c \''
            'nvidia-smi'
            f'&& aws s3 sync s3://{s3_bucket_name} /var/meadowrun/machine_cache '
            '       --exclude "*" '
            f'      --include {model_name} '
            '       --include prompts.txt '
            '&& python custom-aimodels/createimage-small.py'
            '&& python custom-aimodels/resize.py '
            '&& python custom-aimodels/img2img-upscale.py '
            f'&& aws s3 sync /tmp/outputs/img2img s3://{s3_bucket_name}/{model_name}/'
            f'\'',
            meadowrun.AllocCloudInstance("EC2"),
            meadowrun.Resources(
                logical_cpu=1, memory_gb=8, max_eviction_rate=80, gpu_memory=20, flags="nvidia"
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