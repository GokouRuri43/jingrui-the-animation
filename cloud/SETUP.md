# Codex云端环境：设定创作 + Blender三维预演

配置日期：2026年10月21日。

## 直接填写的配置

| 项目 | 值 |
| --- | --- |
| 仓库 | `GokouRuri43/jingrui-the-animation`，私有 |
| 分支 | `main` |
| 环境名 | 建议 `jingrui-animation` |
| 系统 | Ubuntu / Debian Linux，安装过程可使用apt-get与root/sudo |
| Install script | `bash cloud/install.sh` |
| Start skill | 采用 `cloud/START.md` 的内容，启动命令 `bash cloud/start.sh` |
| Python | 系统Python 3.10+，推荐3.12；不需要pip安装bpy |
| Blender | 系统软件源的Blender 3.4+，实际版本由检查报告记录 |
| 渲染模式 | Cycles CPU，后台运行，默认2线程 |
| 网络 | 开启并选择 Package managers；研究网页所需域名按任务补充 |
| 环境变量 | `PYTHONUTF8=1`；`TZ=Asia/Shanghai` |
| 可选环境变量 | 只有Blender不在PATH时才设置 `BLENDER_BIN` 为可执行文件实际路径 |
| Secrets | 当前无需任何密钥 |
| Privacy / Who can use | Only me |

本仓库不依赖上一版本地迁移方案的虚拟环境、Pillow、参考影片或媒体包。素材只有两份基础设定，其余文件用于配置和预演。

## 创建环境时可直接发送

> 请将GokouRuri43/jingrui-the-animation配置为中文AI短片创作与Blender三维预演环境。先读AGENTS.md及两份基础设定。在Ubuntu/Debian执行bash cloud/install.sh，安装并验证Blender、FFmpeg、Python和中文字体。使用Cycles CPU后台渲染，不要求GPU、X服务器或交互桌面。将cloud/START.md设为启动说明。请验证生成scene.blend、三张PNG和可读的preview.mp4，检查outputs/install-smoke/validation.json和Blender日志，报告实际Blender版本。完成后保存供发布，发布后在新任务再次运行bash cloud/start.sh。不要生成新剧情或把技术样例当作正式场景。

## Blender运行方式

云端预演通过脚本搭建场景、摆放摄影机和人物占位、记录关键帧，并进行离线渲染。可以输出可在本机继续编辑的`.blend`场景、PNG静帧及MP4运镜预览。

安装Blender不代表提供远程交互桌面。当前Codex Cloud官方文档将computer/browser use列为尚不支持。此配置保证的目标是后台脚本工作流，交互拖拽或本机软件操作可在下载`.blend`之后完成。

发行版自带Blender版本可能与本机5.2 LTS不同。本仓库以JSON和脚本重建场景，降低跨版本文件依赖；正式交换`.blend`前应统一版本并进行打开检查，不假设旧版能打开新版保存的所有功能。

无GPU时Cycles CPU可用于低模构图、空间关系、走位与运镜预演；不据此承诺高分辨率复杂场景的实时速度。默认640×360、8 samples、12fps。正式提高精度前先用静帧估算耗时。

## 参数与输出

`previs/demo.json`中的 `frames / fps` 决定视频时长，默认36/12=3秒。`camera.start/end`为摄影机位置，`camera.target`为注视点，`camera.lens`为焦距。人物`start/end`为走位，`buildings`为场景体块。

常用命令见根目录README。生成结果位于指定的`outputs/`子目录，包含：

- `scene.blend`：含摄像机和人物动画的可编辑场景。
- `shot.json`：本次执行的参数，包含小测试覆盖后的实际值。
- `frames/frame_0001.png`等：渲染序列。
- `preview.mp4`：动画模式的H.264视频。
- `blender.log`、`blender-result.json`、`validation.json`：实际执行日志与验证结果。

只生成场景的build模式不输出图片或视频；still模式只输出第一帧。动画模式用ffprobe检查视频尺寸及实际帧数，避免只检查进程是否退出。

## 云端发布验收

1. 从私有仓库创建环境，开放Package managers需要的软件源访问。
2. 运行安装脚本，检查是否完成真实CPU渲染与MP4编码。
3. 查看生成的图片或视频，以及实际版本与验证报告。
4. 保存并Publish；在新任务中运行启动检查，确认发布的环境可复用。

上传仓库不等于创建或发布Codex云端环境。GitHub Actions的Ubuntu验证提供Linux兼容性证据，账号内的实际云端安装仍须完成。

如果使用旧版界面：Setup script填 `bash cloud/install.sh`，Maintenance script填 `bash cloud/start.sh`；依赖更改后重新安装或重置缓存。不要将新版Network secrets和发布机制照搬到旧版。

## 网络与资料

依赖由系统软件源安装，没有后台下载参考视频或大模型。需要检索比赛信息时再添加 `jingrui-ai-competition.youku.com`；Blender资料可添加 `docs.blender.org`。放行域名不代表自动提供网站账号或应用连接器。

源码与两份设定保存在Git；输出默认忽略，重要制作结果另外归档。

官方参考：

- [Codex当前云端环境：创建、安装、启动、网络与限制](https://learn.chatgpt.com/docs/environments/cloud-environments)
- [Blender后台命令行渲染](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html)
- [Blender命令参数：background、Python exit code、CPU与线程](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html)
