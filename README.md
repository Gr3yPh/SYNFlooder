# SYNFlooder

## 项目简介

SYNFlooder 是一个用于模拟 SYN Flood 和 UDP Flood 攻击的工具。它具有图形用户界面（GUI），可以轻松地输入目标服务器的 IP 地址、端口以及攻击速度等参数。

## 功能

- **SYN Flood 攻击**：通过发送大量的 SYN 包来消耗目标服务器的资源。
- **UDP Flood 攻击**：通过发送大量的 UDP 包来消耗目标服务器的带宽。

## 使用方法

1. 克隆项目到本地：

    ```sh
    git clone https://github.com/Gr3yPh/SYNFlooder.git
    cd SYNFlooder
    ```

2. 安装依赖：

    请确保你已经安装了 Python 3 以及相关的依赖包。你可以使用以下命令来安装依赖：

    ```sh
    pip install -r requirements.txt
    ```

3. 运行工具：

    使用以下命令启动图形界面：

    ```sh
    python synflooder-graphic.py
    ```

4. 在图形界面中：

    - 输入目标服务器的 IP 地址。
    - 输入本机的 IP 地址。
    - 输入目标端口。
    - 输入源端口（仅 SYN Flood 攻击需要）。
    - 输入发送速度（1-1000）。
    - 选择要进行的攻击类型（SYN 或 UDP），并点击相应的按钮开始攻击。
    - 点击“停止攻击”按钮停止当前攻击。

## 注意事项

- 本工具仅供学习和研究网络安全之用，严禁用于非法用途。
- 使用本工具时，请确保你有合法的授权对目标服务器进行测试。

## 作者

- **GR3YPH_4NTOM**
- GitHub: [https://github.com/Gr3yPh](https://github.com/Gr3yPh)

## 许可证

本项目采用 Apache 许可证，详情请参阅LICENSE文件。
