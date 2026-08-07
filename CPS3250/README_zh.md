# Hybrid Scheduler

[English](README.md) | 中文

Hybrid Scheduler 是一个基于 FastAPI 的混合任务调度原型。它会按照任务特征把任务分为实时、短任务和批处理任务，再分别使用 EDF、轮转或 SJF 策略排序，并把任务轮转分配到模拟计算节点。

当前版本适合课程实验、本地演示和调度策略比较，不包含真正的容器、Kubernetes 或 AWS 任务执行逻辑。

## 主要功能

- `POST /submit`：提交 CPU 或 IO 任务。
- `GET /health`：服务健康检查。
- `GET /metrics`：Prometheus 指标。
- 支持 RR、SJF、HRRN、EDF 和 Hybrid 五种实验策略。
- 提供 Prometheus、Grafana 的 Docker Compose 本地监控环境。

混合策略的默认映射如下：

| 任务类别 | 判断方式 | 调度策略 |
| --- | --- | --- |
| realtime | 截止时间距离当前时间不超过 5 秒 | EDF |
| short | 预计时长不超过 1 秒 | Round Robin |
| batch | 其他任务 | SJF |

## 项目结构

```text
hybrid-scheduler/
├── src/hybrid_scheduler/
│   ├── main.py              # FastAPI 入口和后台调度线程
│   ├── config.py            # 环境变量配置
│   ├── dispatcher/          # 模拟节点派发器
│   ├── profiler/            # 任务分类规则
│   ├── strategies/          # RR/SJF/HRRN/EDF/Hybrid
│   ├── monitoring/          # Prometheus 指标
│   └── experiments/         # 工作负载、实验与绘图脚本
├── README.md                # 英文文档
├── README_zh.md             # 中文文档
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── pyproject.toml
└── .env.example
```

## 环境要求

- Python 3.12+
- Poetry 2.x（推荐）
- Docker 与 Docker Compose（可选，用于容器化和监控）

## 本地运行

在本目录执行：

```powershell
Copy-Item .env.example .env
poetry install
poetry run uvicorn hybrid_scheduler.main:app --host 127.0.0.1 --port 8080
```

启动后可访问：

- API 文档：<http://127.0.0.1:8080/docs>
- 健康检查：<http://127.0.0.1:8080/health>
- Prometheus 指标：<http://127.0.0.1:8080/metrics>

### 启用 API Key

服务仅在 `API_KEY` 非空时校验 API Key。本地纯演示可以不设置；只要服务可能被其他机器访问，就应设置强随机值，或把服务放在具备身份认证的反向代理后面。

生成随机值：

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

将结果写入私有的 `.env`：

```dotenv
API_KEY=替换为刚生成的随机值
```

修改 `.env` 后需要重启服务。请求时通过 `X-API-Key` 传递：

```powershell
$headers = @{ "X-API-Key" = "替换为你的值" }
$body = @{ category = "CPU"; duration = 0.5 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8080/submit `
  -Headers $headers -ContentType "application/json" -Body $body
```

未启用 API Key 时可以省略 `-Headers`。成功响应示例：

```json
{
  "id": "7fe50f6e-5c90-4603-9fb3-825eaee57e20",
  "status": "queued"
}
```

任务 ID 由服务端生成。请求体不接受 `id` 字段，避免调用方把姓名、邮箱、学号等个人标识误传并进入后续系统。

完整请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `category` | 是 | `CPU` 或 `IO` |
| `duration` | 是 | 预计运行秒数，必须大于 0 |
| `deadline` | 否 | Unix epoch 截止时间 |
| `priority` | 否 | 数值越小优先级越高；当前原型仅保留该输入，尚未参与默认混合策略 |

## Docker Compose

先复制配置并设置 Grafana 管理员密码：

```powershell
Copy-Item .env.example .env
# 编辑 .env，至少设置 GRAFANA_ADMIN_PASSWORD；建议同时设置 API_KEY
docker build -t hybrid-scheduler:0.1 .
docker compose up -d
```

本机入口：

- API：<http://127.0.0.1:8080>
- Prometheus：<http://127.0.0.1:9090>
- Grafana：<http://127.0.0.1:3000>

Compose 默认只把端口绑定到 `127.0.0.1`。Grafana 匿名访问、注册和分析遥测均已关闭。若要供局域网或公网访问，请在受控反向代理后配置 TLS、身份认证和网络访问控制，不要直接把这些端口改成全网监听。

停止服务：

```powershell
docker compose down
```

## 运行调度实验

以 Hybrid 策略运行批处理工作负载，并跳过真实等待：

```powershell
poetry run python -m hybrid_scheduler.experiments.runner `
  --strategy hybrid `
  --workload batch.json `
  --output results/batch_hybrid.csv `
  --dry
```

`--strategy` 可选值为 `rr`、`sjf`、`hrrn`、`edf`、`hybrid`。不加 `--dry` 时，程序会按每个任务的 `duration` 实际等待。

绘图脚本还需要 `pandas` 和 `matplotlib`，它们目前不是核心运行依赖：

```powershell
poetry run pip install pandas matplotlib
poetry run python -m hybrid_scheduler.experiments.plot_results `
  --results-dir results `
  --prefix batch_ `
  --output-dir results/plots
```

## 隐私与安全设计

本项目采用以下默认保护：

- 项目元数据不包含个人姓名或邮箱。
- `.env`、密钥文件、虚拟环境、缓存和新生成的任务级实验结果不会进入 Git 或 Docker 构建上下文。
- API 不接收调用方自定义任务 ID；内部使用随机 UUID。
- 调度日志只记录目标节点，不记录任务 ID 或任务正文。
- API Key、RabbitMQ URL 使用脱敏配置类型，打印设置对象时不会显示明文。
- AWS 凭据不在项目配置中声明；如需接入 AWS，应使用 boto3 标准凭据链和 IAM 角色。
- Compose 服务仅绑定本机，Grafana 默认禁止匿名访问和遥测。

仍需注意：

- `API_KEY` 是轻量保护，不替代完整用户身份、权限、限流或审计系统。
- `/metrics` 不含任务 ID，但会暴露队列长度、任务类别和耗时分布。不要未经访问控制直接发布到公网。
- 当前队列位于进程内存中，重启即丢失；项目不会把 API 提交内容写入数据库。
- 不要把真实姓名、邮箱、学号、客户编号、访问令牌或业务正文放入任务字段、工作负载 JSON、CSV、日志或截图。
- 如果敏感值曾经进入 Git 历史，仅加入 `.gitignore` 不足以删除历史；应轮换密钥并使用专门工具清理历史记录。

## 配置项

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `APP_NAME` | `Hybrid Scheduler` | 应用名称 |
| `ENVIRONMENT` | `dev` | 运行环境标识 |
| `HOST` | `127.0.0.1` | 本地服务监听地址 |
| `PORT` | `8080` | API 端口 |
| `API_KEY` | 空 | 非空时保护 `/submit` |
| `RABBITMQ_URL` | 空 | 预留的 RabbitMQ 连接串 |
| `AWS_REGION` | `us-east-1` | AWS 区域 |
| `PROM_PORT` | `8000` | 预留的独立 Prometheus 端口配置 |
| `GRAFANA_ADMIN_PASSWORD` | 无 | Compose 启动 Grafana 时必须设置 |

## 当前限制

- 派发器仅记录模拟分配，不会真正启动远程任务。
- 后台执行为单线程顺序 `sleep`，不代表真实并行调度。
- 队列和状态不持久化。
- 暂无用户级认证、授权、速率限制和完整审计。
- RR 在实验层以任务切片顺序近似实现，不是操作系统级抢占。

## 开发检查

```powershell
poetry run ruff check src
poetry run black --check src
poetry run pytest
```

提交变更前，请再次确认 `.env`、`keys/`、实验输出以及任何含个人数据的文件未被加入版本控制。
