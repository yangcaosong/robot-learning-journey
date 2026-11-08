# Robot Learning Journey

从 Python 视觉入门到实体机器人的持续学习与实践。

## 项目目标

通过实际编写、运行和调试代码，逐步掌握机器人视觉、Linux、嵌入式系统、ROS 2、运动控制、强化学习和四足机器人仿真部署。

学习过程中优先完成可运行的项目，记录遇到的问题、解决方法和实际成果，而不是单纯积累练习代码。

## Hardware

- Orange Pi 5 Plus
- RK3588
- USB Camera
- Sensors and actuators（逐步接入）

## Development Environment

### Windows 学习电脑

- Python 3.11.9
- Python 虚拟环境：`.venv`
- OpenCV 5.0.0
- NumPy 2.4.6
- Git

### Orange Pi 5 Plus

- Ubuntu Desktop
- eMMC 启动
- 中文语言环境
- 网络连接已验证
- Python 3.10.12
- pip 22.0.2
- Git 2.34.1
- GCC 11.4.0
- G++ 11.4.0
- 已创建机器人学习文件夹

## Progress

### 一、Windows 上的 Python 与 OpenCV

- [x] 安装 Python 3.11
- [x] 创建 Python 虚拟环境 `.venv`
- [x] 安装并验证 OpenCV、NumPy
- [x] Day 1：创建图像并绘制绿色圆形
- [x] Day 2：读取本地图片、检查读取结果并查看图像尺寸
- [x] Day 3：打开 USB 摄像头并实现实时画面显示
- [x] Day 3：使用 HSV 阈值识别红色目标
- [x] Day 3：使用形态学开运算与闭运算处理掩膜噪点
- [x] Day 3：通过轮廓面积筛选候选目标
- [x] Day 3：计算目标中心点并绘制绿色外接框、红色中心点
- [x] Day 3：根据上一帧中心位置实现基础目标跟踪
- [x] Day 3：调整形态学核，减少手部误判产生的零散白点
- [x] Day 4：根据目标中心点变化计算移动方向
- [x] Day 4：根据位移和时间间隔计算像素速度（pixels/s）
- [x] Day 4：设置像素偏移阈值，过滤检测抖动
- [x] Day 4：在摄像头画面实时显示移动方向和速度
- [x] Day 5：使用 deque 保存目标最近的运动轨迹
- [x] Day 5：绘制目标运动轨迹
- [x] Day 5：计算目标累计移动距离
- [x] Day 6：使用 5 帧移动平均滤波平滑目标中心坐标
- [x] Day 6：对比原始坐标与滤波后的坐标
- [x] Day 6：观察移动平均对目标跟踪、速度和累计距离的影响
- [ ] Day 7：学习卡尔曼滤波（Kalman Filter）
- [ ] Day 7：实现目标位置预测与测量更新
- [ ] 继续优化复杂光照下的颜色识别与误判处理
- [ ] 对比原始坐标、移动平均与卡尔曼滤波的跟踪效果
- [ ] 探索目标跟踪、滤波和机器人运动控制

当前视觉项目文件：

- `red_object_tracking.py`：红色目标识别、跟踪、方向判断、速度估算、运动轨迹、累计距离及 5 帧移动平均滤波。

### 二、Orange Pi 5 Plus

#### 硬件与系统

- [x] 准备 Orange Pi 5 Plus 开发板
- [x] 安装 eMMC
- [x] 将 Ubuntu 安装到 eMMC
- [x] 成功进入 Ubuntu Desktop
- [x] 配置中文语言
- [x] 成功连接网络

#### Linux 开发环境

- [x] 更新软件包列表并检查系统环境
- [x] 确认 Python 版本
- [x] 确认 pip 是否可用
- [x] 确认 Git 是否可用
- [x] 确认 GCC、G++ 是否可用
- [x] 确认 Python 虚拟环境工具是否可用
- [x] 创建机器人学习文件夹
- [x] 在 Orange Pi 上创建 Python 虚拟环境
- [x] 在 Orange Pi 上安装并验证 OpenCV、NumPy
- [x] 在 Orange Pi 上成功运行 Python 程序
- [x] 将 Windows 视觉项目迁移到 Orange Pi
- [x] 适配 Linux 下的摄像头访问方式
- [x] 在 Orange Pi 上成功运行红色目标识别与跟踪程序

#### 当前开发平台

- Windows：Python 3.11 + OpenCV，作为前期开发和测试环境。
- Orange Pi 5 Plus：Ubuntu Desktop + Python 虚拟环境 + OpenCV，作为 ARM Linux 实际运行平台。

#### 下一阶段

- [ ] 在 Orange Pi 上继续完善视觉目标跟踪
- [ ] 实现卡尔曼滤波
- [ ] 探索摄像头与 GPIO、传感器的结合
- [ ] 逐步进入 ROS 2 学习与机器人控制

### 三、长期学习方向

- [ ] Linux 与 Python 开发
- [ ] OpenCV 视觉处理
- [ ] ROS 2
- [ ] 机器人运动控制与传感器
- [ ] 机器人仿真与强化学习
- [ ] 四足机器人相关项目探索

## Learning Principles

- 以实际运行和调试代码为主要学习方式。
- 优先理解现有项目，再根据需要修改和扩展。
- 记录真实完成的功能，不为了完成进度而创建无实际用途的文件。
- 每次学习结束后，保存可运行版本，并将实际完成的成果同步到 GitHub。
- 逐步将视觉算法迁移到 Orange Pi，并探索实体机器人应用。