# 46_ДУПЛЕЙМАКСИМ

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Java](https://img.shields.io/badge/Java-16+-orange)
![Node.js](https://img.shields.io/badge/Node.js-16+-green)

Полнофункциональное веб-приложение с разделением на backend и frontend части с интегрированным анализом качества кода через SonarQube и CI/CD pipeline на GitLab.

## 📑 Содержание

- [Особенности](#особенности)
- [Стек технологий](#стек-технологий)
- [Требования к системе](#требования-к-системе)
- [Быстрый старт](#быстрый-старт)
- [Установка](#установка)
- [Запуск приложения](#запуск-приложения)
- [Структура проекта](#структура-проекта)
- [CI/CD Pipeline](#cicd-pipeline)
- [Анализ качества кода](#анализ-качества-кода)
- [Переменные окружения](#переменные-окружения)
- [Разработка](#разработка)
- [Возможные проблемы](#возможные-проблемы)
- [Лицензия](#лицензия)
- [Об авторе](#об-авторе)

## ✨ Особенности

- 🏗️ **Микросервисная архитектура** — разделение backend и frontend
- 🔍 **Непрерывный анализ качества** — интеграция с SonarQube
- 🚀 **CI/CD автоматизация** — GitLab Pipeline для каждого commit
- 🛡️ **SAST сканирование** — автоматическая проверка безопасности
- 📊 **Метрики качества** — отслеживание технического долга
- 🐳 **Docker поддержка** — легкое развёртывание в контейнерах

## 🛠 Стек технологий

### Backend
| Технология | Версия | Назначение |
|-----------|--------|-----------|
| Java | 16+ | Язык программирования |
| Maven | 3.8+ | Управление зависимостями |
| Spring Boot | 2.7+ | REST API фреймворк |
| JUnit | 5+ | Unit тестирование |

### Frontend
| Технология | Версия | Назначение |
|-----------|--------|-----------|
| Node.js | 16+ | Runtime среда |
| npm / yarn | 8+ / 3+ | Менеджер пакетов |
| React / Vue | - | UI фреймворк |
| Webpack / Vite | - | Сборщик модулей |
| ESLint | - | Проверка кода |

### DevOps & Quality Assurance
| Инструмент | Назначение |
|-----------|-----------|
| GitLab CI/CD | Непрерывная интеграция |
| SonarQube | Анализ качества кода |
| Docker | Контейнеризация |
| Maven / npm | Автоматизированная сборка |

## 📋 Требования к системе

### Backend
```bash
Java JDK 16 или выше
Maven 3.8.0 или выше
Git
```

### Frontend
```bash
Node.js 16.0.0 или выше
npm 8.0.0 или выше (или yarn 3.0.0+)
Git
```

### Для анализа качества кода
```bash
SonarQube 9.0 или выше (сервер)
SonarScanner CLI (для frontend)
```

## 🚀 Быстрый старт

```bash
# 1. Клонируйте репозиторий
git clone <repository-url>
cd 46_ДУПЛЕЙМАКСИМ

# 2. Установите backend
cd backend
mvn clean install
cd ..

# 3. Установите frontend
cd frontend
npm install
cd ..

# 4. Создайте файл .env
cp .env.example .env

# 5. Запустите приложение
# Terminal 1 - Backend
cd backend && mvn spring-boot:run

# Terminal 2 - Frontend
cd frontend && npm start
```

Приложение будет доступно на:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **Swagger документация:** http://localhost:8080/swagger-ui.html

## 📦 Установка

### Backend

```bash
cd backend

# Установка зависимостей
mvn clean install

# Пропуск тестов (если нужно)
mvn clean install -DskipTests

# Проверка версии Java
mvn -version
```

### Frontend

```bash
cd frontend

# С использованием npm
npm install

# Или с использованием yarn
yarn install

# Проверка версий
node --version
npm --version
```

## ▶️ Запуск приложения

### Development режим

**Backend:**
```bash
cd backend
mvn spring-boot:run
```

**Frontend:**
```bash
cd frontend
npm start
```

### Production режим

**Backend:**
```bash
cd backend
mvn clean package
java -jar target/app.jar
```

**Frontend:**
```bash
cd frontend
npm run build
npm install -g serve
serve -s build
```

## 📁 Структура проекта

```
46_ДУПЛЕЙМАКСИМ/
├── backend/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   └── resources/
│   │   └── test/
│   ├── pom.xml
│   ├── .gitlab-ci.yml
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── public/
│   ├── package.json
│   ├── .gitlab-ci.yml
│   └── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 🔄 CI/CD Pipeline

Проект использует **GitLab CI/CD** для автоматизации процесса разработки.

### Этапы Pipeline

```mermaid
Build → Test → SAST Analysis → Deploy
```

### Подробное описание

| Этап | Описание | Триггер |
|------|---------|---------|
| **Build** | Сборка backend (Maven) и frontend (npm) | Каждый commit |
| **Test** | Unit тесты и интеграционные тесты | На этапе Build |
| **SAST** | Анализ кода с SonarQube | После успешных тестов |
| **Deploy** | Развёртывание на staging/production | На ветке `main` |

### Поддерживаемые ветки

- `dev` — ветка разработки (запускает все проверки)
- `main` — production ветка (дополнительный deploy)
- `feature/*` — feature-ветки (запускают тесты)

## 🔍 Анализ качества кода

### SonarQube интеграция

Проект использует SonarQube для контроля качества на обеих сторонах приложения.

#### Backend анализ (Java/Maven)

```bash
cd backend
mvn verify sonar:sonar \
  -Dsonar.projectKey=${SONAR_PROJECT_KEY_BACK} \
  -Dsonar.host.url=${SONARQUBE_URL} \
  -Dsonar.login=${SONAR_LOGIN_BACK} \
  -Dsonar.projectName="46_ДУПЛЕЙМАКСИМ_БЭКЭНД" \
  -Dsonar.qualitygate.wait=true
```

#### Frontend анализ (JavaScript/TypeScript)

```bash
cd frontend
sonar-scanner \
  -Dsonar.projectKey=${SONAR_PROJECT_KEY_FRONT} \
  -Dsonar.sources=. \
  -Dsonar.host.url=${SONARQUBE_URL} \
  -Dsonar.login=${SONAR_LOGIN_FRONT} \
  -Dsonar.projectName="46_ДУПЛЕЙМАКСИМ_ФРОНТЕНД"
```

### Метрики качества

SonarQube анализирует:
- 🐛 **Ошибки и баги** — критические проблемы
- 🔐 **Уязвимости безопасности** — потенциальные угрозы
- 📋 **Code Smells** — проблемы с читаемостью и поддерживаемостью
- 🔁 **Дублирование кода** — повторяющиеся блоки
- 📊 **Покрытие тестами** — процент протестированного кода

### Локальная проверка качества

Перед push'ем убедитесь в качестве кода:

```bash
# Backend
cd backend
mvn clean verify

# Frontend
cd frontend
npm run lint
npm run test
```

## 🔐 Переменные окружения

### Создание файла .env

```bash
cp .env.example .env
```

### Backend переменные

```env
# Server
SERVER_PORT=8080
SERVER_SERVLET_CONTEXT_PATH=/api

# Database (если используется)
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/dbname
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=password

# SonarQube
SONAR_PROJECT_KEY_BACK=46_ДУПЛЕЙМАКСИМ_БЭКЭНД
SONARQUBE_URL=https://sonarqube.example.com
SONAR_LOGIN_BACK=your_backend_token_here
```

### Frontend переменные

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8080
REACT_APP_API_TIMEOUT=30000

# SonarQube
SONAR_PROJECT_KEY_FRONT=46_ДУПЛЕЙМАКСИМ_ФРОНТЕНД
SONAR_LOGIN_FRONT=your_frontend_token_here

# Environment
REACT_APP_ENV=development
```

**⚠️ Важно:** Никогда не коммитьте `.env` файл с реальными креденшалами!

## 👨‍💻 Разработка

### Создание новой feature

```bash
# 1. Создайте feature-ветку от dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name

# 2. Разработка и тестирование
# ... ваш код ...

# 3. Локальная проверка
npm run lint        # Frontend
mvn clean verify    # Backend

# 4. Коммит и push
git add .
git commit -m "feat: описание вашей фичи"
git push origin feature/your-feature-name

# 5. Создайте Merge Request в GitLab
```

### Соглашения по коммитам

```
feat: новая функциональность
fix: исправление ошибки
docs: документация
style: форматирование кода
refactor: рефакторинг кода
test: добавление тестов
chore: обновление зависимостей
```

### Стандарты кодирования

- **Java:** Google Java Style Guide
- **JavaScript:** Airbnb JavaScript Style Guide
- **React:** ESLint + Prettier конфигурация

## ⚠️ Возможные проблемы

### Problem: `mvn: command not found`

**Решение:**
```bash
# Проверьте установку Maven
mvn -version

# Если не установлен, установите Maven
# macOS
brew install maven

# Ubuntu/Debian
sudo apt-get install maven

# Windows - скачайте с https://maven.apache.org/download.cgi
```

### Problem: `npm ERR! code EACCES`

**Решение:**
```bash
# Исправьте права доступа
sudo chown -R $(whoami) ~/.npm

# Или переустановите npm
npm install -g npm@latest
```

### Problem: Port already in use

**Решение:**
```bash
# Найдите процесс на порту 3000 (frontend)
lsof -i :3000
kill -9 <PID>

# Или используйте другой порт
PORT=3001 npm start
```

### Problem: SonarQube не доступен

**Решение:**
- Проверьте URL сервера в переменных окружения
- Убедитесь, что токен валиден
- Проверьте сетевую доступность

```textline
[ backend/.gitlab-ci.yml ]
sonarqube-backend-sast:
  stage: test
  image: maven:3.8-openjdk-16
  before_script:
    - cd backend
  script:
    - mvn verify sonar:sonar
        -Dsonar.projectKey=${SONAR_PROJECT_KEY_BACK}
        -Dsonar.host.url=${SONARQUBE_URL}
        -Dsonar.login=${SONAR_LOGIN_BACK}
        -Dsonar.projectName="46_ДУПЛЕЙМАКСИМ_БЭКЭНД"
        -Dsonar.qualitygate.wait=true
  dependencies:
    - build-backend-code-job
  only:
    - dev


[ frontend/.gitlab-ci.yml ]
sonarqube-frontend-sast:
  stage: test
  image: sonarsource/sonar-scanner-cli:latest
  before_script:
    - cd frontend
  script:
    - sonar-scanner
        -Dsonar.projectKey=${SONAR_PROJECT_KEY_FRONT}
        -Dsonar.sources=.
        -Dsonar.host.url=${SONARQUBE_URL}
        -Dsonar.login=${SONAR_LOGIN_FRONT}
        -Dsonar.projectName="46_ДУПЛЕЙМАКСИМ_ФРОНТЕНД"
  dependencies:
    - build-frontend-code-job
  only:
    - dev
```

## 📄 Лицензия

Этот проект лицензирован под MIT License — см. файл [LICENSE](LICENSE) для деталей.

## 👤 Об авторе

**Дуплей Максим Игоревич**

- 🔗 [GitHub](https://github.com/QuadDarv1ne/)
- 📊 [ORCID](https://orcid.org/0009-0007-7605-539X)
- 📧 [Email](::malto::maksimqwe42@mail.ru)

---

<div align="center">

**Спасибо за использование этого проекта ⭐**

Если у вас есть вопросы или предложения — создавайте `Issues` и `Pull Requests`

**Последнее обновление:** 17.10.2025

</div>
