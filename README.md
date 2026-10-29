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

- Python 3.11
- Python 虚拟环境：`.venv`
- OpenCV
- NumPy
- Git

### Orange Pi 5 Plus

- Ubuntu Desktop
- eMMC 启动
- 中文语言环境
- 网络连接已验证

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
- [ ] 继续优化复杂光照下的颜色识别与误判处理
- [ ] 学习目标移动方向和速度估计
- [ ] 根据项目需要探索目标跟踪、滤波和控制

### 二、Orange Pi 5 Plus

#### 硬件与系统

- [x] 准备 Orange Pi 5 Plus 开发板
- [x] 安装 eMMC
- [x] 将 Ubuntu 安装到 eMMC
- [x] 成功进入 Ubuntu Desktop
- [x] 配置中文语言
- [x] 成功连接网络

#### Linux 开发环境

- [ ] 更新软件包列表并确认成功
- [ ] 确认 Git 是否可用
- [ ] 确认 Python 虚拟环境工具是否可用
- [ ] 创建机器人学习项目目录
- [ ] 在 Orange Pi 上运行 Python 程序
- [ ] 验证 OpenCV 是否可用
- [ ] 尝试运行 Windows 上的视觉项目

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
