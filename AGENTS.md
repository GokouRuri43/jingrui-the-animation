# ECHO / 某某创作工程

用简体中文协作，所有文本使用UTF-8。先读根目录的 `某某-基础设定.md` 与 `ECHO-基础设定.md`。

## 创作边界

- 当前短片方向为《某某》，剧情尚未定稿。面孔真实变化、自我定义权的丧失、真人质感/二维/三维/拼贴与剧情统一，是创作基础。
- 《ECHO》文档中的早期地铁—城市—战斗—少女倒叙段落单独保留，不自动合并进《某某》。
- 回响来自积累的相信、传播和重复，不是任意一句话瞬间生效。城市文字变化是核心视觉语言。
- 原始人物姓名、职业与能力不是固定主角配置。新规则与候选故事单独标明，不擅自写成定稿。
- 先确定梗概再进入分镜；以导演视角设计行动、空间、转折和人物互动。
- `previs/demo.json` 只是技术预演样例，不是影片场景或剧情定稿。
- 未经明确要求不使用子代理。

## 运行与预演

- 云端安装 `bash cloud/install.sh`；启动检查 `bash cloud/start.sh`。
- 系统Python使用 `python3`，无外部Python依赖。`bpy`由Blender内置Python提供，不能用普通Python直接运行 `tools/blender_scene.py`。
- 先以低分辨率和低采样测试，使用 `python3 tools/render_previs.py --smoke`。
- 常规预演 `python3 tools/render_previs.py --config previs/demo.json --output outputs/demo`。
- 默认 Cycles CPU 后台渲染，不依赖GPU、X服务器、桌面UI或浏览器。
- 输出 `.blend`、PNG与MP4到 `outputs/`，不把生成结果和工具缓存自动加入Git。需要保留的正式场景另行归档。
- 修改环境或预演工具后执行小型渲染检查；纯设定文字改动无需渲染测试。
- 维持中文沟通，不把测试场景扩写成未经选择的剧情。
