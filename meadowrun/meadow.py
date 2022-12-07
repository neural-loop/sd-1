import asyncio
import meadowrun

def main():
    s3_bucket_name = "visioninit-sd"  # replace this with your own bucket name!
    model_name = 'v1-5-pruned-emaonly.ckpt'

    asyncio.run(
        meadowrun.run_command(
            'bash -c \''
            f'aws s3 sync s3://{s3_bucket_name} /var/meadowrun/machine_cache '
            '       --exclude "*" '
            f'      --include {model_name} '
            '       --include prompts.txt '
            '&& python scripts/txt2img.py '
            '       --skip_grid '
            '       --ddim_steps 30 '
            '       --H 320 '
            '       --W 576 '
            '       --n_samples 1 '
            '       --n_iter 1 '
            '       --scale 7.5 '
            '       --from-file /var/meadowrun/machine_cache/prompts.txt '
            f'      --ckpt /var/meadowrun/machine_cache/{model_name} '
            '       --seed 1337 '
            '       --precision autocast '
            '       --outdir /tmp/outputs '
            '       --device cuda '
            '&& python scripts/resize.py '
            f'&& aws s3 sync /tmp/outputs/samples_resized s3://{s3_bucket_name}/resized/{model_name}'
            f'\'',
            meadowrun.AllocCloudInstance("EC2"),
            meadowrun.Resources(
                logical_cpu=1, memory_gb=8, max_eviction_rate=80, gpu_memory=10, flags="nvidia"
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