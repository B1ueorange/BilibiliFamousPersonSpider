import tensorflow as tf
print(tf.test.is_gpu_available())

gpus = tf.config.list_physical_devices('GPU')
cpus = tf.config.list_physical_devices('CPU')

print(gpus, cpus)