import tensorflow as tf
import logging
import os
from distutils.dir_util import copy_tree
# from tensor2tensor.utils import registry
from tensor2tensor.bin import t2t_trainer
import json
from clusterone import get_data_path, get_logs_path

flags = tf.app.flags

flags.DEFINE_integer("number_worker_gpu", 0, "Number of worker GPUs")
flags.DEFINE_integer("number_ps_gpu", 0, "Number of PS GPUs")
flags.DEFINE_integer("batch_size", 2097152, "Batch size")

FLAGS = tf.flags.FLAGS

USERNAME = "sohrab"

DATASET_NAME = "openslr_small"
PROBLEM = 'librispeech_clean'

DATA_PATH = get_data_path(
            dataset_name = "%s/%s"%(USERNAME, DATASET_NAME), #on clusterone
            local_root = os.path.expanduser("~/Data"),
            local_repo = "openSLR",
            path = ''
            )

CHECKPOINTS_PATH = get_logs_path(root=os.path.expanduser("~/logs"))

if not os.path.exists(CHECKPOINTS_PATH):
    os.makedirs(CHECKPOINTS_PATH)



try:
    job_name = os.environ['JOB_NAME']
    task_index = int(os.environ['TASK_INDEX'])
    ps_hosts = os.environ['PS_HOSTS'].split(',')
    worker_hosts = os.environ['WORKER_HOSTS'].split(',')
    if job_name == 'ps':
        ps_hosts[task_index] = 'localhost:%s'%(ps_hosts[task_index].split(':')[-1])
    elif job_name == 'worker':
        worker_hosts[task_index] = 'localhost:%s'%(worker_hosts[task_index].split(':')[-1])
except:
    job_name = None
    task_index = 0
    ps_hosts = None
    worker_hosts = None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')

    for param in os.environ.keys():
        logging.info("%s: %s " % (param, os.environ[param]))

    # This sets the sync automatically
    if worker_hosts:
        FLAGS.sync = True if len(worker_hosts) == 1 else False
    else:
        FLAGS.sync = False

    # hack to get correct parameters for tensor2tensor
    if worker_hosts is not None:
        if job_name == 'ps':
            FLAGS.schedule = 'run_std_server'
            FLAGS.master = 'grpc://%s'%(ps_hosts[task_index])
            cluster = {
                'ps': ps_hosts,
                'master': worker_hosts
            }
            os.environ['TF_CONFIG'] = json.dumps({
                'cluster': cluster,
                'task': {'type': 'ps', 'index': task_index},
                'environment': 'cloud',
            })

        if job_name == 'worker':
            FLAGS.master = 'grpc://%s'%(worker_hosts[task_index])
            FLAGS.ps_replicas = len(ps_hosts)
            FLAGS.worker_replicas = len(worker_hosts)
            FLAGS.worker_gpu = FLAGS.number_worker_gpu  #TODO
            FLAGS.worker_id = task_index
            FLAGS.worker_job = '/job:master'
            FLAGS.ps_gpu = FLAGS.number_ps_gpu

            FLAGS.schedule='train'
            # FLAGS.schedule='continuous_eval_on_train_data'
            # FLAGS.schedule=continuous_train_and_eval
            # FLAGS.schedule='train_and_evaluate'

            cluster = {
                'ps': ps_hosts,
                'master': worker_hosts
            }
            os.environ['TF_CONFIG'] = json.dumps({
                'cluster': cluster,
                'task': {'type': 'master', 'index': task_index},
                'environment': 'cloud',
            })

    FLAGS.problems = PROBLEM
    FLAGS.model = 'transformer'
    FLAGS.hparams_set = 'transformer_librispeech'
    FLAGS.hparams = 'batch_size=%s'%(FLAGS.batch_size)
    FLAGS.train_steps = 2000000
    FLAGS.eval_steps = 100
    FLAGS.save_checkpoints_secs=100
    FLAGS.output_dir = CHECKPOINTS_PATH
    FLAGS.data_dir = DATA_PATH
    FLAGS.tmp_dir = os.path.expanduser("~/tmp")

    t2t_trainer.main(None)
