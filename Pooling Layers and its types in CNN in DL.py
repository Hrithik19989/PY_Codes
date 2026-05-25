import tensorflow as tf
from keras.layers import MaxPooling2D ,AveragePooling2D , GlobalMaxPooling2D, GlobalAveragePooling2D
import numpy as np

#Feature for MaxPooling2D
feature_map_mp = np.array([
    [1, 3, 2, 9],
    [5, 6, 1, 7],
    [4, 2, 8, 6],
    [3, 5, 7, 2]
]).reshape(1, 4, 4, 1)

# Feature for everything else
feature_map_GMAP = np.array([
    [1, 3, 2, 9],
    [5, 6, 1, 7],
    [4, 2, 8, 6],
    [3, 5, 7, 2]
], dtype=np.float32).reshape(1, 4, 4, 1)


#MaxPooling2D
max_pool = MaxPooling2D(pool_size=(2, 2), strides=2)
output_mp = max_pool(feature_map_mp)

#AveragePooling2D
avg_pool = AveragePooling2D(pool_size=(2, 2), strides=2)
output_ap = avg_pool(feature_map_GMAP)

#GlobalMaxPooling2D
gm_pool = GlobalMaxPooling2D()
gm_output_GMP = gm_pool(feature_map_GMAP)

#GlobalAveragePooling2D
ga_pool = GlobalAveragePooling2D()
ga_output_GAP = ga_pool(feature_map_GMAP)

#Printing Outputs
print(output_mp.numpy().reshape(2, 2))
print(output_ap.numpy().reshape(2, 2))
print("Global Max Pooling Output:", gm_output_GMP.numpy())
print("Global Average Pooling Output:", ga_output_GAP.numpy())
