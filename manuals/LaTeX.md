# LaTeX - Полное руководство по системе компьютерной верстки

## Что такое LaTeX?

`LaTeX` - это профессиональная система компьютерной верстки, разработанная для создания высококачественных технических и научных документов.

В отличие от обычных текстовых редакторов, LaTeX позволяет сосредоточиться на содержании документа, а форматированием занимается система автоматически.

### Основные преимущества LaTeX:

- Профессиональное качество типографики
- Автоматическая нумерация разделов, формул, рисунков
- Удобное управление библиографией
- Отличная поддержка математических формул
- Кроссплатформенность
- Бесплатность и открытый исходный код

## Установка LaTeX

### Windows

#### MiKTeX (рекомендуется для начинающих)

1. Скачайте установщик с официального сайта: https://miktex.org/download
2. Запустите установщик и следуйте инструкциям
3. Выберите "Install MiKTeX" для автоматической установки
4. После установки рекомендуется установить редактор TeXstudio

#### TeX Live

1. Скачайте установщик с https://www.tug.org/texlive/
2. Запустите install-tl-windows.bat
3. Следуйте инструкциям установщика

### macOS

#### MacTeX (полная установка)

1. Скачайте MacTeX с https://www.tug.org/mactex/
2. Откройте скачанный .pkg файл
3. Следуйте инструкциям установщика

#### BasicTeX (минимальная установка)

1. Скачайте BasicTeX с того же сайта
2. Установите через .pkg файл
3. При необходимости доустановите пакеты через tlmgr

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install texlive-full
# Или минимальную версию:
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
```

#### Fedora/RHEL

```bash
sudo dnf install texlive-scheme-full
# Или минимальную версию:
sudo dnf install texlive-latex texlive-collection-fontsrecommended
```

#### Arch Linux

```bash
sudo pacman -S texlive-most
# Или полную установку:
sudo pacman -S texlive-most texlive-lang
```

## Редакторы LaTeX

### TeXstudio (рекомендуется)

- Бесплатный и кроссплатформенный
- Интуитивный интерфейс
- Встроенная проверка синтаксиса
- Автозавершение команд

Скачать: https://www.texstudio.org/

### Overleaf (онлайн)

- Веб-редактор LaTeX
- Совместная работа в реальном времени
- Нет необходимости в локальной установке
- Большое количество шаблонов

Сайт: https://www.overleaf.com/

### VS Code с расширениями

- Установите расширение "LaTeX Workshop"
- Поддержка современного редактора
- Хорошая интеграция с системами контроля версий

## Базовый синтаксис LaTeX

### Структура документа

```latex
\documentclass{article}

% Преамбула - настройки документа
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{amsmath}
\usepackage{graphicx}

\title{Заголовок документа}
\author{Автор}
\date{\today}

\begin{document}

\maketitle

\section{Первый раздел}
Это первый раздел документа.

\subsection{Подраздел}
Это подраздел первого раздела.

\section{Второй раздел}
Это второй раздел.

\end{document}
```

### Основные команды

#### Структура документа

```latex
\documentclass{article}     % Стандартный статьи
\documentclass{report}      % Отчеты и дипломы
\documentclass{book}        % Книги
\documentclass{beamer}      % Презентации
```

#### Разделы

```latex
\section{Название раздела}
\subsection{Название подраздела}
\subsubsection{Название подподраздела}
\paragraph{Параграф}
\subparagraph{Подпараграф}
```

#### Форматирование текста

```latex
\textbf{Жирный текст}
\textit{Курсив}
\underline{Подчеркнутый текст}
\texttt{Моноширинный текст}
\textsc{Капитель}
\emph{Выделенный текст}

{\Large Больший шрифт}
{\small Меньший шрифт}
```

#### Списки

```latex
% Нумерованный список
\begin{enumerate}
    \item Первый элемент
    \item Второй элемент
    \begin{enumerate}
        \item Вложенный элемент
    \end{enumerate}
\end{enumerate}

% Маркированный список
\begin{itemize}
    \item Элемент списка
    \item Еще один элемент
\end{itemize}

% Описание
\begin{description}
    \item[Термин] Определение термина
    \item[LaTeX] Система компьютерной верстки
\end{description}
```

## Математика в LaTeX

### Режимы математики

#### Встроенные формулы

```latex
Формула в тексте: $E = mc^2$ или \(E = mc^2\)
```

#### Отдельные формулы

Отдельная формула:
$$E = mc^2$$
или
\[E = mc^2\]
```

#### Нумерованные формулы

```latex
\begin{equation}
E = mc^2
\end{equation}
```

### Основные математические символы

```latex
% Греческие буквы
\alpha, \beta, \gamma, \delta, \epsilon
\Gamma, \Delta, \Theta, \Lambda, \Omega

% Операторы
\int \infty \sum \prod \lim
\sin \cos \tan \log \ln \exp

% Отношения
= \neq \approx \equiv \sim
< \leq \ll > \geq \gg
\in \notin \subset \subseteq \cup \cap

% Стрелки
\rightarrow \leftarrow \Rightarrow \Leftarrow
\leftrightarrow \Leftrightarrow \mapsto \to
```

### Дроби и корни

```latex
\frac{a}{b}           % Простая дробь
\dfrac{a}{b}          % Отображаемая дробь
\sqrt{x}              % Квадратный корень
\sqrt[n]{x}           % Корень n-й степени
```

### Индексы и степени

```latex
x^2                   % Степень
x_1                   % Нижний индекс
x^{2y}                % Сложная степень
x_{i+1}               % Сложный индекс
{}_{a}^{b}X_{c}^{d}   % Комбинированные индексы
```

### Матрицы

```latex
\begin{matrix}
a & b \\
c & d
\end{matrix}

\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}

\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
```

### Системы уравнений

```latex
\begin{cases}
x + y = 5 \\
2x - y = 1
\end{cases}

\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}
```

## Работа с изображениями

```latex
\usepackage{graphicx}

% Базовое включение изображения
\includegraphics{image.png}

% С масштабированием
\includegraphics[width=0.5\textwidth]{image.png}
\includegraphics[height=3cm]{image.png}

% В окружении figure
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{image.png}
    \caption{Подпись к изображению}
    \label{fig:my_label}
\end{figure}

% Ссылка на рисунок
Как показано на рисунке \ref{fig:my_label}...
```

## Таблицы

```latex
% Простая таблица
\begin{tabular}{|l|c|r|}
\hline
Лево & Центр & Право \\
\hline
Текст & 123 & 45.67 \\
Другая строка & 890 & 12.34 \\
\hline
\end{tabular}

% Таблица с подписью
\begin{table}[htbp]
    \centering
    \begin{tabular}{|c|c|c|}
    \hline
    A & B & C \\
    \hline
    1 & 2 & 3 \\
    4 & 5 & 6 \\
    \hline
    \end{tabular}
    \caption{Пример таблицы}
    \label{tab:example}
\end{table}
```

## Библиография

### Простой способ (thebibliography)

```latex
\begin{thebibliography}{9}
    \bibitem{knuth1984}
    Donald E. Knuth.
    \newblock \emph{The TeXbook}.
    \newblock Addison-Wesley, 1984.
    
    \bibitem{lamport1994}
    Leslie Lamport.
    \newblock \emph{LaTeX: A Document Preparation System}.
    \newblock Addison-Wesley, 1994.
\end{thebibliography}

% Цитирование
Согласно \cite{knuth1984}, LaTeX был создан...
```

### С помощью BibTeX

1. Создайте файл `references.bib`:

```bibtex
@book{knuth1984,
    author = {Knuth, Donald E.},
    title = {The TeXbook},
    publisher = {Addison-Wesley},
    year = {1984}
}

@book{lamport1994,
    author = {Lamport, Leslie},
    title = {LaTeX: A Document Preparation System},
    publisher = {Addison-Wesley},
    year = {1994}
}
```

2. В основном файле:

```latex
\bibliographystyle{plain}
\bibliography{references}

% Цитирование
Согласно \cite{knuth1984}, LaTeX был создан...
```

## Полезные пакеты

```latex
% Основные пакеты
\usepackage[utf8]{inputenc}        % Поддержка UTF-8
\usepackage[russian]{babel}        % Русский язык
\usepackage{amsmath}               % Расширенная математика
\usepackage{amsfonts}              % Математические шрифты
\usepackage{amssymb}               % Математические символы
\usepackage{graphicx}              % Работа с изображениями
\usepackage{hyperref}              % Гиперссылки
\usepackage{geometry}              % Настройка полей
\usepackage{fancyhdr}              % Колонтитулы
\usepackage{color}                 % Цвета
\usepackage{listings}              % Оформление кода
\usepackage{tikz}                  % Создание графиков
\usepackage{float}                 % Управление плавающими объектами
\usepackage{caption}               % Подписи к рисункам и таблицам
```

## Распространенные ошибки и их решение

### Ошибка: "File 'xxx.sty' not found"

**Решение:** Установите недостающий пакет
```bash
# Для MiKTeX
mpm --install=package-name

# Для TeX Live
tlmgr install package-name
```

### Ошибка: "Undefined control sequence"

**Причины:**
- Опечатка в команде
- Не подключен нужный пакет
- Использование команды без соответствующего окружения

### Ошибка: "Missing $ inserted"

**Решение:** Математические символы должны быть в математическом режиме
```latex
% Неправильно:
В формуле alpha используется...

% Правильно:
В формуле $\alpha$ используется...
```

### Ошибка: "Extra alignment tab has been changed to \cr"

**Решение:** Слишком много столбцов в таблице. Проверьте количество & в строке.

### Проблемы с кириллицей
```latex
% Убедитесь, что используете:
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage[T2A]{fontenc}
```

## Производительность и оптимизация

### Компиляция больших документов

```bash
# Использование pdflatex с несколькими проходами
pdflatex document.tex
pdflatex document.tex  # Второй проход для ссылок

# Использование latexmk (автоматическое определение числа проходов)
latexmk -pdf document.tex
```

### Ускорение компиляции

- Используйте \includeonly для компиляции только нужных частей
- Разбивайте большие документы на главы с помощью \include
- Используйте предкомпиляцию преамбулы

## Полезные ресурсы

### Официальная документация

- Официальный сайт: https://www.latex-project.org/
- Курс LaTeX: https://www.overleaf.com/learn
- Книга "The LaTeX Companion": https://www.informit.com/store/latex-companion-9780201362992

### Онлайн-редакторы

- Overleaf: https://www.overleaf.com/
- ShareLaTeX: https://ru.sharelatex.com/
- Papeeria: https://papeeria.com/

### Сообщества и помощь

- StackExchange: https://tex.stackexchange.com/
- Русскоязычный форум: https://latex.org/forum/
- GitHub с шаблонами: https://github.com/topics/latex-template

### Шаблоны

- Шаблоны Overleaf: https://www.overleaf.com/gallery
- Шаблоны университетов: https://www.latextemplates.com/
- CTAN (Comprehensive TeX Archive Network): https://www.ctan.org/

## Заключение

`LaTeX` - мощная система для создания профессиональных документов. Хотя начальное освоение может потребовать времени, результат стоит усилий.

**Главное** - начать с простых документов и постепенно осваивать новые возможности.

**Практические советы для начинающих:**

1. Используйте готовые шаблоны
2. Начинайте с простых документов
3. Постепенно добавляйте новые пакеты
4. Используйте онлайн-редакторы для начала
5. Не бойтесь экспериментировать

Prism - AI LaTeX Editor
https://prism.openai.com/