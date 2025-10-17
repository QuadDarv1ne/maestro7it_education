

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

---

**Дата:** 17.10.2025
