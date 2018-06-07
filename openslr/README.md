# Train Speech Recognition Model on [OpenSLR LibriSpeech ASR corpus](http://www.openslr.org/) dataset using [Tensor2Tensor](https://github.com/tensorflow/tensor2tensor) on [Clusterone](https://clusterone.com)


## Prerequisites
Let's first install prerequisites. We will install [Tensor2Tensor](https://github.com/tensorflow/tensor2tensor) and  [Clusterone](https://clusterone.com):

```sh
pip install --upgrade clusterone
pip install --upgrade tensor2tensor
```

## Set your environment variables
You need to set up the correct values here:

```sh
export CLUSTERONE_USER=[YOUR USERNAME]
```

## Clone the repo from [Clusterone Github](https://github.com/clusterone/OpenSlrTest)
Go to a directory that you want to clone and clone the repo in that directory:

```sh
git clone https://github.com/clusterone/OpenSlrTest.git
```

Install the dependencies for the project if you want to run it locally:

```sh
cd OpenSlrTest #Go to the directory of the file that you cloned from Clusterone Github
pip install -r requirements.txt
```

brew install sox


## Download and prepare [OpenSLR LibriSpeech ASR corpus](http://www.openslr.org/) data locally

Let's use Tensor2Tensor to download and prepare the dataset. Go to the downloaded repo and Run:

```sh
cd OpenSlrTest #Go to the directory of the file that you cloned from Clusterone Github
python dataset.py #If you want, you can change the download directory in dataset.py
```

## Login to [Clusterone](https://clusterone.com) by running the following command.

If you do not have an account first create your account at [Clusterone](https://clusterone.com). To login, enter:

```sh
just login
```

## Create and upload your dataset in S3 bucket on Clusterone

##### Create an S3 dataset on [Clusterone](https://clusterone.com)
* To create a new S3 dataset, run ```just create dataset s3 <bucket-name>```
* Note: Bucket name needs to be unique across AWS. The command will return an error in case the name is already taken.
* To find more information on creating S3 buckets [click here](https://docs.clusterone.com/docs/s3-datasets)


##### Upload to your Clusterone S3 bucket

* Obtain your AWS Access Keys from Clusterone. Go to [your account](https://clusterone.com/matrix/account) and select Keys.
* Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* Run  ```aws configure``` and input your access key and secret key. You can leave the region name and output format as default.
* Download your OpenSLR LibriSpeech ASR corpus dataset from [here](http://www.openslr.org/12/)
* Run ```aws s3 cp <source_file> s3://<bucket-name>``` for file upload or ```aws s3 cp <source-folder> s3://<bucket-name> --recursive``` for folder upload.


## Create a project on Clusterone

Create a project on Clusterone.

```sh
just init project openslr #you can change the "openslr" project name, if you want
```

Push the code to ClusterOne repo:

```sh
git push clusterone master
```

## Create and start a job

### 1 worker

```sh
just create job single --project $CLUSTERONE_USER/openslr --module main --name openslr-1w-0ps --datasets $CLUSTERONE_USER/<bucket-name> --description openslr-1w-0ps --python-version 2.7 --framework tensorflow-1.5.0  --instance-type p2.xlarge --time-limit 1h

just start job -p openslr/openslr-1w-0ps
```

### 2 workers and 1 parameter server

```sh
just create job distributed --project $CLUSTERONE_USER/openslr --module main --name openslr-2w-1ps --datasets $CLUSTERONE_USER/<bucket-name> --description openslr-2w-1ps --python-version 2.7 --framework tensorflow-1.5.0 --worker-type p2.xlarge --worker-replicas 2 --ps-type c4.2xlarge --ps-replicas 1 --time-limit 1h

just start job -p openslr/openslr-2w-1ps
```

### 4 wokers and 2 parameter server

```sh
just create job distributed --project $CLUSTERONE_USER/openslr --module main --name openslr-4w-2ps --datasets $CLUSTERONE_USER/<bucket-name> --description openslr-4w-2ps --python-version 2.7 --framework tensorflow-1.5.0 --worker-type p2.xlarge --worker-replicas 4 --ps-type c4.2xlarge --ps-replicas 2 --time-limit 1h

just start job -p openslr/openslr-4w-2ps
```

### 8 wokers and 4 parameter server

```sh
just create job distributed --project $CLUSTERONE_USER/openslr --module main --name openslr-8w-4ps --datasets $CLUSTERONE_USER/<bucket-name> --description openslr-8w-4ps --python-version 2.7 --framework tensorflow-1.5.0 --worker-type p2.xlarge --worker-replicas 8 --ps-type c4.2xlarge --ps-replicas 4 --time-limit 1h

just start job -p openslr/openslr-8w-4ps
```
