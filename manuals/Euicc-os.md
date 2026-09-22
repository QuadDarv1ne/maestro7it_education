# eUICC OS: архитектура и программирование

## 1. Что это

**eUICC OS** — операционная система на чипе **eUICC** (embedded Universal Integrated Circuit Card). Она управляет профилями операторов, безопасной средой и удалённой конфигурацией.

В отличие от традиционной SIM, eUICC OS работает не с одной картой, а с платформой, которую можно переконфигурировать по сети.

---

## 2. Архитектура

### 2.1. Уровни

eUICC OS делится на:

- **верхний уровень** — взаимодействие с LPA, удалёнными серверами и управление профилями;
- **нижний уровень** — безопасность, криптография и жизненный цикл профилей.

### 2.2. Верхний уровень

| Компонент | Назначение |
|---|---|
| LPAe | Local Profile Assistant in eUICC. Взаимодействует с LPA на устройстве и серверами SM-DP+ / SM-DS |
| LPA services | Вспомогательные сервисы для LPA |
| Telecom Framework | Алгоритмы сетевой аутентификации: Milenage, TUAK |
| Profile Package Interpreter | Разбор и установка профильных пакетов |
| Profile Policy Enabler | Исполнение политик профиля, включая Rules Authorisation Table |

### 2.3. Нижний уровень

| Компонент | Назначение |
|---|---|
| ISD-R | Issuer Security Domain — Root. Создаёт ISD-P и управляет их жизненным циклом. В одном eUICC только один ISD-R. Не может быть удалён или отключён |
| ECASD | eUICC Controlling Authority Security Domain. Корень доверия. Хранит сертификаты и ключи |
| ISD-P | Issuer Security Domain — Profile. Безопасный контейнер для одного профиля |
| Криптография | ECDSA, SHA-1, TUAK, Milenage |

### 2.4. Взаимодействие

Основные участники:

- **LPA** на устройстве;
- **eUICC OS** внутри чипа;
- **SM-DP+** — сервер загрузки профилей;
- **SM-DS** — сервер обнаружения;
- **ODS** — сервер обновления ОС.

Обычно активен один ISD-P. Несколько активных профилей поддерживаются через **MEP** (Multiple Enabled Profiles).

---

## 3. Программирование

### 3.1. Java Card

eUICC может поддерживать Java Card. Типовые пакеты:

- java.*;
- javacard.*;
- javacardx.*;
- uicc.*;
- uicc.usim.*;

Апплеты eUICC — это Java Card апплеты. Они управляются APDU-командами ISO 7816 или работают как сервлеты.

Для загрузки и установки приложений используется **TCALoader**.

### 3.2. Интерфейсы ES10x

| Интерфейс | Назначение |
|---|---|
| ES10a | Получение адресов SM-DS / SM-DP+ |
| ES10b | PrepareDownload, LoadBoundProfilePackage, GetEUICCInfo, AuthenticateServer |
| ES10c | GetProfilesInfo, EnableProfile, DisableProfile |

Команды передаются через **STORE DATA APDU** по защищённому каналу **SCP03**.

### 3.3. Android API

Основные классы:

- **EuiccManager** — высокоуровневые операции: downloadSubscription(), switchToSubscription(), deleteSubscription();
- **EuiccService** — расширяется OEM для создания LPA;
- **EuiccCardManager** — низкоуровневые ES10x-функции.

Пример получения менеджера:

    EuiccManager mgr = (EuiccManager) context.getSystemService(Context.EUICC_SERVICE);
    if (mgr == null || !mgr.isEnabled()) {
        return;
    }
    EuiccInfo info = mgr.getEuiccInfo();
    String osVer = info.getOsVersion();

### 3.4. Формат профиля

Профильный пакет описан в **ASN.1** и кодируется в **TLV** с использованием **DER**. Зашифрованный пакет называется **Bound Profile Package**.

### 3.5. Обновление ОС

Обновление eUICC OS выполняется через **ODS**. Поддержка обновления объявляется в **EIS** через OSUpdateSupported в AdditionalProperties.

---

## 4. Безопасность и чувствительность к взлому

eUICC OS не является «лёгкой» для взлома, но чувствительна к качеству реализации и физическим атакам.

Основные требования:

- устойчивость к атакам по сторонним каналам;
- изоляция профилей;
- защита ключей в ECASD;
- запрет неавторизованного повышения привилегий;
- сертификация GSMA eSA и Common Criteria.

Возможные векторы атак:

- физический доступ к чипу;
- side-channel analysis;
- fault injection;
- уязвимости firmware;
- компрометация цепочки поставок;
- атаки на LPA и интерфейсы ES10x.

**Вывод:** eUICC OS спроектирована как защищённая платформа, но её стойкость зависит от реализации, сертификации и защиты ключей.

---

## 5. Стандарты

- GSMA SGP.22
- GSMA SGP.02
- ETSI TS 102 221
- GlobalPlatform
- Java Card 3.0.4 Classic
