# CTMDbA 魔改版

MoviePilot V3 插件 `CureTMDbAnimeShy` 的独立维护仓库，从 [shyblacktea/MoviePilot-Plugins](https://github.com/shyblacktea/MoviePilot-Plugins) 提取，保留原作者 Attente、shyblacktea 的功能与署名，由 ifsherlock 维护兼容修复。

## 安装

在 MoviePilot 的插件仓库设置中添加：

```text
https://github.com/ifsherlock/moviepilot-curetmdbanimeshy
```

仓库仅提供 MoviePilot V3 插件。当前版本 **0.0.9**，使用 `package.v3.json` 索引及 `CureTMDbAnimeShy_v0.0.9` 发布包。

从其他仓库迁移已安装的同 ID 插件时，请使用 MoviePilot 的插件来源切换功能选择本仓库，再安装新版本。无需卸载；保留原插件 ID 可沿用现有配置和数据。

## 功能

- 对 TMDB 被合并为一季的番剧提供分季修正，支持 TVDB、Bangumi 和自定义来源。
- 支持优先使用来源中的分季定义、累计集数转换、按播出时间窗口推断季号、越界宽限和改写阈值。
- 保留同步与异步识别修正、下载历史季集优先采用，以及按关键词排除识别增强。
- 支持刷新来源缓存和上传来源文件；配套服务随插件启动、停止或重载。
- 继续复用 MoviePilot 的网络代理和 TMDB 配置，配套服务由原作者仓库提供。

## 配置

| 设置 | 说明 |
| --- | --- |
| 启用插件 | 启动插件和配套服务，默认关闭 |
| 端口 | 配套服务监听端口，默认 `8632`，需避免端口冲突 |
| 启用元数据修正 | 执行季集修正，默认开启 |
| 优先使用来源分季 | 优先按来源的 `seasons` 累计集数修正 |
| 按播出窗口推断季号 | 在标题没有明确季号时按发布时间推断 |
| 集数越界宽限 / 改写阈值 | 控制修正容差和触发条件 |
| Bangumi API / 使用代理 | 配置数据源连接及是否复用 MoviePilot 代理 |
| 来源 | 分季数据地址，可刷新缓存或上传本地来源文件 |
| 识别排除 | 命中关键词时跳过插件增强，不改变宿主的正常识别和下载 |

## v0.0.9 修复

MoviePilot 在搜索完成后的资源匹配阶段，会向 `match_torrent` 传入 `season_episodes`（季集范围）。旧插件替换函数只接受三个参数，导致候选结果已逐步出现，最终却报搜索失败。

本版将宿主额外参数原样转交原匹配方法，保留季集范围判断、匹配返回值和成功后的修正回调。未新增参数的旧调用方式继续可用；底层错误仍正常向上传播。

## 开发验证

```bash
python -m pytest tests -q
python -m compileall -q plugins.v3 tests scripts
python scripts/build_release.py --output-dir dist
```

测试隔离宿主配置与网络，覆盖搜索参数兼容、修正回调、补丁恢复、同步/异步识别和累计集数转换。发布包只包含插件源码，不附带日志、凭据、缓存或服务二进制。

## 来源

- 本仓库提取基线：`shyblacktea/MoviePilot-Plugins@12a8c5ff0b7d466abd520e23643ca4d43398dc72`，插件版本 `0.0.8`。
- 上游实现：[CTMDbA 魔改版](https://github.com/shyblacktea/MoviePilot-Plugins/tree/main/plugins.v3/curetmdbanimeshy)。
- 原始插件：[wikrin/MoviePilot-Plugins](https://github.com/wikrin/MoviePilot-Plugins)。
- 配套服务及二进制：[wikrin/CureTMDbAnime](https://github.com/wikrin/CureTMDbAnime)，当前服务版本 `1.4.0`。

提取时上游仓库未声明根目录许可证，本仓库保留原作者信息与来源，未额外授予上游代码的新许可。
