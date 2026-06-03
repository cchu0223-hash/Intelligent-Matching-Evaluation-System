# 智能匹配音色评测平台 - 设计方案（v2026-06-03）

## 1. 目标

构建一个内部评测链接，支持任意知道地址的评测人员输入配音正文，获取 `Top5` 音色推荐，并对每个推荐音色进行试听、评分和文字反馈。

本系统的主要目标不是生产级账号服务，而是沉淀推荐结果与人工反馈数据，用于后续优化音色匹配规则、定位 bad case，并为未来扩展到数字人形象推荐保留结构。

## 2. 范围

本期包含：
- 输入配音正文，最多 `15000` 字。
- 返回 `Top5` 音色推荐。
- 每个推荐音色展示发音人、VCN、一级场景、二级场景、技术标签、性别、语言、试听入口。
- 每个推荐音色必须返回对应标签信息，用于前端展示、用户评审和后续 bad case 归因。
- 每个推荐音色支持 `1-5` 分评分。
- 每个推荐音色支持可选文字建议。
- 后端保存完整输入、推荐结果、调试信息和用户反馈。

本期不包含：
- 复杂账号体系。
- 付费、权限分级、团队管理。
- 真实音频 URL 管理后台。
- 数字人形象推荐的完整实现。

## 3. 产品形态

前端是一个单页内部评测工具：

1. 用户输入配音文本。
2. 页面显示当前字数和最大字数限制。
3. 用户点击“智能匹配”。
4. 前端展示 `Top5` 推荐音色卡片。
5. 用户逐个试听音色。
6. 用户给每个音色打分，并可填写文字建议。
7. 用户提交反馈后，后端记录反馈数据。

音色卡片默认展示调试字段，便于评测人员判断问题来源：
- Rank
- 发音人名称
- VCN
- 一级场景
- 二级场景
- 标签信息
- 性别
- 语言
- 技术标签
- 试听播放器
- 评分
- 文字建议

## 4. 系统架构

建议目录：

```text
frontend/
  src/
  package.json
  vite.config.ts

backend/
  app/
    main.py
    schemas.py
    recommender/
    storage/
  data/
  requirements.txt
  README.md
```

推荐技术栈：
- 前端：`React + Vite`
- 后端：`FastAPI`
- 存储：`SQLite`
- 推荐逻辑：复用当前 Python 规则召回与 DeepSeek 重排逻辑

选择原因：
- 当前推荐 demo 已经是 Python，后端用 FastAPI 可最小成本复用。
- SQLite 足够支撑内部评测和数据导出。
- React + Vite 适合快速做评测型交互页面。

前端视觉规范：
- 参考 `docs/specs/2026-06-03-frontend-visual-guidelines.md`。
- 参考 `design-system/intelligent-matching-evaluation-system/MASTER.md`。
- 使用舒缓 pastel 与轻拟物风格，但页面必须是评测工具，不做营销落地页。

## 5. 后端设计

后端职责：
- 加载音库、标签体系、关键词库。
- 执行规则召回。
- 调用 `deepseek-v4-flash` 重排。
- 发音人去重后返回 `Top5`。
- 保存推荐请求、推荐结果、调试信息。
- 接收评分和文字建议。

推荐接口：

```http
POST /api/recommend
```

请求：

```json
{
  "task_type": "voice",
  "text": "配音正文"
}
```

返回：

```json
{
  "request_id": "uuid",
  "task_type": "voice",
  "recommendations": [
    {
      "rank": 1,
      "asset_type": "voice",
      "asset_id": "vcn_xxx",
      "vcn": "vcn_xxx",
      "speaker_name": "发音人名称",
      "scene_l1": ["商业广告"],
      "scene_l2": ["营销风格"],
      "tags": {
        "scene_l1": ["商业广告"],
        "scene_l2": ["营销风格"],
        "attributes": ["地道方言"],
        "language": "普通话",
        "gender": "女",
        "tech_desc": "超拟人 Pro"
      },
      "gender": "女",
      "language": "普通话",
      "tech_desc": "超拟人 Pro",
      "audio_url": null
    }
  ]
}
```

反馈接口：

```http
POST /api/feedback
```

请求：

```json
{
  "request_id": "uuid",
  "task_type": "voice",
  "asset_type": "voice",
  "asset_id": "vcn_xxx",
  "rank": 1,
  "rating": 4,
  "comment": "方向正确，但希望更年轻一点"
}
```

辅助接口：

```http
GET /api/health
```

用于部署和联调时确认服务可用。

## 6. 数据设计

### 6.1 recommendation_requests

记录每次推荐请求。

字段：
- `request_id`
- `task_type`
- `input_text`
- `input_char_count`
- `analysis_text`
- `analysis_char_count`
- `model`
- `status`
- `error_message`
- `created_at`

### 6.2 recommendation_results

记录每次推荐返回的候选。

字段：
- `id`
- `request_id`
- `task_type`
- `asset_type`
- `asset_id`
- `rank`
- `metadata_json`
- `debug_json`
- `created_at`

说明：
- `metadata_json` 保存展示字段，如 `speaker_name`、`vcn`、`scene_l1`、`scene_l2`、`tags`、`gender`、`language`、`tech_desc`、`audio_url`。
- `debug_json` 保存内部调试字段，如规则命中、规则分、LLM score、reason、降级链路。

### 6.2.1 推荐标签字段

推荐结果需要返回音色对应标签，标签来源为音库标注和标签体系归一结果。

字段：
- `scene_l1`：一级场景标签。
- `scene_l2`：二级场景标签。
- `attributes`：属性标签，例如 `童声`、`地道方言`。
- `language`：语言。
- `gender`：性别。
- `tech_desc`：技术标签或技术描述。

前端应直接展示这些字段，后端应同步写入 `recommendation_results.metadata_json`，保证后续能按标签维度统计反馈。

### 6.3 feedback

记录评测人员反馈。

字段：
- `feedback_id`
- `request_id`
- `task_type`
- `asset_type`
- `asset_id`
- `rank`
- `rating`
- `comment`
- `created_at`

### 6.4 asset_url_overrides

预留音频 URL 配置。

字段：
- `asset_type`
- `asset_id`
- `audio_url`
- `status`
- `updated_at`

本期可先返回 `audio_url: null`，后续接入你提供的音频 URL。

## 7. 长文本处理

前端允许最多 `15000` 字输入。后端需要区分完整原文和模型分析文本：

- `input_text`：完整保存，用于人工复盘和后续评测。
- `analysis_text`：用于规则召回和 DeepSeek 重排。

建议第一版处理方式：
- 完整保存 `15000` 字原文。
- 规则召回可使用完整文本。
- DeepSeek 输入裁剪到 `3000-5000` 字。
- 裁剪策略优先保留开头、结尾和高信号片段。

这样可以兼顾数据采集完整性、推荐成本和接口稳定性。

## 8. 扩展到形象推荐

接口和数据表必须保留 `task_type` 与 `asset_type`：

当前音色推荐：
- `task_type = voice`
- `asset_type = voice`
- `asset_id = vcn`

未来形象推荐：
- `task_type = avatar`
- `asset_type = avatar`
- `asset_id = 数字人形象ID`

未来联合推荐：
- `task_type = voice_avatar`
- `asset_type = voice` 或 `avatar`
- 同一个 `request_id` 下可保存多类推荐结果。

这样后续扩展数字人形象推荐时，不需要推翻前端反馈结构和后端日志结构。

## 9. 安全与访问控制

系统是内部评测链接，不做账号体系，但仍需基本保护：

- DeepSeek API Key 只放在后端环境变量。
- 前端不得暴露模型 API Key。
- 后端限制单次输入最大 `15000` 字。
- 后端设置基础限流，例如同 IP 每分钟 `10` 次。
- CORS 限制为内部前端域名。
- 错误响应不暴露内部堆栈。
- 页面展示数据使用说明，提醒评测人员避免输入敏感信息。

## 10. 实施计划

### 阶段一：本地可运行版本

- 创建 `backend/`。
- 将现有 `demo/voice_recommend_demo.py` 的推荐逻辑拆成可复用模块。
- 用 FastAPI 提供 `/api/recommend`、`/api/feedback`、`/api/health`。
- 用 SQLite 保存请求、结果和反馈。
- 创建 `frontend/`。
- 实现文本输入、Top5 展示、试听占位、评分和反馈提交。

### 阶段二：内部评测版本

- 接入真实音频 URL。
- 增加部署配置。
- 配置环境变量、限流、CORS。
- 生成反馈数据导出方式。

### 阶段三：反馈分析

- 汇总评分低的推荐。
- 按场景、音色、发音人统计反馈。
- 形成 bad case 回流表。
- 支持导出为 CSV，用于规则迭代。

## 11. 验收标准

本地版本验收：
- 前端可输入 `15000` 字以内文本。
- 点击智能匹配后返回 `Top5`。
- 每个音色展示一级/二级场景、技术标签、性别、语言。
- 每个音色返回并展示对应标签信息，且标签信息写入推荐结果日志。
- 每个音色支持评分和文字建议提交。
- 后端数据库可查到请求日志、推荐结果和反馈。
- DeepSeek API Key 不出现在前端代码和浏览器请求中。

内部评测版本验收：
- 通过内部链接可访问。
- 多名评测人员可同时使用。
- 推荐失败时页面有明确提示。
- 后端保存错误日志，便于排查。
- 音频 URL 接入后可正常试听。
