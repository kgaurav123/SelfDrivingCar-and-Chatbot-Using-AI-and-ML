# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 12:12:12 2019

@author: amanv
"""

import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
import numpy as np
PATH = os.getcwd()
LOG_DIR =PATH + '/mnist-tensorboard/log'
metadata = os.path.join(LOG_DIR , 'metadata.tsv')
mnist = input_data.read_data_sets(PATH + '/mnist-tensorboard/data',one_hot = True)
images = tf.Variable(mnist.test.images,name='images')
#def save_metadata(file):
with open(metadata,'w') as metadata_file:
    for row in range(10000):
        c=np.nonzero(mnist.data.labels[::1])[1:][0][row]
        metadata_file.write('{}\n'.format(c))
        
with tf.Session() as sess:
    saver = tf.train.Saver([images])
    
    sess.run(images.initializer)
    saver.save(sess , os.path.join(LOG_DIR,'images.ckpt'))
    config=projector.ProjectorConfig()
    #One can add multiple embeddings.
    embedding = config.embeddings.add()
    embedding.tensor_name=images.name
    #Link this tensor to its metadata file (eg labels)
    embedding.metadata_path  = metadata
    #saves a config file that tensorflow will read during startup
    projector.visualize_embeddings(tf.summary.FileWriter(LOG_DIR),config)