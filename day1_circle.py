import cv2
import numpy as np

print("OpenCV 运行成功！")
print("OpenCV 版本：", cv2.__version__)

# 创建一张黑色图像：高480像素、宽640像素、3个颜色通道
image = np.zeros((480, 640, 3), dtype=np.uint8)

# 在图像中央绘制绿色圆形
cv2.circle(image, (100, 100), 40, (0, 255, 0), -1)

# 显示图像
cv2.imshow("My First Vision Program", image)

# 按任意键关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
