import torch as tch
import numpy as np

random = np.add(np.random.rand(4,4),1.j*np.random.rand(4,4))
random = tch.tensor(random)
random = tch.reshape(random,[2,2,2,2])
print(random)
print(random.shape)
random = tch.transpose(random,1,2)
print(random)
