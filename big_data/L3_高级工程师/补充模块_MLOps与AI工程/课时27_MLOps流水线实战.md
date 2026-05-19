# 课时27：MLOps流水线实战

> **所属阶段**：L3 高级工程师 | **模块**：补充模块_MLOps与AI工程 | **课时**：4h | **难度**：★★★★★

---

## 一、教学目标

1. 理解MLOps成熟度模型，能评估团队当前所处级别并制定演进路线
2. 掌握MLflow Tracking实现实验追踪，记录超参数、指标、产物
3. 掌握MLflow Model Registry实现模型注册、阶段转换、版本管理
4. 了解模型服务方案：MLflow Serving、TF Serving、Triton Inference Server
5. 了解编排平台选型：Kubeflow、Vertex AI、SageMaker
6. 掌握数据漂移检测方法，能使用Evidently检测特征分布变化

---

## 二、MLOps成熟度模型

### 2.1 三个级别详解

```
MLOps成熟度模型（Google提出）:

  Level 0: 手动流程
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  数据科学家 ──手动──→ 训练脚本 ──手动──→ 模型文件(.pkl)   │
  │                              │                           │
  │                              ↓ 手动部署                  │
  │                         工程师 ──→ 线上服务               │
  │                                                          │
  │  特征:                                                    │
  │  ✗ 无实验追踪，结果无法复现                                │
  │  ✗ 无CI/CD，部署靠人工                                    │
  │  ✗ 无监控，模型退化无人知晓                                │
  │  ✓ 适合: PoC阶段、一次性分析                               │
  └──────────────────────────────────────────────────────────┘

  Level 1: ML Pipeline自动化
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐     │
  │  │数据摄取│──→│特征工程│──→│模型训练│──→│模型验证│     │
  │  └────────┘   └────────┘   └────────┘   └───┬────┘     │
  │                                               │          │
  │  编排器(Airflow/Kubeflow)自动触发              ↓          │
  │                                         ┌──────────┐    │
  │                                         │模型注册表│    │
  │                                         └────┬─────┘    │
  │                                              │ 自动部署  │
  │                                              ↓          │
  │                                         ┌──────────┐    │
  │                                         │模型服务  │    │
  │                                         └──────────┘    │
  │                                                          │
  │  特征:                                                    │
  │  ✓ 实验追踪，结果可复现                                    │
  │  ✓ Pipeline自动执行（定时/事件触发）                       │
  │  ✓ 模型注册与版本管理                                     │
  │  ✗ 无CI/CD，代码变更无自动测试                             │
  │  ✓ 适合: 生产环境基础版                                   │
  └──────────────────────────────────────────────────────────┘

  Level 2: CI/CD + 持续监控
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │               CI/CD Pipeline                      │   │
  │  │  代码提交 → 单元测试 → 集成测试 → Pipeline构建    │   │
  │  │       → 模型训练 → 模型验证 → A/B测试 → 上线      │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  ┌──────────────────────────────────────────────────┐   │
  │  │               持续监控                            │   │
  │  │  数据漂移检测 → 概念漂移检测 → 性能退化告警        │   │
  │  │       → 自动触发重训练 → 新模型验证 → 灰度发布     │   │
  │  └──────────────────────────────────────────────────┘   │
  │                                                          │
  │  特征:                                                    │
  │  ✓ 完整CI/CD，代码和Pipeline变更自动测试                  │
  │  ✓ 持续监控，漂移自动检测                                 │
  │  ✓ 自动重训练与灰度发布                                   │
  │  ✓ 特征存储保证训练-推理一致性                             │
  │  ✓ 适合: 大规模生产环境                                   │
  └──────────────────────────────────────────────────────────┘
```

### 2.2 级别对比

| 维度 | Level 0 | Level 1 | Level 2 |
|------|---------|---------|---------|
| Pipeline | 手动脚本 | 自动化Pipeline | CI/CD Pipeline |
| 实验追踪 | 无/Excel | MLflow/W&B | MLflow/W&B |
| 模型注册 | 文件系统 | Model Registry | Model Registry + 审批 |
| 部署方式 | 手动拷贝 | 自动部署 | 灰度/A/B测试 |
| 监控 | 无 | 基础监控 | 漂移检测 + 自动重训练 |
| 特征管理 | 脚本内硬编码 | 特征存储 | 特征存储 + 治理 |
| 典型团队 | 1-2人 | 3-5人 | 5+人 |

---

## 三、实验追踪：MLflow Tracking

### 3.1 核心概念

```
MLflow Tracking 架构:

  ┌──────────────────────────────────────────────────────────┐
  │                  MLflow Tracking Server                   │
  │                                                          │
  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐  │
  │  │ Experiment │  │  Run       │  │  Artifact Store   │  │
  │  │ (实验)     │  │  (运行)    │  │  (产物存储)       │  │
  │  │            │  │            │  │                   │  │
  │  │ - 名称     │  │ - 超参数   │  │ - 模型文件(.pkl)  │  │
  │  │ - 描述     │  │ - 指标     │  │ - 数据快照        │  │
  │  │ - Run列表  │  │ - 产物     │  │ - 环境信息        │  │
  │  │            │  │ - 状态     │  │ - 可视化图表      │  │
  │  │            │  │ - 标签     │  │                   │  │
  │  └────────────┘  └────────────┘  └──────────────────┘  │
  │                                                          │
  │  Backend Store: PostgreSQL/MySQL (元数据)                 │
  │  Artifact Store: S3/OSS/HDFS (产物文件)                  │
  └──────────────────────────────────────────────────────────┘
```

### 3.2 MLflow与Weights & Biases对比

| 维度 | MLflow | Weights & Biases |
|------|--------|------------------|
| 开源 | ✅ 完全开源 | ⚠️ 核心功能闭源 |
| 部署 | 自托管 / Databricks托管 | 仅SaaS |
| 实验追踪 | ✅ | ✅（可视化更强） |
| 模型注册 | ✅ | ✅ |
| 协作 | 基础UI | 强（团队、报告） |
| 超参数搜索 | 需配合Optuna | 内置Sweep |
| 成本 | 免费（自托管） | 免费额度有限 |
| 适用 | 企业级、合规要求 | 研究团队、快速迭代 |

### 3.3 实战：XGBoost训练 + MLflow追踪

```python
import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("user_churn_prediction")

X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

params = {
    "max_depth": 6,
    "learning_rate": 0.1,
    "n_estimators": 200,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "random_state": 42,
}

with mlflow.start_run(run_name="xgboost_churn_v1") as run:
    mlflow.log_params(params)

    model = xgb.XGBClassifier(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)

    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    mlflow.log_metrics({
        "auc": auc,
        "accuracy": accuracy,
        "f1_score": f1,
    })

    importances = model.feature_importances_
    for i, imp in enumerate(importances):
        mlflow.log_metric(f"feature_importance_{i}", imp)

    mlflow.xgboost.log_model(model, "model")

    print(f"Run ID: {run.info.run_id}")
    print(f"AUC: {auc:.4f}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1: {f1:.4f}")
```

### 3.4 超参数搜索 + MLflow追踪

```python
import mlflow
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("user_churn_prediction")

X, y = make_classification(n_samples=10000, n_features=20, n_informative=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

param_grid = {
    "max_depth": [4, 6, 8],
    "learning_rate": [0.01, 0.05, 0.1],
    "n_estimators": [100, 200, 300],
    "subsample": [0.7, 0.8, 0.9],
}

best_auc = 0
best_run_id = None

for max_depth in param_grid["max_depth"]:
    for lr in param_grid["learning_rate"]:
        for n_est in param_grid["n_estimators"]:
            for subsample in param_grid["subsample"]:
                params = {
                    "max_depth": max_depth,
                    "learning_rate": lr,
                    "n_estimators": n_est,
                    "subsample": subsample,
                    "objective": "binary:logistic",
                    "eval_metric": "auc",
                    "colsample_bytree": 0.8,
                    "random_state": 42,
                }

                with mlflow.start_run(run_name=f"xgb_d{max_depth}_lr{lr}_n{n_est}_s{subsample}"):
                    mlflow.log_params(params)

                    model = xgb.XGBClassifier(**params)
                    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

                    y_pred_proba = model.predict_proba(X_test)[:, 1]
                    auc = roc_auc_score(y_test, y_pred_proba)

                    mlflow.log_metrics({"auc": auc, "accuracy": accuracy_score(y_test, model.predict(X_test))})
                    mlflow.xgboost.log_model(model, "model")

                    if auc > best_auc:
                        best_auc = auc
                        best_run_id = mlflow.active_run().info.run_id

print(f"Best AUC: {best_auc:.4f}, Run ID: {best_run_id}")
```

---

## 四、模型注册：MLflow Model Registry

### 4.1 核心概念

```
MLflow Model Registry 模型生命周期:

  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  注册模型 ──→ None ──→ Staging ──→ Production            │
  │                │          │            │                  │
  │                │          │            │                  │
  │              实验中     测试验证中    线上服务中            │
  │                │          │            │                  │
  │                │          │            │                  │
  │              可删除    可回退None   可回退Staging          │
  │                                     可归档Archived        │
  │                                                          │
  │  版本管理:                                                │
  │  churn_model v1 (XGBoost, AUC=0.85) → Production         │
  │  churn_model v2 (LightGBM, AUC=0.87) → Staging          │
  │  churn_model v3 (XGBoost, AUC=0.88) → None              │
  │                                                          │
  │  审批流程:                                                │
  │  数据科学家提交 → 评审人审批 → 转换到Staging              │
  │  → 测试通过 → 评审人审批 → 转换到Production              │
  └──────────────────────────────────────────────────────────┘
```

### 4.2 注册模型与阶段转换

```python
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

model_name = "user_churn_model"

try:
    client.create_registered_model(model_name)
except Exception:
    print(f"模型 {model_name} 已存在")

result = mlflow.register_model(
    model_uri=f"runs://<RUN_ID>/model",
    name=model_name,
)
print(f"注册版本: {result.version}")

client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Staging",
)

staging_versions = client.get_latest_versions(model_name, stages=["Staging"])
for v in staging_versions:
    print(f"Staging版本: v{v.version}, Run ID: {v.run_id}")

client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Production",
)

prod_versions = client.get_latest_versions(model_name, stages=["Production"])
for v in prod_versions:
    print(f"Production版本: v{v.version}, Run ID: {v.run_id}")
```

### 4.3 模型版本管理与比较

```python
from mlflow.tracking import MlflowClient
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

model_name = "user_churn_model"

versions = client.search_model_versions(f"name='{model_name}'")
for v in versions:
    run = client.get_run(v.run_id)
    auc = run.data.metrics.get("auc", "N/A")
    print(f"版本: v{v.version}, 阶段: {v.current_stage}, AUC: {auc}")

latest_prod = client.get_latest_versions(model_name, stages=["Production"])[0]
prod_run = client.get_run(latest_prod.run_id)
prod_auc = prod_run.data.metrics.get("auc", 0)

latest_staging = client.get_latest_versions(model_name, stages=["Staging"])[0]
staging_run = client.get_run(latest_staging.run_id)
staging_auc = staging_run.data.metrics.get("auc", 0)

print(f"\nProduction AUC: {prod_auc:.4f}")
print(f"Staging AUC: {staging_auc:.4f}")
print(f"提升: {(staging_auc - prod_auc) * 100:.2f}%")

if staging_auc > prod_auc:
    client.transition_model_version_stage(
        name=model_name,
        version=latest_staging.version,
        stage="Production",
        archive_existing_versions=True,
    )
    print("Staging模型已提升为Production")
```

---

## 五、模型服务

### 5.1 方案对比

| 维度 | MLflow Serving | TF Serving | Triton Inference Server |
|------|---------------|------------|------------------------|
| 支持框架 | 任意MLflow模型 | TensorFlow/TF Lite | TF/PyTorch/ONNX/TensorRT |
| 部署方式 | Docker/CLI | Docker/K8s | Docker/K8s |
| 批量推理 | ✅ | ✅ | ✅（高级调度） |
| 动态批处理 | ❌ | ✅ | ✅ |
| GPU加速 | ❌ | ✅ | ✅（TensorRT集成） |
| A/B测试 | 基础支持 | ✅ | ✅ |
| 模型热更新 | ❌ | ✅ | ✅ |
| 适用场景 | 快速原型 | TF生态 | 高性能/多框架 |

### 5.2 MLflow模型部署REST API

```bash
mlflow models serve -m "models:/user_churn_model/Production" -p 5001 --host 0.0.0.0
```

```python
import requests
import json
import numpy as np

data = {
    "dataframe_split": {
        "columns": [f"feature_{i}" for i in range(20)],
        "data": [
            [float(x) for x in np.random.randn(20)]
            for _ in range(5)
        ],
    }
}

response = requests.post(
    "http://localhost:5001/invocations",
    headers={"Content-Type": "application/json"},
    data=json.dumps(data),
)

predictions = response.json()
print(f"预测结果: {predictions}")
```

### 5.3 A/B测试部署

```python
from flask import Flask, request, jsonify
import mlflow
import numpy as np
import random

app = Flask(__name__)

model_a_uri = "models:/user_churn_model/1"
model_b_uri = "models:/user_churn_model/2"

model_a = mlflow.xgboost.load_model(model_a_uri)
model_b = mlflow.xgboost.load_model(model_b_uri)

TRAFFIC_SPLIT = 0.2

@app.route("/predict", methods=["POST"])
def predict():
    features = request.json["features"]
    X = np.array(features).reshape(1, -1)

    if random.random() < TRAFFIC_SPLIT:
        model = model_b
        model_version = "B"
    else:
        model = model_a
        model_version = "A"

    prediction = model.predict_proba(X)[0][1]

    return jsonify({
        "churn_probability": float(prediction),
        "model_version": model_version,
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
```

---

## 六、编排平台对比

### 6.1 三大平台对比

| 维度 | Kubeflow Pipelines | Vertex AI | SageMaker |
|------|-------------------|-----------|-----------|
| 部署方式 | 自托管K8s | 全托管 | 全托管 |
| Pipeline定义 | Python SDK | Python SDK | Python SDK |
| 实验追踪 | MLflow集成 | 内置 | 内置 |
| 超参数搜索 | Katib | 内置 | 内置 |
| 模型注册 | MLflow | 内置 | 内置 |
| 模型服务 | K8s/Seldon | 内置 | 内置 |
| 成本 | 基础设施成本 | 按使用付费 | 按使用付费 |
| 灵活性 | 最高 | 中等 | 中等 |
| 运维复杂度 | 高 | 低 | 低 |
| 适用场景 | 大型团队/合规 | GCP用户 | AWS用户 |

### 6.2 Kubeflow Pipeline示例

```python
from kfp import dsl
from kfp.dsl import component, Output, Model, Metrics

@component(base_image="python:3.9")
def train_model(
    data_path: str,
    max_depth: int,
    learning_rate: float,
    model: Output[Model],
    metrics: Output[Metrics],
):
    import xgboost as xgb
    import numpy as np
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    import joblib

    X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_obj = xgb.XGBClassifier(
        max_depth=max_depth,
        learning_rate=learning_rate,
        n_estimators=200,
        objective="binary:logistic",
        random_state=42,
    )
    model_obj.fit(X_train, y_train)

    y_pred_proba = model_obj.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)

    joblib.dump(model_obj, model.path)
    metrics.log_metric("auc", auc)

@component(base_image="python:3.9")
def validate_model(
    model: Input[Model],
    min_auc: float,
) -> bool:
    import joblib
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score

    model_obj = joblib.load(model.path)
    X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    y_pred_proba = model_obj.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)

    if auc >= min_auc:
        print(f"验证通过: AUC={auc:.4f} >= {min_auc}")
        return True
    else:
        print(f"验证失败: AUC={auc:.4f} < {min_auc}")
        return False

@dsl.pipeline(name="churn-model-pipeline")
def churn_pipeline(
    data_path: str = "/data/churn.csv",
    max_depth: int = 6,
    learning_rate: float = 0.1,
    min_auc: float = 0.80,
):
    train_task = train_model(
        data_path=data_path,
        max_depth=max_depth,
        learning_rate=learning_rate,
    )

    validate_task = validate_model(
        model=train_task.outputs["model"],
        min_auc=min_auc,
    )
```

---

## 七、监控与漂移检测

### 7.1 漂移类型

```
数据漂移(Data Drift) vs 概念漂移(Concept Drift):

  数据漂移: 输入特征分布变化，但P(Y|X)不变
  ┌──────────────────────────────────────────────────────────┐
  │  训练时: 用户年龄分布 = [18-35: 60%, 36-55: 30%, 55+: 10%]│
  │  推理时: 用户年龄分布 = [18-35: 30%, 36-55: 40%, 55+: 30%]│
  │                                                          │
  │  原因: 用户群体变化、季节性、数据源变更                     │
  │  影响: 模型在新的分布上表现下降                              │
  │  检测: 统计检验(KS/Psi)、特征分布对比                      │
  └──────────────────────────────────────────────────────────┘

  概念漂移: P(Y|X)变化，输入分布可能不变
  ┌──────────────────────────────────────────────────────────┐
  │  训练时: 年龄55+ → 流失概率30%                             │
  │  推理时: 年龄55+ → 流失概率60%（经济环境变化）              │
  │                                                          │
  │  原因: 业务规则变化、市场环境变化、用户行为变化              │
  │  影响: 模型预测不再准确                                     │
  │  检测: 模型性能指标监控、标签延迟获取后对比                  │
  └──────────────────────────────────────────────────────────┘
```

### 7.2 Evidently数据漂移检测

```python
import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset
from evidently.metrics import *

np.random.seed(42)
n_train = 5000
n_prod = 2000

reference_data = pd.DataFrame({
    "age": np.random.normal(35, 10, n_train).clip(18, 70),
    "income": np.random.lognormal(10, 1, n_train),
    "tenure_months": np.random.randint(1, 120, n_train),
    "monthly_spend": np.random.gamma(5, 20, n_train),
    "num_support_tickets": np.random.poisson(1.5, n_train),
})

production_data = pd.DataFrame({
    "age": np.random.normal(45, 12, n_prod).clip(18, 70),
    "income": np.random.lognormal(10.5, 1.2, n_prod),
    "tenure_months": np.random.randint(1, 120, n_prod),
    "monthly_spend": np.random.gamma(4, 25, n_prod),
    "num_support_tickets": np.random.poisson(2.5, n_prod),
})

drift_report = Report(metrics=[
    DataDriftPreset(),
])

drift_report.run(
    reference_data=reference_data,
    current_data=production_data,
)

drift_report.save_html("data_drift_report.html")

drift_results = drift_report.as_dict()
for metric in drift_results["metrics"]:
    if "drift_summary" in metric.get("result", {}):
        summary = metric["result"]["drift_summary"]
        for feature, info in summary.items():
            drift = info.get("drift_detected", False)
            score = info.get("drift_score", 0)
            status = "⚠️ 漂移" if drift else "✅ 正常"
            print(f"{feature}: {status}, 得分={score:.4f}")
```

### 7.3 模型性能退化告警

```python
import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import ClassificationPreset
from evidently.metrics import *

np.random.seed(42)
n = 5000

X = np.random.randn(n, 5)
y_true = (X[:, 0] * 2 + X[:, 1] - X[:, 2] > 0).astype(int)

y_ref_pred = y_true.copy()
noise_idx = np.random.choice(n, int(n * 0.05), replace=False)
y_ref_pred[noise_idx] = 1 - y_ref_pred[noise_idx]

y_prod_pred = y_true.copy()
noise_idx = np.random.choice(n, int(n * 0.25), replace=False)
y_prod_pred[noise_idx] = 1 - y_prod_pred[noise_idx]

reference = pd.DataFrame({"target": y_true, "prediction": y_ref_pred})
production = pd.DataFrame({"target": y_true, "prediction": y_prod_pred})

performance_report = Report(metrics=[
    ClassificationPreset(),
])

performance_report.run(
    reference_data=reference,
    current_data=production,
)

performance_report.save_html("model_performance_report.html")

perf_results = performance_report.as_dict()
for metric in perf_results["metrics"]:
    metric_name = metric.get("metric", "")
    if "accuracy" in str(metric.get("result", {})).lower():
        print(f"{metric_name}: {metric['result']}")
```

### 7.4 定时漂移检测脚本

```python
import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import requests
import json
from datetime import datetime

WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
DRIFT_THRESHOLD = 0.3

def load_reference_data():
    return pd.read_csv("s3://ml-data/churn/reference_data.csv")

def load_production_data():
    return pd.read_csv("s3://ml-data/churn/production_data_latest.csv")

def check_drift(reference, production):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=production)
    results = report.as_dict()

    drifted_features = []
    for metric in results["metrics"]:
        if "drift_summary" in metric.get("result", {}):
            for feature, info in metric["result"]["drift_summary"].items():
                if info.get("drift_detected", False):
                    drifted_features.append({
                        "feature": feature,
                        "drift_score": info.get("drift_score", 0),
                    })

    drift_ratio = len(drifted_features) / len(reference.columns) if len(reference.columns) > 0 else 0
    return drifted_features, drift_ratio

def send_alert(drifted_features, drift_ratio):
    feature_list = "\n".join(
        [f"  - {f['feature']}: 漂移得分={f['drift_score']:.4f}" for f in drifted_features]
    )
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": (
                f"**⚠️ 数据漂移告警**\n"
                f"> 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"> 漂移特征比例: {drift_ratio:.1%}\n"
                f"> 漂移特征:\n{feature_list}\n"
                f"> 请及时排查并考虑重训练模型"
            )
        }
    }
    requests.post(WEBHOOK_URL, json=payload)

def main():
    reference = load_reference_data()
    production = load_production_data()
    drifted_features, drift_ratio = check_drift(reference, production)

    if drift_ratio > DRIFT_THRESHOLD:
        send_alert(drifted_features, drift_ratio)
        print(f"漂移告警已发送，漂移比例: {drift_ratio:.1%}")
    else:
        print(f"数据正常，漂移比例: {drift_ratio:.1%}")

if __name__ == "__main__":
    main()
```

---

## 八、课堂练习（60min）

### 练习1：用MLflow追踪完整的模型训练流程（20min）

```bash
pip install mlflow xgboost scikit-learn
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow_artifacts
```

```python
import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("churn_prediction_lab")

X, y = make_classification(n_samples=5000, n_features=15, n_informative=8, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

configs = [
    {"max_depth": 4, "learning_rate": 0.1, "n_estimators": 100},
    {"max_depth": 6, "learning_rate": 0.05, "n_estimators": 200},
    {"max_depth": 8, "learning_rate": 0.01, "n_estimators": 300},
]

for i, cfg in enumerate(configs):
    with mlflow.start_run(run_name=f"xgboost_config_{i+1}"):
        params = {**cfg, "objective": "binary:logistic", "random_state": 42}
        mlflow.log_params(params)

        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "auc": roc_auc_score(y_test, y_pred_proba),
            "accuracy": accuracy_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
        }
        mlflow.log_metrics(metrics)
        mlflow.xgboost.log_model(model, "model")

        print(f"Config {i+1}: AUC={metrics['auc']:.4f}, F1={metrics['f1']:.4f}")
```

### 练习2：注册模型并部署为REST API（20min）

```python
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

model_name = "churn_lab_model"

client.create_registered_model(model_name)

best_run = client.search_runs(
    experiment_ids=["1"],
    order_by=["metrics.auc DESC"],
    max_results=1,
)[0]

result = mlflow.register_model(
    model_uri=f"runs:/{best_run.info.run_id}/model",
    name=model_name,
)
print(f"注册版本: {result.version}, AUC: {best_run.data.metrics['auc']:.4f}")

client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Staging",
)

client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Production",
)

print(f"模型 {model_name} v{result.version} 已发布到Production")
```

```bash
mlflow models serve -m "models:/churn_lab_model/Production" -p 5001 --host 0.0.0.0
```

### 练习3：发送预测请求验证模型服务（20min）

```python
import requests
import json
import numpy as np
from sklearn.datasets import make_classification

X, _ = make_classification(n_samples=10, n_features=15, n_informative=8, random_state=99)

data = {
    "dataframe_split": {
        "columns": [f"f{i}" for i in range(15)],
        "data": X.tolist(),
    }
}

response = requests.post(
    "http://localhost:5001/invocations",
    headers={"Content-Type": "application/json"},
    data=json.dumps(data),
    timeout=10,
)

if response.status_code == 200:
    predictions = response.json()
    print("预测结果:")
    for i, pred in enumerate(predictions["predictions"]):
        print(f"  样本{i}: 流失概率={pred:.4f}")
else:
    print(f"请求失败: {response.status_code}, {response.text}")

health = requests.get("http://localhost:5001/health", timeout=5)
print(f"\n健康检查: {health.status_code}")
```

---

## 九、课后作业

### 必做

1. **流失预测模型**：为L1项目5的用户画像系统添加流失预测模型，使用XGBoost/LightGBM训练，AUC > 0.80
2. **MLflow全生命周期管理**：使用MLflow管理模型全生命周期，包含实验追踪、模型注册、阶段转换、版本管理
3. **漂移检测脚本**：编写模型监控脚本，使用Evidently检测数据漂移，当漂移特征比例超过30%时发送告警

### 选做

1. 搭建Kubeflow Pipelines环境，将训练流程编排为Pipeline
2. 实现A/B测试部署，对比新旧模型的线上效果
3. 实现自动重训练：漂移检测触发 → 自动训练新模型 → 验证通过 → 自动替换Production模型

---

## 十、参考资料

- [MLflow官方文档](https://mlflow.org/docs/latest/index.html)
- [Evidently AI官方文档](https://docs.evidentlyai.com/)
- [Kubeflow Pipelines文档](https://www.kubeflow.org/docs/components/pipelines/)
- [Google MLOps白皮书](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [Weights & Biases文档](https://docs.wandb.ai/)
- [NVIDIA Triton Inference Server](https://github.com/triton-inference-server/server)
