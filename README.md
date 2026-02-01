# Проектная работа: Спринт 6 — High Load & Observability

> **Кейс:** Компания «Александрит» — производство ювелирных украшений на заказ  
> **Проблема:** Система не справляется с ростом нагрузки, заказы теряются, MES тормозит  
> **Решение:** Внедрение Observability-стека и оптимизация производительности

---

## ✅ Чеклист выполнения

| Задание | Статус | Артефакт |
|---------|--------|----------|
| **Task 1.** Анализ архитектуры, проблемы, план инициатив | ✅ Выполнено | [📄 Документ](./Task1/Планирование_анализ_идентификация_проблем_и_поиск_решений.md) |
| **Task 2.** Мониторинг (выбор метрик, подходы RED/USE) | ✅ Выполнено | [📄 Документ](./Task2/Выбор_и_настройка_мониторинга_в_системе.md) |
| **Task 3.** Трейсинг (архитектура + MVP на OpenTelemetry) | ✅ Выполнено | [📄 Документ](./Task3/Архитектурное_решение_по_трейсингу.md), [💻 Код](./Task3/services/), [📸 Скриншот](./Task3/trace_evidence.png) |
| **Task 4.** Логирование (ELK/OpenSearch, политики) | ✅ Выполнено | [📄 Документ](./Task4/Архитектурное_решение_по_логированию.md) |
| **Task 5.** Кеширование (Redis, Cache-Aside, Sequence Diagram) | ✅ Выполнено | [📄 Документ](./Task5/Архитектурное_решение_по_кешированию.md), [📊 Диаграмма](./Task5/MES_Order_Flow_with_Caching.png) |

**Дополнительные задания:**
- [x] Task 2: Показатели насыщенности и пороговые значения
- [x] Task 3: Алертинг на основе данных трейсинга (зелёная диаграмма)
- [x] Task 4: Сравнение технологий (ELK vs OpenSearch vs Splunk)

---

## 📂 Структура репозитория

```
.
├── README.md                          # Этот файл
├── docs/
│   ├── c4-current.puml                # C4-диаграмма "As Is" (PlantUML)
│   └── c4-current.png                 # C4-диаграмма (рендер)
├── Task1/
│   └── Планирование_анализ_...md      # Анализ проблем и план инициатив
├── Task2/
│   └── Выбор_и_настройка_...md        # Стратегия мониторинга
├── Task3/
│   ├── Архитектурное_решение_...md    # Решение по трейсингу
│   ├── k8s/                           # Kubernetes манифесты (Jaeger)
│   ├── services/                      # Код микросервисов (Python/FastAPI)
│   ├── trace_evidence.png             # Скриншот Jaeger UI
│   └── Task3.png                      # Диаграмма архитектуры
├── Task4/
│   └── Архитектурное_решение_...md    # Решение по логированию
└── Task5/
    ├── Архитектурное_решение_...md    # Решение по кешированию
    ├── MES_Order_Flow_with_Caching.puml
    └── MES_Order_Flow_with_Caching.png # Sequence Diagram
```

---

## 🏗 Архитектура "As Is"

Текущее состояние системы «Александрит»:

![C4 Container Diagram](./docs/c4-current.png)

**Ключевые проблемы (подробнее в Task 1):**
- 🔴 SPOF — по одному инстансу на каждый сервис
- 🔴 MES Dashboard тормозит (тяжёлые SQL-запросы)
- 🔴 Сообщения теряются в RabbitMQ (нет DLX)
- 🟡 CRM напрямую обращается к Shop DB (Shared Database антипаттерн)
- 🟡 Нет observability — о проблемах узнаём от клиентов

---

## 🚀 Ключевые решения

### Task 5: Кеширование MES Dashboard

Паттерн **Cache-Aside** + комбинированная инвалидация (TTL + Explicit):

![Caching Sequence Diagram](./Task5/MES_Order_Flow_with_Caching.png)

### Task 3: Распределённый трейсинг (MVP)

Реализован работающий MVP:
- **Jaeger** в Kubernetes (Minikube)
- Два микросервиса на **Python (FastAPI)**
- Авто-инструментация через **OpenTelemetry**

**Скриншот работающего трейса:**

![Jaeger Trace](./Task3/trace_evidence.png)

#### Как запустить локально

```bash
# 1. Запуск Minikube
minikube start --addons=ingress

# 2. Установка Jaeger Operator
kubectl create namespace observability
kubectl apply -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.51.0/jaeger-operator.yaml -n observability
kubectl apply -f Task3/k8s/jaeger-instance.yaml -n observability

# 3. Сборка Docker-образов
eval $(minikube docker-env)
docker build -t service-a:latest Task3/services/service-a/
docker build -t service-b:latest Task3/services/service-b/

# 4. Деплой сервисов
kubectl apply -f Task3/k8s/services.yaml

# 5. Тестовый вызов
kubectl exec -it $(kubectl get pods -l app=service-a -o jsonpath='{.items[0].metadata.name}') \
  -- wget -qO- http://service-a:8080

# 6. Открыть Jaeger UI
kubectl port-forward svc/simplest-query -n observability 16686:16686
# Браузер: http://localhost:16686
```

---

## 📋 Краткое содержание документов

| Документ | Основные разделы |
|----------|------------------|
| **Task 1** | 7 проблем → 8 инициатив → Топ-3 на полгода |
| **Task 2** | RED/USE методологии → 40 метрик → Thresholds → Roadmap |
| **Task 3** | 6 точек отказа → OpenTelemetry + Jaeger → Sampling → Безопасность |
| **Task 4** | JSON-логи → OpenSearch → PII-маскирование → Hot/Warm/Cold retention |
| **Task 5** | Cache-Aside → TTL + Explicit Invalidation → Sequence Diagram → Риски |

---

## 🛠 Технологический стек (предлагаемый)

| Область | Технология |
|---------|------------|
| **Metrics** | Prometheus + Grafana |
| **Tracing** | OpenTelemetry + Jaeger |
| **Logging** | Filebeat + Logstash + OpenSearch + Kibana |
| **Caching** | Redis (Yandex Managed) |
| **Alerting** | Alertmanager + Slack/PagerDuty |

---

*Спринт 6 / Архитектура ПО PRO / 2024*
