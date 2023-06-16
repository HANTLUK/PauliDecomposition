import tensorflow as tf
import numpy as np

random = np.add(np.random.rand(4,4),1.j*np.random.rand(4,4))
tf.convert_to_tensor(random)
random = tf.reshape(random,[2,2,2,2])
print(random)
print(random.shape)
random = tf.transpose(random,perm=[0,2,1,3])
print(random)

# print(np.tensordot(matZ,mat1,0).swapaxes(1,2).reshape(4,4))
