# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Defining common flags used across all BERT models/applications."""

from absl import flags
import tensorflow as tf

from official.utils.flags import core as flags_core


def define_common_bert_flags():
  """Define the flags related to TPU's."""
  flags.DEFINE_string('bert_config_file', None,
                      'Bert configuration file to define core bert layers.')
  flags.DEFINE_string('model_dir', None, (
      'The directory where the model weights and training/evaluation summaries '
      'are stored. If not specified, save to /tmp/bert20/.'))
  flags.DEFINE_string('tpu', '', 'TPU address to connect to.')
  flags.DEFINE_string(
      'init_checkpoint', None,
      'Initial checkpoint (usually from a pre-trained BERT model).')
  flags.DEFINE_enum(
      'strategy_type', 'mirror', ['tpu', 'mirror', 'multi_worker_mirror'],
      'Distribution Strategy type to use for training. `tpu` uses '
      'TPUStrategy for running on TPUs, `mirror` uses GPUs with single host, '
      '`multi_worker_mirror` uses CPUs or GPUs with multiple hosts.')
  flags.DEFINE_integer('num_train_epochs', 3,
                       'Total number of training epochs to perform.')
  flags.DEFINE_integer(
      'steps_per_loop', 200,
      'Number of steps per graph-mode loop. Only training step '
      'happens inside the loop. Callbacks will not be called '
      'inside.')
  flags.DEFINE_float('learning_rate', 5e-5,
                     'The initial learning rate for Adam.')
  flags.DEFINE_boolean(
      'run_eagerly', False,
      'Run the model op by op without building a model function.')

  # Adds flags for mixed precision training.
  flags_core.define_performance(
      num_parallel_calls=False,
      inter_op=False,
      intra_op=False,
      synthetic_data=False,
      max_train_steps=False,
      dtype=True,
      dynamic_loss_scale=True,
      loss_scale=True,
      all_reduce_alg=False,
      num_packs=False,
      enable_xla=True
  )


def use_float16():
  return flags_core.get_tf_dtype(flags.FLAGS) == tf.float16


def get_loss_scale():
  return flags_core.get_loss_scale(flags.FLAGS, default_for_fp16='dynamic')
