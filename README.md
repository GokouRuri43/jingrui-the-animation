# jingrui-the-animation · ECHO / 某某

原创都市异能AI短片创作与Blender三维预演工程。

## 创作素材

只收录两份基础设定：

- [《某某》基础设定](某某-基础设定.md)
- [《ECHO / 回响》基础设定](ECHO-基础设定.md)，包含之前设计的地铁、城市、战斗与少女倒叙拍摄段落。

《某某》的剧情尚未定稿。仓库不包含参考影片、抽帧、旧候选故事或本地工具缓存。

## 云端准备

详细设置见 [cloud/SETUP.md](cloud/SETUP.md)。使用Ubuntu/Debian，在仓库根目录运行：

```bash
bash cloud/install.sh
```

安装Python、Blender、FFmpeg和中文字体，随后执行一次三帧CPU后台渲染及MP4编码检查。无额外Python包、API密钥、数据库、GPU或桌面窗口要求。

日常启动检查：

```bash
bash cloud/start.sh
```

## Blender三维预演

```bash
# 3帧小测试：160×90，Cycles CPU
python3 tools/render_previs.py --smoke --output outputs/smoke

# 默认3秒预演：640×360，12fps，含摄像机与人物占位移动
python3 tools/render_previs.py --config previs/demo.json --output outputs/demo

# 只生成可继续编辑的场景，不渲染
python3 tools/render_previs.py --mode build --output outputs/scene-only

# 只渲染第一帧用于构图检查
python3 tools/render_previs.py --mode still --output outputs/still
```

输出目录包含 `scene.blend`、实际使用的 `shot.json`、日志与验证结果。动画模式另含 `frames/` 下的PNG序列和 `preview.mp4`。

编辑 [previs/demo.json](previs/demo.json) 可调整镜头焦距、摄影机起止位置、注视点、场景体块、人物占位走位、时长、分辨率和采样数。样例仅用于环境验收，不属于剧情设定。

Blender通过自身内置Python执行 `tools/blender_scene.py`；普通Python只负责调度和视频编码。使用新输出目录区分不同镜头和迭代；同名输出会重建同名产物。渲染结果默认不提交Git，需要保存时另行下载或归档。

## 验证

本地Blender 5.2.0 LTS已完成Cycles CPU三帧渲染、MP4属性检查及640×360构图静帧检查。

[Linux自动检查](https://github.com/GokouRuri43/jingrui-the-animation/actions/workflows/cloud-smoke.yml) 在Ubuntu 24.04安装系统包并运行同一后台渲染流程，保留验证日志、`.blend`、PNG与MP4为短期Actions产物。

Linux自动检查不能替代Codex账号中实际环境的安装、网络与发布后验收；创建云端环境时仍需运行安装脚本。
