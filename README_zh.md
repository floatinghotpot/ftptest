
通过 阶梯有氧骑行 线性拟合 轻松测试 FTP（功能阈值功率）的小工具。

# 安装 #

请确保 Python 3.7 以上版本.

```bash
python3 --version
python3 -m pip install ftptest
```

或者，从 GitHub 克隆:
```bash
git clone https://github.com/floatinghotpot/ftptest.git
cd ftptest
python3 -m pip install -e .
```

# 使用方法 #

```bash
ftptest <csv文件路径> [乳酸阈值心率]
```

```bash
ftptest docs/demo.csv 165
```

csv的格式，为每行一个功率和对应的心率，用逗号分隔，例如:
```bash
124,117
146,127
174,142
197,153
224,161
```

# 示例 #

使用 Zwift / MyWhoosh 进行阶梯有氧骑行训练：

![workout](https://github.com/floatinghotpot/ftptest/raw/main/docs/workout.jpg)

获得 功率/心率 数据和曲线：

![power heartrate](https://github.com/floatinghotpot/ftptest/raw/main/docs/power_hr.jpg)

从骑行的阶梯采样 功率/心率 进行线性拟合，并计算出 FTP：

![linear](https://github.com/floatinghotpot/ftptest/raw/main/docs/demo.png)

# 声明 #

漂流的火锅 创建的小工具。

欢迎使用哦和反馈。
