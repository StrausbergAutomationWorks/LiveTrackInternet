# Live Track Internet

[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Nederlands](README.nl.md) · **简体中文** · [Español](README.es.md) · [Italiano](README.it.md) · [Українська](README.uk.md) · [العربية](README.ar.md) · [所有语言](#语言)

**为 Home Assistant 提供互联网中断、海底光缆和光纤链路，全部在一张地图上。**
Live Track Internet 把 Cloudflare Radar 在世界各地记录的互联网中断连同原因放到
你的 Home Assistant 地图上。它还会画出每一条海底光缆及其登陆点，以及国际电联
（ITU）记录的城镇之间的光纤和微波链路。当某次中断提到一条光缆时，这条光缆会
画成红色。

> **Live Track Internet 是 Live Track 的一个模块**。Live Track 是一组 Home
> Assistant 集成，把所有移动的东西以及它们穿越的天气画在同一张共享地图上：
> 飞机、船舶、火车和天气。可以单独安装，也可以和其他模块一起安装
> （[见下方列表](#live-track-的组成部分其他模块)）。

> **正在扩展，欢迎提出想法。** 目前 Live Track Internet 覆盖全世界的中断、
> 光缆和陆地链路，我们正在添加更多数据源（计划加入互联网交换中心和数据
> 中心）。缺少什么吗？[提出建议](#帮助它成长)，或者自己添加：我们会帮助你
> 完成。

**状态：0.3.4，已发布。** 已在 Marketplace 的目录中（[安装方法见下文](#安装步骤)）。

StrausbergAutomationWorks 的原创作品。与 Cloudflare、Tristan Hotham、
TeleGeography、国际电信联盟（ITU）以及任何光缆所有者或网络运营商均无关联，
也未获其认可。

> ⚠ **这不是对你自己网络连接的监测。** 这些中断是 Cloudflare 的工作人员撰写
> 的记录，常常在中断开始几个小时之后才写，而且只记录大到能从 Cloudflare 的
> 网络看到的中断。**地图上什么都没有，并不代表各地的互联网都正常。** 地图上
> 的光缆或链路也不能说明它今天是否在传输数据。

---

## 目录

1. [全部功能](#全部功能)
2. [适用地区](#适用地区)
3. [Live Track 的组成部分：其他模块](#live-track-的组成部分其他模块)
4. [开始之前](#开始之前)
5. [安装步骤](#安装步骤)
6. [设置步骤](#设置步骤)
7. [解锁更多功能的免费密钥](#解锁更多功能的免费密钥)
8. [把地图放到仪表盘上](#把地图放到仪表盘上)
9. [在自动化中使用](#在自动化中使用)
10. [地图上的全部内容详解](#地图上的全部内容详解)
11. [它创建的全部实体](#它创建的全部实体)
12. [它发送和下载的内容](#它发送和下载的内容)
13. [帮助它成长](#帮助它成长)
14. [语言](#语言)
15. [致谢与许可](#致谢与许可)
16. [关键词](#关键词)

---

## 全部功能

### 地图上的内容，无需任何设置

以下每一项都是一个图层，在地图的图层控件中有自己的复选框。所有图层一开始都是
**关闭**的：勾选复选框即可显示。

| 内容 | 范围 | 来源 |
|---|---|---|
| **全部电缆**：每一条海底光缆，608 条在用、105 条计划中，画成细线；点击可查看名称、所有者、长度和登陆国家 | 全世界 | Tristan Hotham 根据 TeleGeography 光缆数据整理的数据集，随集成一起提供 |
| **登陆点**：光缆上岸的 1,928 个地点，画成小点 | 全世界 | 同上 |
| **陆地链路**：陆地上城镇之间的光纤和微波链路，从一个节点到下一个节点画成直线 | 国际电联收集到这些数据的国家（[哪些地区](#适用地区)） | ITU Broadband Maps（BBmaps），由你的 Home Assistant 每周获取一次 |

### 用你自己的免费密钥或账户启用

| 免费密钥或账户 | 增加的内容 |
|---|---|
| **Cloudflare** API 令牌 | **中断**：Cloudflare Radar 记录的每一次正在发生的互联网中断各有一个标记，位于记录所指的国家或地区，按原因着色和绘制；默认开启。**受影响的电缆**：正在发生的中断所提到的海底光缆，画成粗红线；默认开启 |

几分钟就能获取：[步骤见下文](#解锁更多功能的免费密钥)。

---

## 适用地区

| 地区 | 你能看到什么 | 来源 | 需要 |
|---|---|---|---|
| **全世界** | 互联网中断，位于每条记录所指的国家或地区 | Cloudflare Radar | 免费令牌 |
| **全世界** | 受影响的海底光缆 | Cloudflare Radar 和光缆数据 | 免费令牌 |
| **全世界** | 全部海底光缆和登陆点 | Tristan Hotham 根据 TeleGeography 数据整理的数据集 | 无 |
| **非洲和中东** | 约 5,400 条陆地链路 | ITU Broadband Maps | 无 |
| **中美洲和南美洲** | 约 5,500 条陆地链路 | ITU Broadband Maps | 无 |
| **欧洲** | 约 12,400 条陆地链路 | ITU Broadband Maps | 无 |
| **北美洲** | 约 4,700 条陆地链路 | ITU Broadband Maps | 无 |
| **大洋洲** | 约 1,400 条陆地链路 | ITU Broadband Maps | 无 |
| **俄罗斯、北亚和东亚** | 约 1,500 条陆地链路 | ITU Broadband Maps | 无 |
| **南亚和东南亚** | 约 9,500 条陆地链路 | ITU Broadband Maps | 无 |

链路数量于 2026 年 11 月 25 日测得，是粗略数字：每条链路按其第一个端点计数。
国际电联总共发布约 40,000 条链路。

⚠ **陆地链路的覆盖不均匀。** 国际电联显示的是运营商和监管机构提供给它的数据。
有些国家画得很详细（印度、巴西、欧洲大部分地区）；另一些国家链路很少，或者
没有。

不在列表中？[告诉我们](#帮助它成长)。只要有人公开发布数据，我们就会考虑加入。

---

## Live Track 的组成部分：其他模块

Live Track 是一组 Home Assistant 集成，每种移动的东西对应一个，全部画在同
一张地图卡片上。每个集成都能单独使用；合在一起就构成一幅实时画面。它们共用
地图卡片和一个 Python 库
（[saw-livetrack](https://github.com/StrausbergAutomationWorks/LiveTrackCore)），
因此多安装一个集成，不会对另一个集成已在读取的数据源增加任何请求。

| 模块 | 它在地图上显示什么 | 状态 |
|---|---|---|
| [Live Track Aircraft](https://github.com/StrausbergAutomationWorks/LiveTrackAircraft) | 通过 ADS-B 显示头顶上的飞机，含航线和机型图标 | 已发布 |
| [Live Track Ships](https://github.com/StrausbergAutomationWorks/LiveTrackShips) | 通过 AIS 显示附近或任何地方的船舶 | 已发布 |
| [Live Track Commuter Rail](https://github.com/StrausbergAutomationWorks/LiveTrackCommuterRail) | 北美、欧洲和澳大利亚的通勤列车 | 已发布 |
| [Live Track Intercity Rail](https://github.com/StrausbergAutomationWorks/LiveTrackIntercityRail) | 北美、欧洲和澳大利亚的城际和长途列车 | 已发布 |
| [Live Track SALT](https://github.com/StrausbergAutomationWorks/LiveTrackSALT) | 移民和联邦执法机构的飞机和船只，来自公开名单 | 已发布 |
| [Live Track Weather](https://github.com/StrausbergAutomationWorks/LiveTrackWeather) | 天气、风暴和自然灾害 | 已发布 |
| **Live Track Internet** | 互联网中断、海底光缆和陆地链路（本模块） | 已发布 |
| Live Track Stations | 每个车站的发车时刻表和"该出发了"提醒 | 计划中 |
| Live Track Satellites | 从头顶经过的卫星 | 计划中 |
| Live Track Freight Trains | 铁路公司公布的货运和工程列车 | 计划中 |
| Live Track Transit | 城市公交、有轨电车、渡轮和地铁 | 计划中 |
| Live Track Intercity Buses | 城际和区域长途客车 | 计划中 |
| Live Track Commuter Buses | 通勤巴士 | 计划中 |
| [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard) | 每个模块都在其上绘制的共享地图卡片 | 已发布，随每个模块安装 |

全部免费且开源。没有任何功能只留给赞助者。

---

## 开始之前

* **Home Assistant** 2026.11 或更高版本。
* 你的 Home Assistant 中装有 **Marketplace**（HACS），便于安装和更新。没有
  它也可以手动复制文件。
* Home Assistant 能**访问互联网**：中断和陆地链路来自公共服务。
* 光缆和链路无需付费，也无需账户。上面的免费 Cloudflare 令牌是可选的。
* 集成第一次加载时，Home Assistant 会自动安装它需要的 Python 包
  （`saw-livetrack`）。

---

## 安装步骤

### 通过 Marketplace（推荐）

1. 在 Home Assistant 中打开 **设置 → Marketplace**（HACS）。
2. 搜索 **Live Track Internet** 并打开它。
3. 选择 **下载**（或 **安装**）。
4. **重启 Home Assistant**：**设置 → 系统 → 修复** 会提供重启，或者使用
   **设置 → 系统 → 重启 Home Assistant**。

如果搜索找不到它，就通过链接添加：选择 **从链接添加** 选项卡（或三点菜单 → **自定义存储库**），输入 `StrausbergAutomationWorks/LiveTrackInternet`，如果询问类型，选择 **集成**，然后从第 3 步继续。

之后，Marketplace 会把每个新版本作为更新提供给你。

### 手动安装

1. 下载[最新版本](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/releases/latest)
   的源代码。
2. 把其中的 `custom_components/live_track_internet` 文件夹复制到 Home
   Assistant 配置文件夹中的 `custom_components` 文件夹（如果没有
   `custom_components`，请创建）。
3. 重启 Home Assistant。

手动更新时，用新版本的文件夹替换旧文件夹，然后重启。

---

## 设置步骤

1. 打开 **设置 → 设备与服务**。
2. 选择 **添加集成**（右下角），搜索 **Live Track Internet**。
3. **Cloudflare API 令牌**：如果你有令牌，把它粘贴进来
   （[如何获取](#解锁更多功能的免费密钥)）。留空则只显示光缆和链路；以后可以
   再添加令牌。
4. **来自国际电联的陆地链路**：保持勾选。如果你不希望 Home Assistant 每周
   从国际电联获取一次链路（约 1 MB），就取消勾选。
5. 选择 **提交**。

就这样。有令牌时条目名为 **Cloudflare Radar**，没有令牌时名为
**Submarine cables**。只能有一个条目：第二个条目会把每次中断画两遍，所以会被
拒绝。

* 光缆和登陆点图层会立即出现。
* 有令牌时，正在发生的中断会在一分钟内出现。
* 陆地链路会在设置后几分钟出现，也就是第一次从国际电联获取完成之后。

每个图层一开始都是关闭的。在地图的图层控件中勾选它就能看到
（[把地图放到仪表盘上](#把地图放到仪表盘上)）。

### 以后更改令牌或国际电联复选框

1. 打开 **设置 → 设备与服务 → Live Track Internet**。
2. 打开该条目的三点菜单，选择 **重新配置**。
3. 粘贴新的令牌，或者留空以保留现有令牌。勾选或取消勾选
   **来自国际电联的陆地链路**。
4. 选择 **提交**。

要移除令牌，请删除该条目（同一菜单中的 **删除**），然后不带令牌重新添加
Live Track Internet。如果以后 Cloudflare 拒绝了你的令牌（令牌被删除或已过期），
中断标记就会停止，Home Assistant 会在 **设置 → 设备与服务** 中请你提供新的
令牌。

---

## 解锁更多功能的免费密钥

令牌是免费的，也是个人的：每个安装 Live Track Internet 的人都自己创建一个。
你需要一个免费的 Cloudflare 账户；不需要在 Cloudflare 上有网站或域名。

### Cloudflare API 令牌（互联网中断，全世界）

1. 在 <https://dash.cloudflare.com> 登录 Cloudflare，或创建一个免费账户。
2. 打开 <https://dash.cloudflare.com/profile/api-tokens>（**My Profile → API
   Tokens**），选择 **Create Token**。
3. 不要使用模板：从头开始，创建一个自定义令牌。给它起个名字，例如
   `Live Track Internet`。
4. 在权限中依次选择 **Account**、**Radar**、**Read**。其他都不需要。
5. 选择 **Continue to summary**，然后选择 **Create Token**。
6. 立即复制令牌：Cloudflare 只显示一次。
7. 在[设置](#设置步骤) Live Track Internet 时把它粘贴到
   **Cloudflare API 令牌** 中，或以后通过 **重新配置** 粘贴。

Live Track Internet 在保存令牌之前，会向 Cloudflare Radar 发出一次真实请求来
检查它。令牌保存在你的 Home Assistant 中，只发送给 Cloudflare。除了令牌，不需要
任何密码或其他机密。这里的按钮名称是 Cloudflare 英文界面上的名称；如果
Cloudflare 以中文显示页面，名称会不同。

---

## 把地图放到仪表盘上

地图是 [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard)，
也就是每个 Live Track 模块都在其上绘制的卡片。**它随 Live Track Internet 一起
安装**：无需下载，无需复制，也无需添加资源。

1. 打开一个仪表盘，选择铅笔图标（**编辑仪表盘**），然后选择 **添加卡片**。
2. 滚动到底部，选择 **手动**。
3. 粘贴以下内容，然后选择 **保存**：

```yaml
type: custom:live-track-map-card
entity_filter:
  include:
    - domain: geo_location
      attributes:
        source: live_track_internet
      options:
        display: attribute
        attribute: marker_label
  exclude:
    - state: unavailable
```

光缆和链路图层会自动出现。中断标记通过上面的过滤器显示。

其他 Live Track 模块也以同样方式放进 `entity_filter`：每个数据源再加一条
`- domain: geo_location` 规则。

**地图上：**

* 右上角的**图层控件**为每个图层提供一个复选框：**受影响的电缆**、
  **全部电缆**、**登陆点** 和 **陆地链路**。每位查看者的选择都保存在他自己的
  浏览器中。
* 每次中断都是一个表示原因的圆形图片，旁边是国家的两字母代码。把指针**移到**
  上面可以看到地点和原因；**点击**可查看 Cloudflare 的描述、报道链接，以及该中断提到的每个网络、地区或国家在 Cloudflare Radar 上的流量页面（从中断开始的前一天起，最多四个链接）。
* **点击**一条光缆可查看名称、所有者、长度和登陆国家。陆地链路不能点击。
* **过滤卡片**（`custom:live-track-map-filter-card`）可以按原因隐藏中断。
* 只要显示了某个来源的数据，该来源的署名就会出现在地图的署名行中。

这张卡片为所有 Live Track 模块合起来只保留一行仪表盘资源：使用其中任一模块
携带的最新卡片版本，绝不会是旧版本。你自己通过 Marketplace 安装的卡片不会被
改动。如果你的仪表盘资源是在 YAML 中设置的（`lovelace: resource_mode: yaml`），
就无法为你自动注册：此时 **修复** 中会出现一个问题，给出需要添加的确切行，
样子如下，其中的占位符会换成该集成自己的地址：

```yaml
lovelace:
  resource_mode: yaml
  resources:
    - url: /live_track_internet/map-card/<12 hex>/live-track-map-card.js?v=<version>&h=<12 hex>
      type: module
```

删除 Live Track Internet 的条目时，这一行会交给另一个 Live Track 模块；如果
没有其他模块了，这一行就会被移除。如果集成的文件被移除，而它的条目仍然存在，
并且没有安装其他 Live Track 模块，请自己在 **设置 → 仪表盘 → 资源** 中移除
卡片的那一行。如果想手动安装卡片，请按照卡片的 README 操作。你自己创建的行
（用于 `/local/` 下的副本或任何其他地址）永远不会被更改或移除。只要它在加载
这张卡片，每个 Live Track 模块都会把卡片交给它，即使某个模块带有更新的版本，
**修复** 中也不会提示。要改回使用模块自带的副本，请在 **设置 → 仪表盘 → 资源**
中移除你的那一行，然后重启 Home Assistant。如果你删除了自己副本的文件，也请
移除它的那一行：只要文件已不存在的行还在，模块就不会添加自己的行。任何其他
显示 `geo_location` 实体的地图卡片也会显示中断标记，但不会显示光缆或链路。

---

## 在自动化中使用

所有内容都是普通的 Home Assistant 实体，所以自动化编辑器可以直接使用，不需要
写代码。

**当 Cloudflare 记录到新的互联网中断时，向手机发送通知**（需要 Cloudflare 令牌）：

1. **设置 → 自动化与场景 → 创建自动化 → 创建新的自动化**。
2. **每当**：**添加触发条件**，在搜索框中输入 `numeric`，选择
   **数值状态已跨越阈值**。**实体** 选择 **Cloudflare Radar 互联网中断**，
   在 **高于** 中输入 `0`。
3. **就执行**：**添加动作**，搜索你手机的通知动作（它带有你手机的名称），
   然后输入一条消息，例如：

   ```text
   Cloudflare Radar 报告了一次互联网中断
   ```

4. **保存**。

**其他想法：** 当某次中断提到一条海底光缆时发送通知，使用
**Submarine cables 受影响的电缆** 高于 0；在仪表盘上放一个磁贴显示正在发生的
中断数量，来自 **Cloudflare Radar 互联网中断**。

---

## 地图上的全部内容详解

### 中断

[Cloudflare Radar](https://radar.cloudflare.com) 维护着一个 Outage Center：
由 Cloudflare 的工作人员撰写的全球互联网中断记录，每条都有原因、类型（全国、
地区或单个网络）、受影响的国家或地区、开始时间，通常还有一个新闻报道链接。

Live Track Internet 每 15 分钟获取一次过去 24 小时的记录，并为每条正在发生的
记录在它提到的每个地点画一个标记：记录提到地区时画在该地区，否则画在该国家。
记录结束后，标记会从地图上消失。关于某项在线服务而不是某个地点的记录（例如
某个云服务商的中断）不会画出；传感器 **Cloudflare Radar 互联网中断** 会在其
`not_on_map` 属性中列出它们。

⚠ **只提到一个网络的记录会放在该国家的中心**，在大国中这可能离中断地点很远。
点击后的文字会说明这一点。例如，Cloudflare 把卢甘斯克和顿涅茨克（乌克兰）的
两个网络归在俄罗斯名下，所以它们的中断被放在西伯利亚中部；美国的网络则被放在
堪萨斯州。

⚠ 中断记录是人工撰写的，常常在中断开始几个小时之后。我们测量了一年的记录
（截至 2026 年 11 月 23 日），共 143 条，同时进行中的从未超过 4 条，有 43% 的
时间一条也没有。大多数时候，地图上根本没有中断。

每个标记按原因绘制：

| 原因 | 颜色 | 图片 |
|---|---|---|
| 光缆切断 | 红色 | 张开的剪刀 |
| 停电 | 琥珀色 | 闪电 |
| 政府指令（断网） | 靛蓝色 | 挂锁 |
| 军事行动 | 黑色 | 准星 |
| 天气或自然灾害 | 蓝色 | 雷雨云 |
| 网络攻击 | 青绿色 | 带 `!` 的盾牌 |
| 技术问题（网络、软件、DNS、维护） | 蓝灰色 | 扳手 |
| 原因不明 | 灰色 | `?` |

每个标记上有：`outage_cause` 和 `outage_type`（Cloudflare 自己的用词，例如
`POWER_OUTAGE`、`NATIONWIDE`）、`started_at`、`place_kind`（`region`、`country`
或 `network`）、`country_code`、`country_name`、`region_name`、记录提到网络时的
`asns` 和 `asn_names`、`description`、`linked_url`（报道）、`marker_links`（点击时显示的链接）、描述提到光缆时的
`cables_named`，以及 `marker_group`（原因，供过滤卡片使用）。

### 受影响的电缆

有 Cloudflare 令牌时，正在发生的中断的描述中提到的每一条海底光缆都会画成带白边
的粗红线，默认开启。通常一条也没有。光缆按名称识别，常见写法都能识别
（`SEA-ME-WE 5`、`SeaMeWe-5`）；短名称只按完整单词匹配。

⚠ Cloudflare 的原因字段并不说明被切断的光缆是不是海底光缆：在我们测量的那一年，
唯一一条标为光缆切断的记录是陆地上的光缆，而 SEA-ME-WE 5 光缆的一次故障被标为
原因不明。所以无论原因是什么，都会在描述中查找光缆。

### 全部电缆和登陆点

Tristan Hotham 2026 年根据 TeleGeography 光缆数据整理的数据集中的每一条海底
光缆：713 条，其中 608 条在用（画成蓝色）、105 条计划中（画成橙色），画成又细
又淡的线；以及 1,928 个登陆点，画成小点（只有计划中光缆登陆的地方为橙色）。
点击一条光缆，可查看名称、已投入或计划投入使用的日期、长度、登陆国家、所有者
和供应商。这些数据随集成一起提供，只会随新版本而改变。

⚠ 在数据集制作之后（2026 年 11 月）铺设的光缆，要等到带有更新数据的版本发布后
才会出现。

### 陆地链路

国际电联的 Broadband Maps（Infrastructure Connectivity Map）记录的陆地光纤和
微波链路，数据来自运营商和监管机构。每条链路都按国际电联发布的样子画出：从一个
节点到下一个节点的直线，而不是光缆在地面上的实际走向。

| 线条 | 含义 |
|---|---|
| 梅紫色 | 光纤，运行中 |
| 带黑边的黄色 | 微波，运行中 |
| 橙色 | 计划中、拟建或在建（微波带黑边） |
| 灰色 | 未注明状态（微波带黑边） |

⚠ 按地图上又细又淡的线宽，微波线看起来更像橄榄色或卡其色，而不是黄色；靠黑边
才能把它们和光纤区分开。

⚠ 国际电联没有记录链路的运营商、名称、容量或日期，所以链路不能点击，也不会和
任何中断关联。

你的 Home Assistant 每周在它自己的某一天、某一小时从国际电联获取一次整个图层，
并保存下来。如果某次获取失败或不完整，就继续使用上一份完好的副本，不管它有多旧。

---

## 它创建的全部实体

| 实体 | 含义 |
|---|---|
| `sensor.live_track_internet_outages` | **Cloudflare Radar 互联网中断**：地图上有多少个中断标记（仅在有令牌时） |
| `sensor.live_track_internet_cables_in_trouble` | **Submarine cables 受影响的电缆**：正在发生的中断提到了多少条光缆（仅在有令牌时） |
| `sensor.live_track_internet_all_cables` | **Submarine cables 全部电缆**：光缆数量，713 |
| `sensor.live_track_internet_landing_points` | **Submarine cables 登陆点**：登陆点数量，1,928 |
| `sensor.live_track_internet_terrestrial_links` | **ITU Broadband Maps 陆地链路**：画出了多少条链路（仅在勾选 **来自国际电联的陆地链路** 时） |
| `geo_location.outage_…` | 每次正在发生的中断在每个地点各一个，按 Cloudflare 的记录编号命名（`geo_location.outage_1754`）；随记录出现和消失 |

每个标记都带有 `source: live_track_internet`，其状态是它到你家的距离，单位为
公里。这些传感器属于三个设备：**Cloudflare Radar**、**Submarine cables** 和
**ITU Broadband Maps**。

中断传感器的属性：`open_records`（所有正在发生的记录，包括不在地图上的）、
`not_on_map` 和 `last_success`。

⚠ **这些标记有意不设唯一 ID。** 中断记录来来去去，为每条记录都建一行注册表会
永远留在那里。因此无法在界面中给它们改名、隐藏或分配区域。传感器有唯一 ID，
可以改名。

每次更新都会变化的属性，以及地图读取的大型列表，都不会写入 Home Assistant 的
历史记录，所以你的数据库不会因此变大。

---

## 它发送和下载的内容

**关于你的位置。** 不会发送。你家的位置只在你的 Home Assistant 内部用来计算
每个标记的距离。Cloudflare 收到的是你的令牌和请求的时间范围；国际电联收到的是
对其链路的请求。光缆数据随集成一起提供，不需要下载。每个服务都能看到你的
网络地址，就像任何网站一样。

**数据量。** 大小于 2026 年 11 月 25 日测得，表中另有注明的除外。

| 来源 | 内容和频率 | 测得的大小 | 出错之后 |
|---|---|---|---|
| Cloudflare Radar，中断 | 每 15 分钟一次请求，使用你的令牌：过去 24 小时的记录 | 传输 447 字节（一条记录） | 令牌被拒绝时停止请求，并请你提供新令牌。HTTP 429：按 Cloudflare 要求的时间等待，或等 15 分钟，加倍直至 2 小时。其他错误：在 15、30 和 60 分钟后重试，之后每 2 小时一次。上一次完好的回答保留 2 小时；之后标记消失 |
| Cloudflare Radar，地点 | 各国中心点每天一次；某个地区的点在记录第一次提到它时获取，之后保留 | 国家列表：36,905 字节（2026 年 11 月 23 日） | 继续使用你已有的副本 |
| ITU Broadband Maps | 每周一次获取整个图层，分 9 次请求，间隔 3 秒，共约 36 秒 | 传输约 0.9 MB（每 5,000 条链路 111,537 字节） | HTTP 429：按国际电联要求的时间等待，或等一小时，加倍直至一天。其他错误：第二天重试。上一份完好的副本保留 |
| 你的浏览器 | 来自你的 Home Assistant，而不是互联网：勾选 **全部电缆** 时获取光缆文件，勾选 **登陆点** 时获取登陆点，勾选 **陆地链路** 时获取链路文件 | 光缆 113,323 字节；登陆点 38,160 字节；链路 296,105 字节 | |

取消勾选 **来自国际电联的陆地链路**（**重新配置**）即可停止每周获取。删除条目
即可停止全部。

下载的文件保存在 Home Assistant 的 `.storage` 文件夹中，文件名以 `saw_` 开头
（`saw_radar_locations.json`、`saw_radar_geolocations.json`、
`saw_itu_bbmaps_links.json.gz`），以便其他 Live Track 模块共用。如果你移除了
Live Track Internet，且没有其他 Live Track 模块使用它们，可以手动删除。

---

## 帮助它成长

Live Track Internet 仍在成长。我们发现新的数据源时就会添加，也想知道你接下来
希望看到什么。

### 提出建议

缺少某个数据源？有什么错误或难以理解的地方？用对你最方便的方式告诉我们：

* [**填写一份简短的表单**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=zh-Hans.yml)
  （中文）。你需要一个免费的 GitHub 账户。
* **发送电子邮件**到
  [StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org)。
  不需要账户。

无论哪种方式，告诉我们以下内容会有帮助：

* 你希望看到什么，以及在世界上的哪个地方；
* 数据发布位置的链接（如果你知道的话，例如开放数据页面、公开数据源或某项服务
  的网站）：不是必需的，但会有帮助；
* 你的 Home Assistant 语言（如果问题涉及措辞或翻译）。

用英文或你自己的语言书写都可以，哪种方便就用哪种。

### 在我们的帮助下自己添加

如果你想自己添加内容，我们会帮助你完成，从第一个问题一直到最终发布。开始时
你不需要是开发者：

* **翻译。** 设置对话框中的文字是一个文本文件里的一小段短语列表。我们会告诉
  你是哪个文件、哪些行。
* **新的数据源。** 告诉我们数据在哪里发布。我们可以一起编写代码，或者帮你
  检查你写的代码。
* **在你居住的地方测试。** 安装它，查看地图上你所在的区域，告诉我们哪些正确、
  哪些不正确。
* **修正本 README。** 如果某个步骤和你看到的不一致，告诉我们你看到了什么。

[**告诉我们你的想法**](https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues/new?template=zh-Hans.yml)
或写信到
[StrausbergAutomationWorks@recordwise.org](mailto:StrausbergAutomationWorks@recordwise.org)，
我们会回复你接下来的步骤。

---

## 语言

本 README：[English](README.md)、[Deutsch](README.de.md)、
[Français](README.fr.md)、[Nederlands](README.nl.md)、**简体中文**、
[Español](README.es.md)、[Italiano](README.it.md)、
[Українська](README.uk.md) 和 [العربية](README.ar.md)。每份翻译的 README 都是
完整的，但都还没有经过母语者审阅。如果其中有你的母语，请告诉我们它读起来是否
通顺：见[帮助它成长](#帮助它成长)。

当你的 Home Assistant 语言是以下之一时，设置对话框会以该语言显示：English、
Deutsch、Español、Français、Italiano、Nederlands、简体中文、Українська 和
العربية。其他语言显示英文。对话框的翻译也没有经过母语者审阅。地图上的文字
（中断的名称和点击后的文字、过滤卡片中的原因名称以及署名）在所有语言中都是
英文。

发现翻译有误，或需要其他语言？请在
<https://github.com/StrausbergAutomationWorks/LiveTrackInternet/issues> 告诉我们，或者
[在我们的帮助下翻译](#在我们的帮助下自己添加)。

---

## 致谢与许可

* **Cloudflare Radar**（Cloudflare, Inc.，<https://radar.cloudflare.com>）：
  中断记录，采用
  [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可，使用
  每位用户自己的令牌读取。本集成把每条记录放到地图上；不修改记录内容。安装本
  集成即表示你在使用 Cloudflare 的 API，其条款适用于你。
* **海底光缆和登陆点**：Hotham, T. (2026), *The internet's seabed: submarine
  cables, when they were laid, who owns them and where they crowd together*,
  Zenodo, <https://doi.org/10.5281/zenodo.23856607>，源自 TeleGeography 的
  [Submarine Cable Map](https://www.submarinecablemap.com/)，采用
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可。
  本集成把光缆线路与光缆表关联起来，把两者转换为地图文件，并把登陆点四舍五入
  到小数点后 4 位；没有添加或更正任何内容。
  `custom_components/live_track_internet/cables/` 中转换后的文件以相同许可共享，
  旁边附有许可的法律文本和一份署名文件
  （[CREDIT.md](custom_components/live_track_internet/cables/CREDIT.md)）。
* **陆地链路**：ITU Broadband Maps（BBmaps），即 Infrastructure Connectivity
  Map，<https://bbmaps.itu.int>，© ITU。根据国际电联的使用条款用于非商业用途，
  并注明来源。本仓库不附带任何国际电联的数据：每个安装都为自己的用户获取链路。
  本集成按国际电联发布的样子绘制，四舍五入到小数点后 3 位（约 110 米），同一
  类型的重复链路只画一次。
* **中断图片** 是为 StrausbergAutomationWorks 绘制的，采用 MIT 许可。
* **地图卡片** 是 [LiveTrackMapCard](https://github.com/StrausbergAutomationWorks/LiveTrackMapCard)，
  MIT，是 nathan-gs 的 [ha-map-card](https://github.com/nathan-gs/ha-map-card)
  （MIT）的副本。其地图瓦片及署名见它的 README。

⚠ **仅限非商业用途。** 三个数据源都只允许非商业使用。代码采用 MIT 许可，但它
显示的数据不得用于商业用途。

上述机构均未制作或认可本集成。哪个许可覆盖本仓库的哪一部分：
[ATTRIBUTION.md](ATTRIBUTION.md)。

**代码**：MIT，见 [LICENSE](LICENSE)。

**面向开发者：** 实体遵循 Live Track 共享的地图约定，因此每个模块都显示在同一张
地图上。`tools/build_cables.py` 从 Hotham 的仓库重新生成光缆文件。测试用
`python -m unittest discover -s tests` 运行。

---

## 关键词

Home Assistant 互联网中断 · 断网 · 断网地图 · 互联网封锁 · 网络中断 · 宽带故障 ·
运营商故障 · Cloudflare Radar · Radar Outage Center · 海底光缆 · 海底电缆 ·
海缆地图 · 光缆切断 · 光缆登陆点 · TeleGeography · Submarine Cable Map ·
陆地光纤 · 光纤地图 · 光纤骨干网 · 微波链路 · 国际电联 · ITU · ITU Broadband
Maps · BBmaps · Infrastructure Connectivity Map · internet outage · submarine
cables · Internetausfall · Seekabel · panne internet · câbles sous-marins ·
internetstoring · zeekabels · corte de internet · cables submarinos ·
interruzione internet · cavi sottomarini · відключення інтернету · підводні
кабелі · انقطاع الإنترنت · كابلات بحرية · geo_location · 地图卡片 · Lovelace ·
HACS · Marketplace · Live Track · LiveTrack · StrausbergAutomationWorks

---

**致敬。** StrausbergAutomationWorks 向这张地图上世界各地陆地和水域的原住民族致意，并向他们过去和现在的长老致敬。
