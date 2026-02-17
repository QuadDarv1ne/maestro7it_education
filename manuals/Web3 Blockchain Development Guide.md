# 1⃣ Web3 и блокчейн разработка: Полное руководство по децентрализованным приложениям

В данном разделе курса будет рассмотрено основное введение в Web3 и блокчейн технологии, включая фундаментальные концепции, разработку смарт-контрактов и создание децентрализованных приложений.

## Содержание:
1. **Введение в Web3 и блокчейн**
   - Что такое децентрализованный интернет
   - История развития блокчейн технологий
   - Основные концепции: блоки, транзакции, консенсус
   - Отличия Web3 от традиционного веба

2. **Фундаментальные технологии**
   - Блокчейн основы: криптографические хэш-функции, асимметричная криптография
   - Механизмы консенсуса (PoW, PoS, PoA)
   - Меркльские деревья
   - Сетевые протоколы: P2P сети, gossip протоколы

3. **Разработка смарт-контрактов**
   - Язык Solidity для Ethereum
   - Язык Rust для Solana
   - Паттерны проектирования смарт-контрактов
   - Тестирование смарт-контрактов

4. **Децентрализованные приложения (dApps)**
   - Архитектура dApps
   - Интеграция с фронтендом
   - Хранение данных в IPFS
   - Использование оракулов

5. **NFT и цифровые активы**
   - Стандарты токенов: ERC-20, ERC-721, ERC-1155
   - Создание NFT коллекций
   - Маркетплейсы NFT

6. **Криптовалютные протоколы**
   - DeFi протоколы: AMM, кредитование, ферминг доходности
   - Примеры DeFi контрактов
   - Автоматизированные биржевые протоколы

7. **Практические инструменты**
   - Среды разработки: Hardhat, Truffle, Anchor
   - Тестирование и симуляция
   - Интеграция с MetaMask

8. **Безопасность и аудит**
   - Распространенные уязвимости
   - Лучшие практики безопасности
   - Инструменты аудита

9. **Деплой и интеграция**
   - Деплой на тестовые сети
   - Деплой на основные сети
   - Интеграция с фронтендом

10. **Будущее Web3**
   - Layer 2 решения
   - Cross-chain взаимодействие
   - Zero-knowledge доказательства

---

## Введение в Web3 и блокчейн

**Web3** — это следующая эволюция интернета, ориентированная на децентрализованные, управляемые сообществами сервисы, построенные на блокчейн-технологиях. В отличие от Web2, где крупные корпорации контролируют данные пользователей, Web3 позволяет пользователям владеть своими данными и цифровыми активами.

### История развития блокчейн технологий

Концепция блокчейна была впервые реализована в 2008 году с появлением Bitcoin, созданного неизвестным лицом или группой под псевдонимом Сатоши Накамото. Эта технология позволила создать первую децентрализованную цифровую валюту без необходимости доверия к центральному органу.

В 2013 году Виталик Бутerin предложил Ethereum — платформу для "умных контрактов", которая значительно расширила возможности блокчейна за пределы простых финансовых транзакций.

### Основные концепции

- **Блоки**: структуры данных, содержащие транзакции
- **Транзакции**: операции, записываемые в блокчейн
- **Консенсус**: механизм достижения согласия в децентрализованной сети

### Отличия Web3 от традиционного веба

- **Владение активами**: пользователи владеют своими цифровыми активами, а не третьи лица
- **Децентрализация**: нет единой точки отказа
- **Прозрачность**: все транзакции публичны и проверяемы
- **Неизменяемость**: однажды записанные данные нельзя изменить

---

## Фундаментальные технологии

### Блокчейн основы

**Криптографические хэш-функции** — это односторонние математические функции, которые принимают входные данные любого размера и возвращают результат фиксированного размера. Наиболее распространенные алгоритмы:
- SHA-256 (используется в Bitcoin)
- Keccak-256 (используется в Ethereum)

**Асимметричная криптография** — система, использующая пару ключей: публичный и приватный. Приватный ключ используется для подписи транзакций, а публичный — для проверки подписей.

### Механизмы консенсуса

- **PoW (Proof of Work)**: участники решают сложные математические задачи для добавления блоков
- **PoS (Proof of Stake)**: участники "замораживают" криптовалюту в качестве залога
- **PoA (Proof of Authority)**: проверенные узлы имеют право создавать блоки

### Меркльские деревья

Меркльское дерево — это древовидная структура данных, где каждый листовой узел содержит хэш данных, а каждый нелистовой узел содержит хэш своих дочерних узлов. Это позволяет эффективно проверять принадлежность транзакции блоку.

### Сетевые протоколы

- **P2P сети**: децентрализованные сети, где каждый узел является равноправным участником
- **Gossip протоколы**: метод распространения информации, при котором узлы обмениваются данными случайным образом

---

## Разработка смарт-контрактов

### Solidity (Ethereum)

Solidity — это объектно-ориентированный язык программирования высокого уровня для написания смарт-контрактов на Ethereum.

#### Пример базового токена:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleToken {
    string public name = "Simple Token";
    string public symbol = "SMP";
    uint256 public totalSupply;
    mapping(address => uint256) public balances;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10**18; // стандартный формат с 18 знаками после запятой
        balances[msg.sender] = totalSupply;
    }
    
    function transfer(address to, uint256 value) public returns (bool) {
        require(balances[msg.sender] >= value, "Insufficient balance");
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
    
    function approve(address spender, uint256 value) public returns (bool) {
        // Реализация функции одобрения
        return true;
    }
}
```

### Rust (Solana)

Rust — это системный язык программирования, который используется для написания смарт-контрактов в экосистеме Solana.

#### Пример программы на Rust для Solana:

```rust
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    pubkey::Pubkey,
    program_error::ProgramError,
    rent::Rent,
    system_instruction,
    system_program,
    sysvar::Sysvar,
};

entrypoint!(process_instruction);

fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    let accounts_iter = &mut accounts.iter();
    let payer = next_account_info(accounts_iter)?;
    
    if !payer.is_signer {
        return Err(ProgramError::MissingRequiredSignature);
    }
    
    msg!("Hello from Solana Smart Contract!");
    
    Ok(())
}
```

### Паттерны проектирования смарт-контрактов

- **Ownable**: позволяет ограничить вызов функций только владельцем
- **Pausable**: позволяет приостановить выполнение контракта
- **Access Control**: более гибкий контроль доступа
- **Proxy**: позволяет обновлять логику контракта без изменения адреса

---

## Децентрализованные приложения (dApps)

### Архитектура dApps

Типичная архитектура dApp включает:
- **Frontend**: интерфейс на React, Vue или другом фреймворке
- **Web3 библиотеки**: Web3.js, ethers.js или sol-wallet-js
- **Смарт-контракты**: логика на блокчейне
- **Хранение данных**: IPFS, Filecoin или Arweave

### Пример структуры проекта dApp:

```
dapp-project/
├── frontend/           # React/Vue приложение
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── contracts/          # Смарт-контракты
│   ├── SimpleToken.sol
│   └── MyNFT.sol
├── tests/              # Тесты смарт-контрактов
├── scripts/            # Скрипты деплоя
├── hardhat.config.js   # Конфигурация Hardhat
└── package.json
```

### Интеграция с фронтендом

Для интеграции с фронтендом используются библиотеки Web3:

```javascript
import { ethers } from 'ethers';

// Подключение к MetaMask
if (window.ethereum) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const signer = provider.getSigner();
    
    // Подключение к смарт-контракту
    const contractAddress = "0x...";
    const abi = [...]; // ABI контракта
    
    const contract = new ethers.Contract(contractAddress, abi, signer);
    
    // Вызов функции контракта
    try {
        const tx = await contract.transfer(toAddress, amount);
        await tx.wait();
        console.log("Transaction successful!");
    } catch (error) {
        console.error("Transaction failed:", error);
    }
}
```

### Хранение данных в IPFS

IPFS (InterPlanetary File System) — это децентрализованная система хранения и доступа к файлам. Для хранения метаданных NFT часто используются:
- IPFS для хранения изображений и описаний
- CID (Content Identifier) для ссылки на файлы

---

## NFT и цифровые активы

### Стандарты токенов

- **ERC-20**: стандарт для взаимозаменяемых токенов
- **ERC-721**: стандарт для невзаимозаменяемых токенов (NFT)
- **ERC-1155**: стандарт для мульти-токенов (может быть как взаимозаменяемым, так и невзаимозаменяемым)

### Создание NFT

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter;
    
    constructor() ERC721("MyNFT", "MNFT") {
        tokenCounter = 0;
    }
    
    function createNFT(address recipient, string memory tokenURI) 
        public onlyOwner returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter++;
        return newTokenId;
    }
}
```

### NFT маркетплейсы

NFT маркетплейсы позволяют пользователям покупать, продавать и торговать NFT. Они обычно включают:
- Возможность выставления NFT на продажу
- Аукционные механизмы
- Комиссии за сделки
- Листинговые сборы

---

## Криптовалютные протоколы

### DeFi протоколы

**DeFi (Decentralized Finance)** — это экосистема децентрализованных финансовых услуг:
- **AMM (Automated Market Makers)**: алгоритмические биржи, такие как Uniswap
- **Lending protocols**: протоколы кредитования, такие как Aave
- **Yield farming**: заработок на предоставлении ликвидности
- **Staking mechanisms**: стейкинг токенов для получения вознаграждений

### Пример DeFi контракта

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SimpleLending {
    mapping(address => uint256) public deposits;
    mapping(address => uint256) public loans;
    mapping(address => uint256) public loanStartTime;
    
    uint256 public constant INTEREST_RATE = 10; // 10% годовых
    
    event Deposit(address indexed user, uint256 amount);
    event Borrow(address indexed user, uint256 amount);
    event Repay(address indexed user, uint256 amount);
    
    function deposit() public payable {
        deposits[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    function borrow(uint256 amount) public {
        require(deposits[msg.sender] >= amount * 150 / 100, "Insufficient collateral");
        require(loans[msg.sender] == 0, "Outstanding loan exists");
        
        loans[msg.sender] = amount;
        loanStartTime[msg.sender] = block.timestamp;
        payable(msg.sender).transfer(amount);
        
        emit Borrow(msg.sender, amount);
    }
    
    function repay() public payable {
        uint256 loanAmount = loans[msg.sender];
        require(loanAmount > 0, "No outstanding loan");
        
        // Расчет процентов
        uint256 timeElapsed = block.timestamp - loanStartTime[msg.sender];
        uint256 interest = (loanAmount * INTEREST_RATE * timeElapsed) / (365 days * 100);
        uint256 totalRepayment = loanAmount + interest;
        
        require(msg.value >= totalRepayment, "Insufficient repayment amount");
        
        loans[msg.sender] = 0;
        
        // Возврат излишка
        if (msg.value > totalRepayment) {
            payable(msg.sender).transfer(msg.value - totalRepayment);
        }
        
        emit Repay(msg.sender, totalRepayment);
    }
}
```

---

## Практические инструменты

### Среды разработки

- **Hardhat**: для разработки на Ethereum
- **Truffle**: фреймворк для разработки, тестирования и деплоя смарт-контрактов
- **Anchor**: для разработки на Solana
- **Ganache**: локальный блокчейн для тестирования

### Тестирование смарт-контрактов

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleToken", function() {
    let token;
    let owner;
    let addr1;
    
    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();
        const SimpleToken = await ethers.getContractFactory("SimpleToken");
        token = await SimpleToken.deploy(1000);
    });
    
    it("Should return correct name", async function() {
        expect(await token.name()).to.equal("Simple Token");
    });
    
    it("Should transfer tokens correctly", async function() {
        await token.transfer(addr1.address, 100);
        expect(await token.balances(addr1.address)).to.equal(100);
    });
});
```

### Интеграция с MetaMask

`MetaMask` — это кошелек, который позволяет пользователям взаимодействовать с `dApps`

**Для интеграции:**

1. Проверить наличие `MetaMask`
2. Запросить разрешение на подключение
3. Подписать транзакции

---

## Безопасность и аудит

### Распространенные уязвимости

- **Reentrancy**: повторный вызов функции до завершения предыдущего вызова
- **Integer overflow/underflow**: выход за пределы диапазона целых чисел
- **Access control**: неправильное ограничение доступа
- **Logic errors**: ошибки в бизнес-логике

### Лучшие практики безопасности

- Использование проверок и защитных механизмов
- Тестирование граничных условий
- Регулярные аудиты кода
- Использование проверенных библиотек, таких как `OpenZeppelin`

### Инструменты аудита

- **Slither**: статический анализатор для `Solidity`
- **Mythril**: символьный исполнитель для анализа безопасности
- **SmartCheck**: инструмент для обнаружения уязвимостей

---

## Деплой и интеграция

### Деплой на тестовые сети

**Для безопасного тестирования контрактов используются тестовые сети:**

- Rinkeby, Ropsten, Goerli (для Ethereum)
- Devnet (для Solana)

### Деплой на основные сети

**При деплое на основные сети:**

1. Тщательное тестирование на тестовых сетях
2. Проверка безопасности
3. Верификация исходного кода
4. Мониторинг производительности

### Интеграция с фронтендом

```javascript
import { ethers } from 'ethers';

// Подключение к блокчейну
async function connectWallet() {
    if (typeof window.ethereum !== 'undefined') {
        try {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            const signer = provider.getSigner();
            
            return { provider, signer };
        } catch (error) {
            console.error("User denied account access", error);
        }
    } else {
        alert("Please install MetaMask!");
    }
}

// Вызов смарт-контракта
async function callContractFunction(contractAddress, abi, functionName, params) {
    const { signer } = await connectWallet();
    
    if (signer) {
        const contract = new ethers.Contract(contractAddress, abi, signer);
        
        try {
            const result = await contract[functionName](...params);
            return result;
        } catch (error) {
            console.error("Contract call failed:", error);
        }
    }
}
```

---

## Будущее Web3

### Layer 2 решения

Layer 2 решения решают проблему масштабируемости блокчейнов:

- **Rollups**: Optimistic и ZK-Rollups
- **Sidechains**: независимые блокчейны, связанные с основной сетью
- **State channels**: внецепочечные решения

### Cross-chain взаимодействие

Cross-chain протоколы позволяют взаимодействовать между различными блокчейнами:

- **Atomic swaps**: прямой обмен токенами
- **Bridge протоколы**: связующие протоколы между сетями
- **Interoperability протоколы**: общие протоколы взаимодействия

### Zero-knowledge доказательства

`ZKP` позволяют доказать знание информации без раскрытия самой информации.

**Это открывает возможности для:**

- Приватных транзакций
- Эффективного масштабирования
- Подтверждения вычислений

---

## Итоговые выводы

`Web3` и блокчейн технологии продолжают быстро развиваться, открывая новые возможности для создания децентрализованных приложений.

**Разработчики должны понимать:**

- Фундаментальные концепции блокчейна
- Языки программирования для смарт-контрактов
- Архитектуру dApps
- Безопасность и лучшие практики
- Перспективные направления развития

С развитием этой технологии мы можем ожидать дальнейшей децентрализации интернета и новых форм цифрового взаимодействия.

---

**Автор**: Дуплей Максим Игоревич

**Дата**: 17.02.2026

**Версия**: 1.0
