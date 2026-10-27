import cv2

image = cv2.imread("images/test.jpg")

if image is None:
    print("图片读取失败，请检查路径和文件名。")
else:
    print("图片读取成功！")
    print("图片尺寸（高度、宽度、通道数）：", image.shape)

    cv2.imshow("Day 2 - Read Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
