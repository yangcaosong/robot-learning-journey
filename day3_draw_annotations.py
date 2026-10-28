
import cv2
import numpy as np

# 创建一张黑色图片：宽 640，高 480
image = np.zeros((480, 640, 3), dtype=np.uint8)
# 1. 画绿色矩形：左上角 (100, 80)，右下角 (300, 250)
cv2.rectangle(image, (100, 80), (300, 250), (0, 255, 0), 2)

# 2. 在目标位置画红色圆点
cv2.circle(image, (200, 165), 5, (0, 0, 255), -1)

# 3. 添加文字
cv2.putText(
    image,
    "Target",
    (100, 65),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

# 显示结果
cv2.imshow("Day 3 - Annotations", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
