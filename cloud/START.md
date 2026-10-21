# Start skill内容

此文件提供云端环境“Start skill”字段所需的启动步骤；它本身不会自动注册平台技能。

1. 进入包含 `AGENTS.md` 和 `cloud/install.sh` 的仓库根目录。
2. 运行 `bash cloud/start.sh`，验证系统Python、Blender后台启动、Cycles CPU、FFmpeg和两份UTF-8基础设定。
3. 无需启动Web服务、数据库或图形桌面。Blender按任务以后台命令启动，执行完退出。
4. 开始创作前阅读 `AGENTS.md` 和两份基础设定。先用低分辨率预演验证镜头，再按需要提升画质。
5. 安装或版本变化后运行 `python3 tools/render_previs.py --smoke --output outputs/environment-smoke` 验证实际渲染与编码。
6. 输出位于 `outputs/`。重要`.blend`和预演视频及时归档；任务存储不作为唯一副本。
