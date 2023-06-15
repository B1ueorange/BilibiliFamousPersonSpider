
import dlib

print(dlib.__version__)

# 查看是否打开了CUDA加速
print(dlib.DLIB_USE_CUDA)

# 获取设备个数
print(dlib.cuda.get_num_devices())