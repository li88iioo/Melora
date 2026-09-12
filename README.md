# 乐屿 · Melora

<p align="center">
  <strong>轻量、优雅的自托管音乐 Web 应用，专为飞牛 fnOS 与私有 NAS / Linux 环境设计</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.0.1-blue.svg" alt="version" />
  <img src="https://img.shields.io/badge/backend-Go%201.25+-00ADD8.svg" alt="Go" />
  <img src="https://img.shields.io/badge/frontend-React%2019%20%2B%20TypeScript-61DAFB.svg" alt="React" />
  <img src="https://img.shields.io/badge/platform-fnOS%20%7C%20Linux%20(amd64%2Farm64)-orange.svg" alt="Platform" />
  <img src="https://img.shields.io/badge/license-Private%20%2F%20Custom-green.svg" alt="License" />
</p>

---

## 💡 核心设计理念

- **浏览器直连播放**：浏览器直接拉取外部媒体播放，NAS 不做转码、不作无谓的中继代理，极大降低 NAS 硬件占用与上行带宽消耗。
- **封面直连优先**：列表图片默认懒加载并由浏览器直连平台 CDN；仅客户端直连失败时回退到带域名白名单与缓存的 `/api/v1/covers` 同源代理，避免让 NAS/VPS 承担正常图片流量。
- **NAS 按需离线下载**：仅在用户明确需要保存歌曲时，由后台独立的 Go 下载 Worker 安全拉取并写入指定音乐目录。
- **极简部署，单二进制**：Go 高性能后端 + Vite/React 静态资源 + 内置 SQLite，单二进制独立运行，**NAS 端无需安装 Node.js、Python 或额外容器运行时**。
- **沙箱隔离的音源解析**：提供轻量独立的 JavaScript 隔离运行环境，安全执行用户导入的自定义音源脚本。

---

## ✨ 核心特性

### 1. 🎵 聚合音乐目录与搜索
- 整合主流音乐平台公开目录，支持实时榜单浏览、新歌推荐与分类歌单发现。
- 跨平台歌曲搜索与歌手聚合，无需在多个客户端之间频繁切换。

### 2. 📖 听书
- 小说专区与热播榜、VIP 会员榜、有声小说分类榜、口碑榜、畅销榜浏览。
- 有声专辑章节分页展示与整页连播，播放链路与普通歌曲一致；搜索页提供「有声书」标签。

### 3. 🧩 LX 自定义音源扩展
- 兼容导入主流 LX 自定义音源脚本，利用脚本动态解析歌曲的高品质直链与播放地址。
- 独立的音源隔离环境与请求沙箱保护，拦截敏感内网访问，兼具灵活性与安全性。
- 播放与下载均接入**智能自动换源机制**，当首选音源不可用时自动尝试候选音源无缝切换。

### 4. 🎨 现代沉浸式视听体验
- **响应式双端适配**：桌面端优雅的左右分栏布局（左侧唱片封面/主控 + 右侧全高同步歌词）；移动端定制底部抽屉与沉浸播放器。
- **Dynamic Ambient Canvas 动态氛围感**：从歌曲封面实时提取主色调，结合平滑渐变与噪点渲染出随曲目流动的背景氛围，自动适配深色模式。
- **人性化交互细节**：多级歌词字号切换、断点恢复（浏览器重新打开时恢复队列与曲目）、沉浸状态防误触优化。

### 5. 📥 智能安全下载与元数据内嵌
- **高品质格式支持**：支持下载无损 FLAC、高码率 MP3 以及 M4A 音频。
- **自动内嵌标签**：下载完成时自动将歌曲名、歌手、专辑、高清封面与 LRC 滚动歌词直接内嵌至音频文件（ID3v2 / VorbisComment / MP4 Tags），保持音乐库整洁规范。
- **健壮传输管理**：支持分段校验、断点续传、重名智能防覆盖；提供完备的下载任务列表与一键清理历史记录能力。

### 6. 📦 飞牛 fnOS 深度适配 (FPK)
- 遵循飞牛原生 FPK 规范，打包产物包含 `amd64` 与 `arm64` 架构安装包。
- 深度适配 fnOS 用户权限机制、Unix Socket 通信及应用生命周期管理（安装、启动检查、更新、安全卸载）。

---

## 🏗️ 项目架构

```text
乐屿 · Melora
├── apps/
│   ├── web/                     # 前端应用 (React 19 + TypeScript + Vite)
│   │   ├── src/
│   │   │   ├── components/      # UI 组件 (播放器、沉浸画布、下载弹窗、歌曲列表等)
│   │   │   ├── pages/           # 页面路由 (发现、榜单、听书、搜索、我的音乐、下载、设置)
│   │   │   ├── stores/          # 全局状态管理 (播放会话、队列、设置持久化)
│   │   │   └── lib/             # API 客户端、色彩提取、音质格式化等工具库
│   │   └── tests/               # Playwright 端到端 (E2E) 测试套件
│   └── server/                  # 后端应用 (Go 原生高并发服务)
│       ├── cmd/melora/          # 服务端主入口程序
│       └── internal/
│           ├── api/             # RESTful API 路由、SSE 事件推送与鉴权
│           ├── catalog/         # 公开音乐目录与榜单爬取适配
│           ├── config/          # 环境配置与目录授权校验
│           ├── download/        # 安全下载管道、分段校验与状态机
│           ├── downloadassets/  # 音频元数据（ID3/FLAC/MP4）与封面内嵌工具
│           ├── lxruntime/       # LX 脚本独立轻量 JS 沙箱运行时
│           ├── lxsource/        # 音源导入、存储与生命周期管理
│           ├── netguard/        # 网络出站守卫与 DNS/SSRF 安全防护
│           ├── provider/        # 音乐解析提供者与自动换源调度
│           └── store/           # SQLite (WAL 模式) 数据访问层
├── packaging/                   # 飞牛 fnOS 原生 FPK 打包模板、向导与自动化脚本
└── scripts/                     # 开发调试、交叉编译与打包辅助脚本
```

---

## 🚀 快速开始

### 开发环境依赖
- **Node.js** >= 22.12.0
- **Go** >= 1.25
- **npm** >= 10.0.0

### 1. 克隆代码与安装依赖

```bash
git clone <repository_url>
cd "乐屿 · Melora"

# 安装前端与项目脚本依赖
npm install
```

### 2. 启动全栈本地开发服务

```bash
npm run dev
```
> 该命令会同时启动 Vite 前端开发服务器（热更新）与 Go 后端 API 服务。前端默认运行在 `http://127.0.0.1:5173`。

也可根据需要独立调试单端：
```bash
# 仅启动前端开发服务
npm run dev:web

# 仅启动服务端开发服务
npm run dev:server
```

---

## 🛠️ 构建与发布

### 1. 编译生产二进制与前端资源

```bash
npm run build
```
执行后将生成：
- `apps/web/dist/`：打包压缩后的前端静态资源
- `dist/melora-linux-amd64`：Linux amd64 独立可执行文件
- `dist/melora-linux-arm64`：Linux arm64 独立可执行文件

### 2. 独立运行编译产物

```bash
WEB_DIR="$PWD/apps/web/dist" \
MELORA_DATA_DIR="$PWD/data" \
./dist/melora-linux-amd64
```
访问 `http://127.0.0.1:3780` 即可使用，整个运行期无任何外部依赖。

默认只允许回环地址提供 HTTP 服务。若必须直接监听局域网地址，需要同时设置强访问令牌并显式确认明文 HTTP 风险：

```bash
MELORA_ADDR="0.0.0.0:3780" \
MELORA_AUTH_TOKEN="请替换为至少32字节的随机令牌" \
MELORA_ALLOW_INSECURE_HTTP=1 \
WEB_DIR="$PWD/apps/web/dist" \
MELORA_DATA_DIR="$PWD/data" \
./dist/melora-linux-amd64
```

> 局域网明文 HTTP 会暴露会话与访问令牌，建议优先保持回环监听，并通过启用 HTTPS 的反向代理发布服务。`MELORA_ALLOW_INSECURE_HTTP=1` 只表示已理解风险，不会提供 TLS 加密。

### 3. 构建飞牛 fnOS FPK 安装包

确保环境中具备官方打包工具 `fnpack`：

```bash
# 构建 amd64 架构 FPK 包
bash scripts/package-fpk.sh --arch amd64 --fnpack /path/to/fnpack

# 构建 arm64 架构 FPK 包
bash scripts/package-fpk.sh --arch arm64 --fnpack /path/to/fnpack

# 若暂无 fnpack，可使用 --stage-only 参数仅生成并验证 staging 目录：
bash scripts/package-fpk.sh --arch amd64 --stage-only
```
打包成功后，产物将生成至 `packaging/out/` 目录下（例如 `melora-<version>-linux-amd64.fpk` 及其 sha256 校验文件）。版本统一读取仓库根 `package.json`。

### 4. 云服务器 Docker 部署（仅在线播放）

云服务器推荐用 `MELORA_DEPLOY_MODE=cloud`：只保留在线播放，**不提供任何下载能力**——下载入口、下载任务 API 与下载设置全部关闭，音频流由浏览器直连音源，不经 Melora 服务器中转。登录使用单管理员账号（`MELORA_ADMIN_USER` 默认 `admin` + `MELORA_ADMIN_PASSWORD`，至少 8 位）。

> **WAF / CC 提示**：不要对整个 SPA 使用传统的“10 秒 100 请求”统一阈值。应区分 HTML/API 写操作、哈希静态资源和 `/api/v1/covers` 兜底请求；Melora 已默认懒加载列表封面并优先直连 CDN，但首次冷加载仍会并发请求必要的 JS/CSS/API。

```bash
cp deploy/.env.example .env   # 设置 MELORA_ADMIN_PASSWORD
docker compose pull
docker compose up -d
```

- Compose 直接拉取 GitHub Container Registry 的 `ghcr.io/li88iioo/melora:0.0.1`，无需在服务器安装 Node.js 或 Go；升级时修改 `.env` 中的 `MELORA_IMAGE_TAG` 后重新拉取
- 默认使用 Linux `host` 网络，Melora 只绑定宿主机 `127.0.0.1:3780`，公网入口必须交给宿主机 nginx；示例见 `deploy/nginx.conf`
- nginx 是唯一可信代理，Compose 固定 `MELORA_TRUSTED_PROXIES=127.0.0.1/32`；应用按真实客户端 IP 限流，不接受其它来源伪造的转发头
- 反代声明 `X-Forwarded-Proto: https` 时，会话 Cookie 自动带 `Secure`，Origin 校验也按 HTTPS 处理
- nginx 对登录接口提供第一道来源 IP 限流，后端继续执行单客户端与全局双重限流
- 数据（收藏、设置、音源）保存在 `melora-data` 命名卷，升级镜像不会丢失
- cloud 模式完全不初始化下载管理器，也不会读取、覆盖或迁移已有下载任务
- 密码未配置时容器会拒绝启动；管理员凭据必须通过 HTTPS 传输

### 5. 版本标签自动发布（GitHub Actions）

推送与 `package.json` 版本一致的 `v*` 标签即可触发 `.github/workflows/release.yml`：

```bash
git tag v0.0.1 && git push origin v0.0.1
```

工作流会先校验标签与 `package.json` 版本一致，并执行格式、类型、单元测试、Go race/vet、打包测试及 Chromium E2E 质量门禁；全部通过后才会串行打包 amd64/arm64 双架构 FPK（官方 fnpack 1.2.3，下载后校验 SHA-256），同时构建并发布 amd64/arm64 GHCR 镜像，最后创建 GitHub Release 并附加 FPK、校验文件及 Docker 部署配置。构建任务默认只有只读仓库权限，仅 Release 步骤获取所需写权限；其他分支推送只运行 CI，不发布。

---

## 🧪 测试与质量验证

项目包含严密的自动化测试套件（单测、端到端 E2E、并发竞争检测）：

```bash
# 1. 静态类型检查与代码风格检查
npm run typecheck
npm run format:check

# 2. 全量单元测试 (Vitest 前端单测 + Go 竞态测试 -race)
npm test

# 3. 运行端到端 E2E 浏览器自动化测试 (Playwright)
npm run test:e2e

# 4. 运行打包生命周期专项测试
npm run test:packaging

# 5. 一次执行格式、类型、单测、竞态、vet 与打包专项检查
npm run check
```

---

## ⚠️ 免责声明与版权提示

1. **本项目为开源技术研究与 NAS 自托管学习作品**，仅提供 Web 界面框架与本地文件管理逻辑。
2. 本项目不提供、不存储、不分发任何音乐音频文件或受版权保护的音源脚本。
3. 播放直链由用户自行导入的第三方脚本解析产生，音频数据流直接由用户客户端与音源提供方通信建立。
4. 请在遵守当地法律法规及所使用平台服务条款的前提下合理合法使用本项目。
