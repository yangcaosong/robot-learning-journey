
import cv2
import numpy as np

# 1. 打开 USB 摄像头
# Windows 下先尝试摄像头编号 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    cap.release()
    raise RuntimeError(
        "无法打开摄像头。请检查 USB 连接，"
        "关闭其他占用摄像头的软件后再试。"
    )

print("摄像头已打开，按 q 键退出")

previous_center = None

try:
    while True:
        # 2. 读取一帧实时画面
        ret, frame = cap.read()

        if not ret:
            print("读取摄像头画面失败")
            break

        # 3. BGR 转 HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 4. 红色范围：红色跨越 H 的两端
        lower_red1 = np.array([0, 80, 80])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 80, 80])
        upper_red2 = np.array([179, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # 去除小噪点，并填补目标内部的小空洞
        # 开运算：清除零散的小白点
        open_kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            open_kernel
        )

        # 闭运算：连接目标内部的小缺口
        close_kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            close_kernel
        )
        
        # 5. 从红色掩膜中提取轮廓
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

                # 6. 筛选轮廓，计算候选区域的中心
        min_area = 800
        candidates = []

        for contour in contours:
            area = cv2.contourArea(contour)

            if area < min_area:
                continue

            M = cv2.moments(contour)

            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            candidates.append({
                "contour": contour,
                "area": area,
                "center": (cx, cy)
            })

            # print("候选目标数量：", len(candidates))

                # 7. 根据上一帧的位置选择目标
        target = None

        if candidates:
            if previous_center is None:
                # 第一次检测：选择面积最大的区域
                target = max(
                    candidates,
                    key=lambda item: item["area"]
                )
            else:
                max_distance = 150
                px, py = previous_center
                nearby = []

                for item in candidates:
                    cx, cy = item["center"]
                    distance = (
                        (cx - px) ** 2 + (cy - py) ** 2
                    ) ** 0.5

                    if distance <= max_distance:
                        nearby.append(item)

                if nearby:
                    target = min(
                        nearby,
                        key=lambda item: (
                            (item["center"][0] - px) ** 2
                            + (item["center"][1] - py) ** 2
                        ) ** 0.5
                    )
                else:
                    # 当前目标丢失，等待重新捕获
                    previous_center = None

                    # 暂时重新选择面积最大的候选目标
                    target = max(
                        candidates,
                        key=lambda item: item["area"]
                    )

        # print("是否选中目标：", target is not None)

        # 8. 只要选中了目标，就绘制标记
        if target is not None:
            contour = target["contour"]
            area = target["area"]
            cx, cy = target["center"]

            x, y, w, h = cv2.boundingRect(contour)

            # 绿色目标框
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # 红色中心点
            cv2.circle(
                frame,
                (cx, cy),
                5,
                (0, 0, 255),
                -1
            )

            # 显示中心坐标和面积
            cv2.putText(
                frame,
                f"Center: ({cx}, {cy}) Area: {int(area)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            # 保存当前中心，供下一帧使用
            previous_center = (cx, cy)

            # 7. 显示实时结果
        cv2.imshow("USB Camera", frame)
        cv2.imshow("Red Mask", mask)

        # 按 q 退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    # 8. 释放摄像头和窗口
    cap.release()
    cv2.destroyAllWindows()
    print("摄像头已关闭")