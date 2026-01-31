# ☸️ Полный мануал по Kubernetes: От основ до продвинутых практик

## 📋 Содержание

1. [Введение в Kubernetes](#введение-в-kubernetes)
2. [Архитектура Kubernetes](#архитектура-kubernetes)
3. [Установка и настройка](#установка-и-настройка)
4. [Основные концепции](#основные-концепции)
5. [Pods и контейнеры](#pods-и-контейнеры)
6. [Services и сетевое взаимодействие](#services-и-сетевое-взаимодействие)
7. [Deployments и обновления](#deployments-и-обновления)
8. [Хранение данных (Volumes)](#хранение-данных-volumes)
9. [Конфигурация и секреты](#конфигурация-и-секреты)
10. [Масштабирование и авторегулирование](#масштабирование-и-авторегулирование)
11. [Мониторинг и логирование](#мониторинг-и-логирование)
12. [Безопасность](#безопасность)
13. [Сетевые политики](#сетевые-политики)
14. [Helm и управление чартами](#helm-и-управление-чартами)
15. [Продвинутые темы](#продвинутые-темы)
16. [Лучшие практики](#лучшие-практики)

## Введение в Kubernetes

**Kubernetes** (произносится как "кубернетис" или "k8s") — это открытое программное обеспечение для автоматизации развертывания, масштабирования и управления контейнеризированными приложениями.

### Что такое Kubernetes?

Kubernetes был первоначально разработан Google на основе их внутренней системы Borg. В 2014 году проект был открыт и передан в Cloud Native Computing Foundation (CNCF).

### Основные возможности:

- **Автоматизация развертывания** — автоматическое запуск и оркестрация контейнеров
- **Самовосстановление** — автоматический перезапуск упавших контейнеров
- **Горизонтальное масштабирование** — автоматическое увеличение/уменьшение количества экземпляров
- **Балансировка нагрузки** — автоматическое распределение трафика между подами
- **Обновления без простоя** — постепенное обновление приложений без downtime
- **Хранение данных** — автоматическое монтирование систем хранения
- **Самоконтроль** — автоматическое восстановление после сбоев

### Когда использовать Kubernetes?

✅ **Подходит для:**
- Микросервисных архитектур
- Приложений с высокой нагрузкой
- Систем, требующих высокой доступности
- Проектов с частыми деплоями
- Команд разработчиков среднего и большого размера

❌ **Не всегда нужно для:**
- Простых односервисных приложений
- Статических сайтов
- Приложений без контейнеров
- Очень маленьких команд (до 3 человек)

## Архитектура Kubernetes

### Компоненты Control Plane

Control Plane управляет всем кластером Kubernetes и состоит из следующих компонентов:

#### 1. kube-apiserver
- **Функция:** Единая точка входа для всех REST-запросов
- **Отвечает за:** Аутентификацию, авторизацию, валидацию запросов
- **Порт:** 6443 (HTTPS)

#### 2. etcd
- **Функция:** Распределенное хранилище ключ-значение
- **Хранит:** Всю информацию о состоянии кластера
- **Важно:** Критически важный компонент — потеря данных etcd = потеря кластера

#### 3. kube-scheduler
- **Функция:** Распределяет поды по нодам
- **Учитывает:** Ресурсы, ограничения, affinity/anti-affinity правила

#### 4. kube-controller-manager
- **Функция:** Запускает контроллеры, которые управляют состоянием кластера
- **Контроллеры:**
  - Node Controller (следит за состоянием нод)
  - Replication Controller (поддерживает нужное количество подов)
  - Endpoints Controller (связывает Services и Pods)
  - Service Account & Token Controllers

#### 5. cloud-controller-manager (опционально)
- **Функция:** Взаимодействует с облачными провайдерами
- **Интеграции:** AWS, GCP, Azure, OpenStack

### Компоненты Worker Nodes

Worker Nodes выполняют рабочую нагрузку приложений:

#### 1. kubelet
- **Функция:** Агент на каждой ноде
- **Отвечает за:** Запуск подов, мониторинг состояния, отчеты в Control Plane

#### 2. kube-proxy
- **Функция:** Сетевой прокси
- **Обеспечивает:** Сетевые правила, балансировку нагрузки, service discovery

#### 3. Container Runtime
- **Функция:** Выполняет контейнеры
- **Поддерживаемые:** Docker, containerd, CRI-O

### Сетевая модель Kubernetes

#### Основные принципы:
1. **Каждый Pod получает уникальный IP адрес**
2. **Все Pod могут общаться друг с другом без NAT**
3. **Агенты на нодах могут общаться со всеми Pod без NAT**

#### Реализации сетевых плагинов:
- **Calico** — сетевая политика, высокая производительность
- **Flannel** — простота, overlay networking
- **Cilium** — сетевая безопасность на уровне L7
- **Weave Net** — mesh networking

## Установка и настройка

### Вариант 1: Minikube (для локальной разработки)

Minikube создает однонодовый кластер Kubernetes локально.

#### Установка Minikube:

```bash
# Windows (через Chocolatey)
choco install minikube

# Или скачать напрямую
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-windows-amd64.exe
ren minikube-windows-amd64.exe minikube.exe

# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

#### Запуск кластера:

```bash
# Запуск с драйвером по умолчанию
minikube start

# Запуск с конкретным драйвером
minikube start --driver=docker
minikube start --driver=hyperv
minikube start --driver=virtualbox

# Запуск с дополнительными компонентами
minikube start --addons=dashboard,ingress,metrics-server

# Проверка статуса
minikube status

# Получение информации о кластере
kubectl cluster-info
```

#### Полезные команды Minikube:

```bash
# Открыть Dashboard
minikube dashboard

# Получить IP кластера
minikube ip

# SSH в ноду
minikube ssh

# Остановить кластер
minikube stop

# Удалить кластер
minikube delete
```

### Вариант 2: kubeadm (производственный кластер)

kubeadm используется для создания production-ready кластеров.

#### Предварительные требования:

```bash
# Отключение swap (обязательно для Kubernetes)
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Загрузка модулей ядра
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

# Установка runtime (containerd)
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
```

#### Установка kubeadm:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg

echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# CentOS/RHEL
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

#### Создание кластера:

```bash
# На Control Plane ноде
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Настройка kubectl для обычного пользователя
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Установка сетевого плагина (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Получение команды для присоединения worker нод
kubeadm token create --print-join-command
```

#### Присоединение worker нод:

```bash
# На каждой worker ноде выполнить команду из вывода выше
sudo kubeadm join <control-plane-host>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

### Вариант 3: Managed Kubernetes (облачные провайдеры)

#### Amazon EKS:

```bash
# Установка eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Создание кластера
eksctl create cluster \
  --name my-cluster \
  --version 1.27 \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed
```

#### Google GKE:

```bash
# Установка gcloud CLI
# Следуйте инструкциям: https://cloud.google.com/sdk/docs/install

# Создание кластера
gcloud container clusters create my-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-medium

# Получение учетных данных
gcloud container clusters get-credentials my-cluster --zone us-central1-a
```

#### Azure AKS:

```bash
# Создание группы ресурсов
az group create --name myResourceGroup --location eastus

# Создание кластера
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Получение учетных данных
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```

## Основные концепции

### 1. Pod

**Pod** — наименьшая единица развертывания в Kubernetes. Может содержать один или несколько контейнеров, которые разделяют сеть и хранилище.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

### 2. Service

**Service** обеспечивает стабильную сетевую точку доступа к набору подов.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP  # или NodePort, LoadBalancer
```

### 3. Deployment

**Deployment** управляет ReplicaSets и обеспечивает декларативные обновления приложений.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### 4. Namespace

**Namespace** предоставляет механизм изоляции ресурсов внутри одного кластера.

```bash
# Создание namespace
kubectl create namespace development

# Просмотр namespaces
kubectl get namespaces

# Использование namespace
kubectl get pods -n development
```

### 5. ConfigMap и Secret

**ConfigMap** хранит конфигурационные данные, **Secret** — чувствительную информацию.

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgresql://localhost:5432/mydb"
  log_level: "info"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: bXl1c2Vy  # base64 encoded "myuser"
  password: bXlwYXNz  # base64 encoded "mypass"
```

## Pods и контейнеры

### Создание Pod:

```bash
# Из YAML файла
kubectl apply -f pod.yaml

# Однострочная команда
kubectl run nginx-pod --image=nginx:1.21 --port=80

# Интерактивный режим
kubectl run debug-pod --image=busybox --restart=Never -it -- sh
```

### Управление Pod:

```bash
# Просмотр подов
kubectl get pods
kubectl get pods -o wide
kubectl get pods -n kube-system

# Получение подробной информации
kubectl describe pod nginx-pod

# Просмотр логов
kubectl logs nginx-pod
kubectl logs nginx-pod -f  # следить за логами в реальном времени

# Выполнение команд в поде
kubectl exec -it nginx-pod -- sh
kubectl exec nginx-pod -- ps aux

# Удаление пода
kubectl delete pod nginx-pod
kubectl delete -f pod.yaml
```

### Multi-container Pods:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: web
    image: nginx
    ports:
    - containerPort: 80
  - name: logger
    image: busybox
    command: ['sh', '-c', 'while true; do date >> /var/log/app.log; sleep 30; done']
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  volumes:
  - name: shared-logs
    emptyDir: {}
```

### Init Containers:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  containers:
  - name: main-app
    image: nginx
    volumeMounts:
    - name: workdir
      mountPath: /usr/share/nginx/html
  initContainers:
  - name: install
    image: busybox
    command: ['sh', '-c', 'echo "Hello from init container" > /work-dir/index.html']
    volumeMounts:
    - name: workdir
      mountPath: /work-dir
  volumes:
  - name: workdir
    emptyDir: {}
```

## Services и сетевое взаимодействие

### Типы Services:

#### 1. ClusterIP (по умолчанию):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```

#### 2. NodePort:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport-service
spec:
  type: NodePort
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
    nodePort: 30007  # порт на ноде (30000-32767)
```

#### 3. LoadBalancer:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-lb-service
spec:
  type: LoadBalancer
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```

#### 4. ExternalName:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-database
spec:
  type: ExternalName
  externalName: database.company.com
```

### Headless Services:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: headless-service
spec:
  clusterIP: None
  selector:
    app: MyApp
  ports:
  - port: 80
    targetPort: 9376
```

### Ingress:

Ingress управляет внешним доступом к сервисам в кластере.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
      - path: /app2
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
```

### Network Policies:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

## Deployments и обновления

### Создание Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### Управление Deployments:

```bash
# Создание
kubectl apply -f deployment.yaml

# Просмотр
kubectl get deployments
kubectl describe deployment nginx-deployment

# Масштабирование
kubectl scale deployment nginx-deployment --replicas=5

# Обновление образа
kubectl set image deployment/nginx-deployment nginx=nginx:1.22

# Откат изменений
kubectl rollout undo deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment --to-revision=2

# Просмотр истории
kubectl rollout history deployment/nginx-deployment

# Проверка статуса
kubectl rollout status deployment/nginx-deployment
```

### Стратегии обновления:

#### Rolling Update (по умолчанию):

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

#### Recreate:

```yaml
spec:
  strategy:
    type: Recreate
```

### Health Checks:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-check-deployment
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Хранение данных (Volumes)

### Типы Volumes:

#### 1. emptyDir:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: nginx
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

#### 2. hostPath:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: nginx
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      path: /data
      type: Directory
```

#### 3. PersistentVolume и PersistentVolumeClaim:

```yaml
# PersistentVolume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"

---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi

---
# Pod использующий PVC
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: pvc-claim
```

### Storage Classes:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate
```

## Конфигурация и секреты

### ConfigMaps:

#### Создание из литералов:

```bash
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

#### Создание из файла:

```bash
kubectl create configmap game-config --from-file=config/game.properties
```

#### Использование в Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: registry.k8s.io/busybox
      command: [ "/bin/sh", "-c", "env" ]
      envFrom:
      - configMapRef:
          name: special-config
  restartPolicy: Never
```

### Secrets:

#### Создание Secret:

```bash
# Из литералов
kubectl create secret generic db-user-pass \
  --from-literal=username=myuser \
  --from-literal=password=mypass

# Из файлов
kubectl create secret generic db-user-pass \
  --from-file=./username.txt \
  --from-file=./password.txt
```

#### Использование Secret:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: mycontainer
    image: redis
    env:
      - name: SECRET_USERNAME
        valueFrom:
          secretKeyRef:
            name: db-user-pass
            key: username
      - name: SECRET_PASSWORD
        valueFrom:
          secretKeyRef:
            name: db-user-pass
            key: password
```

## Масштабирование и авторегулирование

### Horizontal Pod Autoscaler (HPA):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

#### Управление HPA:

```bash
# Создание HPA
kubectl apply -f hpa.yaml

# Просмотр HPA
kubectl get hpa

# Получение подробной информации
kubectl describe hpa php-apache
```

### Vertical Pod Autoscaler (VPA):

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: "*"
      maxAllowed:
        cpu: 1
        memory: 500Mi
      minAllowed:
        cpu: 100m
        memory: 50Mi
```

## Мониторинг и логирование

### Установка Prometheus и Grafana:

```bash
# Добавление helm репозитория
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Установка kube-prometheus-stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Просмотр метрик:

```bash
# Port-forward для доступа к Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Port-forward для доступа к Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

### Логирование с Fluentd и Elasticsearch:

```yaml
# Fluentd DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1.14.6-debian-elasticsearch7-1.0
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.monitoring.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

## Безопасность

### Role-Based Access Control (RBAC):

#### Создание Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

#### Создание RoleBinding:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Network Policies:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Pod Security Standards:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: sec-ctx-demo
    image: busybox
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
```

## Сетевые политики

### Ingress Traffic Control:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### Egress Traffic Control:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
spec:
  podSelector:
    matchLabels:
      app: internal
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: production
```

## Helm и управление чартами

### Установка Helm:

```bash
# macOS
brew install helm

# Windows (через Chocolatey)
choco install kubernetes-helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Основные команды Helm:

```bash
# Поиск чартов
helm search hub wordpress

# Установка чарта
helm install my-wordpress bitnami/wordpress

# Просмотр установленных релизов
helm list

# Обновление релиза
helm upgrade my-wordpress bitnami/wordpress --set replicaCount=3

# Откат релиза
helm rollback my-wordpress 1

# Удаление релиза
helm uninstall my-wordpress
```

### Создание своего чарта:

```bash
# Создание шаблона чарта
helm create myapp

# Структура чарта:
# myapp/
# ├── Chart.yaml
# ├── values.yaml
# ├── charts/
# └── templates/
#     ├── deployment.yaml
#     ├── service.yaml
#     └── _helpers.tpl
```

## Продвинутые темы

### StatefulSets:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

### DaemonSets:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: quay.io/fluentd_elasticsearch/fluentd:v2.5.2
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

### Jobs и CronJobs:

```yaml
# Job
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4

---
# CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

## Лучшие практики

### 1. Организация ресурсов:

```yaml
# Используйте namespace для изоляции
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    name: production

---
# Используйте labels для группировки
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: production
  labels:
    app: backend
    version: v1.2.3
    environment: production
    tier: backend
```

### 2. Ресурсные ограничения:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 3. Health Checks:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
```

### 4. Безопасность:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### 5. Конфигурация через ConfigMaps и Secrets:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgresql://db:5432/myapp"
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=  # base64 encoded

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

> Этот мануал охватывает основные аспекты Kubernetes.  Для более глубокого изучения рекомендуется практиковаться на реальных примерах и изучать официальную документацию.