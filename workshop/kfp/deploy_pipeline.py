"""Deploy KFP pipeline to Vertex AI Pipelines."""
import tempfile
from datetime import datetime

import fire
from kfp.v2 import compiler
from kfp.v2.google.client import AIPlatformClient
import google.auth

from pipelines.end_to_end_pipeline import get_end_to_end_pipeline

_, PROJECT_ID = google.auth.default()

project_id = "smart-amplifier-343007"
region = "europe-west1"
gcs_bucket = f'{project_id}_vertex_pipelines_artifacts'

API_CLIENT = AIPlatformClient(project_id=project_id, region=region)


def deploy_pipeline(name: str):
    # Set environment variable to be able to customize pipeline name

    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    pipeline_id_name = f"{name}-end-to-end-pipeline"
    pipeline_function = get_end_to_end_pipeline(name)

    with tempfile.NamedTemporaryFile() as temp_f:
        pipeline_filename = f'{temp_f.name}.json'
        compiler.Compiler().compile(pipeline_func=pipeline_function,
                                    package_path=pipeline_filename)

        response = API_CLIENT.create_run_from_job_spec(
            pipeline_filename,
            pipeline_root=f'gs://{gcs_bucket}/{name}/{pipeline_id_name}',
            parameter_values={
                'project_id': project_id,
                'gcs_bucket': f'{gcs_bucket}/{name}-{run_id}',
            })
        print('Successfully deployed pipeline')


if __name__ == '__main__':
    fire.Fire(deploy_pipeline)
