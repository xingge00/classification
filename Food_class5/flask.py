from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import cv2 as cv
import time

#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__) # 实例化wsgi


# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv.imread(upload_path)
        img = detection(img)
        cv.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')


def detection(image):
    inference_pb = 'F:\Projects\PycharmProjects\opencvtest\detection/test/sorted_inference_graph.pb'
    graph_txt = 'F:\Projects\PycharmProjects\opencvtest\detection/test/graph.pbtxt'
    net = cv.dnn.readNetFromTensorflow(inference_pb, graph_txt)
    h, w = image.shape[:2]
    cv.imshow("input", image)

    im_tensor = cv.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)
    net.setInput(im_tensor)
    cvOut = net.forward()
    print(cvOut.shape)
    for detect in cvOut[0, 0, :, :]:
        score = detect[2]
        if score > 0.5:
            left = detect[3] * w
            top = detect[4] * h
            right = detect[5] * w
            bottom = detect[6] * h
        cv.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 255), 4)
    return image


if __name__ == '__main__':
    app.run( debug=True)
