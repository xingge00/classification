import tensorflow as tf
import os
filename = tf.placeholder(tf.string, [], name='filename')
image_file = tf.read_file(filename)
# Decode the image as a JPEG file, this will turn it into a Tensor
image = tf.image.decode_jpeg(image_file)  # 图像解码成矩阵
image = 255.0 * tf.image.convert_image_dtype(image, tf.float32)

with tf.Session() as sess:
    rootdir = "F:\Projects\PycharmProjects/test/retrain\data/train\Fried_meat_with_broccoli"
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        try:
            img_name1 = os.path.join(rootdir, list[i])
            image1_ = sess.run(image, feed_dict={filename: img_name1})
            # print(image1_.shape)  # (240,320,3)
        except :
            print(img_name1)

