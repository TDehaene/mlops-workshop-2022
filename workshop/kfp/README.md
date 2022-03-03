# MLOps workshop hands-on session 2: Kubeflow pipelines

The goal of this second hands-on session is to provide an example of how Kubeflow Pipelines SDK and Vertex Pipelines can be used to scale the basic machine learning pipeline from the first session. 
In the following section, we will first have a look at the changes that need to be made to the original code. 
Then we will see how you can define a machine learning pipeline using Kubeflow Pipelines SDK and deploy it with Vertex Pipelines.

Before you begin, from the kfp directory:
```
pip install -r requirements.txt
```

## Converting your ML steps to KFP components
Since KFP pipelines are built from connecting individual components together, the fist step is to implement and build these components, located in the `components` folder. 
A typical component folder has the following structure:

```
+-- _[COMPONENT_NAME]  
|   +-- src  
|   +-- build_image.sh  
|   +-- component.yaml  
|   +-- Dockerfile  
|   +-- requirements.txt  
```

### The `src` folder
This folder contains your component logic. 
Here you should define at least one python function that optionally takes some arguments and that will serve as the entrypoint to your component. 
This is the function that should be called whenever the component is run in the context of a ML pipeline and it is responsible for making sure all component logic is executed.

### The `requirements.txt` file
This file contains all non built-in python modules that your component needs and is just a normal `requirements.txt` file.

### The [`component.yaml`](https://www.kubeflow.org/docs/pipelines/reference/component-spec/) file
This file defines the metadata, interface and how to run the component. 
Here you should define the inputs this component expects (along with their types), where the implementation of the actual component logic is located (typically a Docker container 
in Google Container Registry (GCR)) and the command that should be executed when the component is run in the context of a ML pipeline. You may have to update your name in the image path, for example: `image: eu.gcr.io/motorway-ml6/elinaoik/training:latest`.

### The `Dockerfile`
This file defines how the Docker container for the component should be built. 
In the Dockerfile you will typically start from a certain Python version (here 3.7.9-slim), then install the required dependencies (e.g. Python modules) and f
inally copy all application logic code to your container.   

### The `build_image.sh` script
This file is a very simple bash script to submit a job to Google Cloud Builds. 
It will take all files (including folder and subfolders) that are located in the folder from which it is run and send them over to Cloud Build. 
Cloud build will then be able to build the Docker container you defined in you Dockerfile. Note the `--tag` argument that is provided to this command, which will tell Cloud Build where to store the Docker container image once it has been built. 
If all goes well, you can find the newly built image in [GCR](https://console.cloud.google.com/gcr/images/gothic-parsec-308513?project=gothic-parsec-308513).  
NOTE: The bash script might not work on Windows machines. 
Since the script is very simple, an easy workaround is to replace all variables with their appropriate values yourself and simply run the final gcloud command, i.e.:

> `gcloud builds submit --tag eu.gcr.io/motorway-ml6/YOUR_NAME/COMPONENT_NAME:latest COMPONENT_NAME`

There is a script that allows you to build all images at once (we will set an environment variable per participant name so that each participant has his own images:

```
NAME=[YOUR-NAME] ./build_component_images.sh
```

! Please update the path to the image in the component spec so that it points to your specific image repository.

#### When do you need to (re)build these images?
Whenever you make a change to your component (e.g. bug fix, new implementation, update version of some dependecy, ...) you need to rebuild that component. 
This can be done by manually running the `build_image.sh` script, or by automatically triggering this script whenever changes are made to the component in you version control system (VCS). 
The latter option requires you to set this up in your VCS of choice (including necessary permissions to allow your VCS to trigger cloud build jobs), which is out of the scope of this hands-on session.  
It is also important to note that the image tag ('latest' in the previous example) is a way to version your container images. 
If you rebuild your conainer image with the same tag, the old one will be overwritten. In case of using a VCS to trigger builds, it's typically a good practice to use the git commit tag as the image tag, that way you are also able to identify very easily which code is running in which container image.  

#### Where are these components stored?
Once the Docker container is built, it is stored in a container registry. When you build a container locally, it will be stored in your local container registry.
However, since we used Cloud Build and we provided a tag including the GCR URI (the 'eu.gcr.io/motorway-ml6' part), the built container image will be stored in GCR, where it can easily be picked up by KFP. 
It is exactly this URI is also provided in the `component.yaml` file to let KFP know where it can find the implementation of the component.  

## Defining a ML pipeline
Now that we have implemented and built the different components, we are ready to build our first pipeline, which are located in the `pipelines` folder. 
In this folder we typically create 1 Python file for each individual pipeline. Let's have a look at the `end_to_end_pipeline.py` file to understand what is happening.

### Loading the components
After first importing some elements from the [Kubeflow Pipelines Python SDK](https://www.kubeflow.org/docs/pipelines/sdk/), we start by importing the components that will be needed in the pipeline. Loading a component can be done from the `component.yaml` files that we created earlier.   
These files contain all the info that Vertex AI Pipelines needs to run a component. 
The `inputs` part of this yaml file tells KFP what input variables should be provided to this component. The `implementation` part tells KFP where it should look for the actual implementation whenever this component is run in the context of a ML pipeline and which command should be run.

### Defining the actual pipeline
Once all necessary components are loaded, we can define the actual pipeline. 
This is typically done through a Python function that is decorated with the `@dsl.pipeline` decorator, where you can provide a name and description for the pipeline. The inputs to this Python functions are all the parameters that you will be able to provide the pipeline with whenever it is being run at a later time. What they actually represent are placeholders that need to be filled in (you can also provide defaults) for every new pipeline run. It's also good practice to provide the type for each parameters, otherwise KFP needs to infer this and you might get some warning about this.  

In the Python function, we can then link together the different components and provide them with all the parameters they need.  
Also important to realise that you are not able to influence the pipeline definition based on runtime parameters. For example, you cannot set the cpu requirements of a certain step, based on one of the input parameters to the pipeline function for the simple reason that these values are not available when you deploy your pipeline (at which point KFP needs to know all resource requirements for each step), but only become available at runtime, when you actually fill the placeholders with concrete values.  

A possible solution to this last problem is to deploy 2 identical pipelines with different resource requirements and decide at runtime, based on the actual parameters that you receive, which pipeline should be run.

### Compiling and deploying the pipeline

The pipeline compiling and deploying is done in the `deploy_pipeline.py`.
During this process, KFP checks that your pipeline is correctly defined and creates a pipeline package (`json` file). 
This file can then be uploaded to Vertex AI Pipelines using the Python function as in this example.  

Important to realise here is that the pipeline package that is actually uploaded to Vertex AI Pipelines does not contain any logic of the pipeline itself. 
It just contains information about the interface of the different components (i.e. which parameters it takes as input) and where the actual implementation is stored (i.e. in GCR) 
along with information about how these components are connected and what resources they need (which was defined in the pipeline definition file).

To compile and deploy your pipeline, run:

```
python deploy_pipeline.py --identifier=[YOUR-NAME]
```

### Running the pipeline
Once the pipeline is uploaded, it is automatically run on Vertex Pipelines. You can see the implementation of the pipeline job in the UI and watch while the steps in the pipeline get completed.
When the execution is complete, the artifacts of the pipeline are stored in the Google Storage bucket we created during setup, inside a folder with your name.
