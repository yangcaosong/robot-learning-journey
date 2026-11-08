
import cv2
import numpy as np
import time
from collections import deque

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
# Day 5：保存目标最近的运动轨迹
trajectory = deque(maxlen=64)
# Day 6：保存最近 5 帧的目标中心坐标
center_history = deque(maxlen=5)
total_distance = 0.0
# Day 4：记录上一次速度测量的位置和时间
last_measurement_center = None
last_measurement_time = None

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
        lower_red1 = np.array([0, 130, 80])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 130, 80])
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
                    last_measurement_center = None
                    last_measurement_time = None

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
            # 获取原始中心坐标
            raw_cx, raw_cy = target["center"]

            # 保存最近 5 帧的原始坐标
            center_history.append((raw_cx, raw_cy))

            # 计算 X、Y 方向的平均坐标
            cx = int(np.mean([p[0] for p in center_history]))
            cy = int(np.mean([p[1] for p in center_history]))

            # 计算当前点与上一个轨迹点之间的距离
            if len(trajectory) > 0:
                last_x, last_y = trajectory[-1]

                dx = cx - last_x
                dy = cy - last_y

                step_distance = (dx ** 2 + dy ** 2) ** 0.5

                total_distance += step_distance

            # 保存当前中心点
            trajectory.append((cx, cy))

            for i in range(1, len(trajectory)):
                point1 = trajectory[i - 1]
                point2 = trajectory[i]

                cv2.line(
                    frame,
                    point1,
                    point2,
                    (255, 0, 0),
                    2
                )

            direction = "Waiting..."
            speed = 0.0

            # Day 4：计算目标移动方向和速度
            current_time = time.perf_counter()

            if last_measurement_center is not None:
                dx = cx - last_measurement_center[0]
                dy = cy - last_measurement_center[1]

                dt = current_time - last_measurement_time

                if dt > 0:
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    speed = distance / dt

                    # 判断移动方向
                    if abs(dx) < 3 and abs(dy) < 3:
                        direction = "Stationary"
                        speed = 0
                    elif abs(dx) > abs(dy):
                        direction = "Right" if dx > 0 else "Left"
                    else:
                        direction = "Down" if dy > 0 else "Up"

                    # print(
                    #     f"Direction: {direction}, "
                    #     f"Speed: {speed:.2f} pixels/s"
                    # )

            # 更新本次测量的位置和时间
            last_measurement_center = (cx, cy)
            last_measurement_time = current_time

            x, y, w, h = cv2.boundingRect(contour)

            # 绿色目标框
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # 黄色点：原始检测中心
            cv2.circle(
                frame,
                (raw_cx, raw_cy),
                5,
                (0, 255, 255),
                -1
            )

            # 连线：显示两个中心点之间的偏差
            cv2.line(
                frame,
                (raw_cx, raw_cy),
                (cx, cy),
                (255, 255, 0),
                1
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

            # 显示移动方向
            cv2.putText(
                frame,
                f"Direction: {direction}",
                (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # 显示移动速度
            cv2.putText(
                frame,
                f"Speed: {speed:.2f} pixels/s",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # 显示累计移动距离
            cv2.putText(
                frame,
                f"Total Distance: {total_distance:.2f} pixels",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            # 保存当前中心，供下一帧使用
            previous_center = (raw_cx, raw_cy)

        else:
            trajectory.clear()
            center_history.clear()
            total_distance = 0.0

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