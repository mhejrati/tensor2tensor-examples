import tensorflow as tf
from tensor2tensor.bin import t2t_datagen
import os
from clusterone import get_data_path, get_logs_path

# LOCAL_DATASET_ROOT = 'ADDRESS'  # e.g. os.path.expanduser("~/Data")
LOCAL_DATASET_ROOT = os.path.expanduser("~/Data")  # e.g. os.path.expanduser("~/Data")
LOCAL_DATASET_NAME = 'openSLR'
PROBLEM = 'librispeech_clean'

TMP_PATH = os.path.expanduser("~/tmp")
if not os.path.exists(TMP_PATH):
    os.makedirs(TMP_PATH)

FLAGS = tf.flags.FLAGS

if __name__ == '__main__':
    FLAGS.problem = PROBLEM
    FLAGS.data_dir = os.path.join(LOCAL_DATASET_ROOT, LOCAL_DATASET_NAME)
    FLAGS.tmp_dir = TMP_PATH
    t2t_datagen.main(None)
