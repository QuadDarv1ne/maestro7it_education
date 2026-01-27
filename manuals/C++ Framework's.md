# 🚀 C++ Frameworks: Полное руководство по популярным библиотекам и фреймворкам

## 📋 Содержание

1. [Введение в C++ фреймворки](#введение-в-c-фреймворки)
2. [Основные категории фреймворков](#основные-категории-фреймворков)
3. [GUI фреймворки](#gui-фреймворки)
4. [Web фреймворки](#web-фреймворки)
5. [Игровые движки](#игровые-движки)
6. [Компьютерное зрение и медиа](#компьютерное-зрение-и-медиа)
7. [Утилитарные библиотеки](#утилитарные-библиотеки)
8. [Выбор подходящего фреймворка](#выбор-подходящего-фреймворка)
9. [Практические примеры](#практические-примеры)

## Введение в C++ фреймворки

**C++ фреймворк** — это набор библиотек, инструментов и соглашений, которые упрощают разработку приложений на C++.

Они предоставляют готовые решения для типичных задач и позволяют сосредоточиться на бизнес-логике, а не на низкоуровневой реализации.

### Преимущества использования фреймворков:
- **Ускорение разработки**: Готовые компоненты
- **Стандартизация**: Единый стиль кода
- **Надежность**: Протестированные решения
- **Поддержка сообщества**: Документация и помощь
- **Кроссплатформенность**: Работа на разных ОС

### Критерии выбора:
- Тип проекта (десктоп, веб, мобильный)
- Требования к производительности
- Сложность разработки
- Лицензирование
- Размер сообщества

---

## Основные категории фреймворков

### 1. GUI (Graphical User Interface)
Для создания десктопных приложений с графическим интерфейсом

### 2. Web Frameworks
Для разработки веб-приложений и серверов

### 3. Game Engines
Для создания игр и интерактивных приложений

### 4. Computer Vision & Media
Для работы с изображениями, видео и аудио

### 5. Utility Libraries
Общие утилиты и расширения стандартной библиотеки

---

## GUI фреймворки

### 1. Qt Framework

**Описание**: Самый популярный кроссплатформенный фреймворк для создания GUI-приложений.

**Особенности**:
- Кроссплатформенность (Windows, Linux, macOS, Android, iOS)
- Богатый набор виджетов
- Встроенный сигналы/слоты механизм
- Qt Creator IDE
- Поддержка QML для современного UI

**Установка**:
```bash
# Ubuntu/Debian
sudo apt install qt5-default qtcreator

# Windows (через онлайн установщик)
# Скачать с официального сайта: https://www.qt.io/download
```

**Пример приложения**:
```cpp
#include <QApplication>
#include <QWidget>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

class MainWindow : public QWidget {
public:
    MainWindow(QWidget *parent = nullptr) : QWidget(parent) {
        // Создание элементов интерфейса
        QLabel *label = new QLabel("Привет, Qt!");
        QPushButton *button = new QPushButton("Нажми меня");
        
        // Компоновка
        QVBoxLayout *layout = new QVBoxLayout;
        layout->addWidget(label);
        layout->addWidget(button);
        setLayout(layout);
        
        // Подключение сигнала к слоту
        connect(button, &QPushButton::clicked, this, &MainWindow::onButtonClicked);
    }
    
private slots:
    void onButtonClicked() {
        // Обработка нажатия кнопки
        qDebug() << "Кнопка нажата!";
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    MainWindow window;
    window.show();
    
    return app.exec();
}
```

**CMakeLists.txt для Qt**:
```cmake
cmake_minimum_required(VERSION 3.16)
project(QtApp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Core Widgets REQUIRED)

add_executable(QtApp main.cpp)
target_link_libraries(QtApp Qt5::Core Qt5::Widgets)
```

**Преимущества Qt**:
- Мощная экосистема
- Отличная документация
- Большое сообщество
- Коммерческая и open-source лицензии

**Недостатки**:
- Большой размер фреймворка
- Высокое потребление памяти
- Сложность для новичков

### 2. wxWidgets

**Описание**: Альтернатива Qt с акцентом на нативный внешний вид.

**Особенности**:
- Использует нативные элементы управления ОС
- Меньше зависимостей, чем Qt
- Бесплатная лицензия (wxWindows Library Licence)

**Пример**:
```cpp
#include <wx/wx.h>

class MyApp : public wxApp {
public:
    virtual bool OnInit();
};

class MyFrame : public wxFrame {
public:
    MyFrame();
private:
    void OnHello(wxCommandEvent& event);
    void OnExit(wxCommandEvent& event);
    void OnAbout(wxCommandEvent& event);
};

wxIMPLEMENT_APP(MyApp);

bool MyApp::OnInit() {
    MyFrame *frame = new MyFrame();
    frame->Show(true);
    return true;
}

MyFrame::MyFrame()
    : wxFrame(nullptr, wxID_ANY, "Пример wxWidgets") {
    
    wxMenu *menuFile = new wxMenu;
    menuFile->Append(ID_Hello, "&Hello...\tCtrl-H",
                     "Помощь строка для Hello menu item");
    menuFile->AppendSeparator();
    menuFile->Append(wxID_EXIT);
    
    wxMenu *menuHelp = new wxMenu;
    menuHelp->Append(wxID_ABOUT);
    
    wxMenuBar *menuBar = new wxMenuBar;
    menuBar->Append(menuFile, "&File");
    menuBar->Append(menuHelp, "&Help");
    
    SetMenuBar(menuBar);
    
    CreateStatusBar();
    SetStatusText("Добро пожаловать в wxWidgets!");
    
    Bind(wxEVT_MENU, &MyFrame::OnHello, this, ID_Hello);
    Bind(wxEVT_MENU, &MyFrame::OnExit, this, wxID_EXIT);
    Bind(wxEVT_MENU, &MyFrame::OnAbout, this, wxID_ABOUT);
}

void MyFrame::OnExit(wxCommandEvent& event) {
    Close(true);
}

void MyFrame::OnAbout(wxCommandEvent& event) {
    wxMessageBox("Это wxWidgets Hello World пример",
                 "О программе", wxOK | wxICON_INFORMATION);
}

void MyFrame::OnHello(wxCommandEvent& event) {
    wxLogMessage("Hello world from wxWidgets!");
}
```

**Преимущества wxWidgets**:
- Нативный внешний вид
- Меньше ресурсов
- Бесплатная лицензия

**Недостатки**:
- Меньше функциональности, чем Qt
- Меньше документации
- Меньшее сообщество

### 3. FLTK (Fast Light Toolkit)

**Описание**: Легковесный фреймворк для простых GUI-приложений.

**Особенности**:
- Очень маленький размер (~1MB)
- Быстрая работа
- Простота использования

**Пример**:
```cpp
#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Box.H>

int main() {
    Fl_Window *window = new Fl_Window(340, 180);
    Fl_Box *box = new Fl_Box(20, 40, 300, 100, "Привет, FLTK!");
    box->box(FL_UP_BOX);
    box->labelfont(FL_BOLD + FL_ITALIC);
    box->labelsize(36);
    box->labeltype(FL_SHADOW_LABEL);
    
    window->end();
    window->show();
    
    return Fl::run();
}
```

---

## Web фреймворки

### 1. Wt (Web Toolkit)

**Описание**: C++ библиотека для создания веб-приложений с использованием виджетов.

**Особенности**:
- Создание веб-интерфейсов как десктопных приложений
- Автоматическая генерация HTML/CSS/JavaScript
- Поддержка AJAX
- Сессионная модель

**Установка**:
```bash
# Ubuntu
sudo apt install libwt-dev libwthttp-dev

# Сборка из исходников
git clone https://github.com/emweb/wt.git
cd wt
mkdir build && cd build
cmake ..
make -j4
sudo make install
```

**Пример простого приложения**:
```cpp
#include <Wt/WApplication.h>
#include <Wt/WContainerWidget.h>
#include <Wt/WPushButton.h>
#include <Wt/WText.h>

class HelloApplication : public Wt::WApplication {
public:
    HelloApplication(const Wt::WEnvironment& env) : Wt::WApplication(env) {
        setTitle("Пример Wt");
        
        root()->addStyleClass("container");
        
        Wt::WText *title = root()->addNew<Wt::WText>("<h1>Привет, мир!</h1>");
        title->setInline(false);
        
        Wt::WPushButton *button = root()->addNew<Wt::WPushButton>("Нажми меня!");
        button->setMargin(10, Wt::Side::Top);
        
        Wt::WText *out = root()->addNew<Wt::WText>("");
        out->setInline(false);
        
        button->clicked().connect([=] {
            out->setText("Кнопка была нажата!");
        });
    }
};

int main(int argc, char **argv) {
    return Wt::WRun(argc, argv, [](const Wt::WEnvironment& env) {
        return std::make_unique<HelloApplication>(env);
    });
}
```

**CMakeLists.txt**:
```cmake
cmake_minimum_required(VERSION 3.10)
project(WtApp)

find_package(Wt REQUIRED)

add_executable(webapp main.cpp)
target_link_libraries(webapp ${WT_LIBRARIES})
```

### 2. CppCMS

**Описание**: Высокопроизводительный веб-фреймворк для C++.

**Особенности**:
- MVC архитектура
- Шаблонизатор
- Поддержка сессий
- Безопасность

**Пример**:
```cpp
#include <cppcms/application.h>
#include <cppcms/applications_pool.h>
#include <cppcms/service.h>
#include <cppcms/http_response.h>
#include <iostream>

class hello : public cppcms::application {
public:
    hello(cppcms::service &srv) : cppcms::application(srv) {}
    
    virtual void main(std::string url) {
        response().out() <<
            "<html>\n"
            "<body>\n"
            "  <h1>Привет, мир!</h1>\n"
            "</body>\n"
            "</html>\n";
    }
};

int main(int argc, char ** argv) {
    try {
        cppcms::service srv(argc, argv);
        srv.applications_pool().mount(
            cppcms::applications_factory<hello>()
        );
        srv.run();
    }
    catch(std::exception const &e) {
        std::cerr << e.what() << std::endl;
    }
    return 0;
}
```

---

## Игровые движки

### 1. Unreal Engine

**Описание**: Профессиональный игровой движок с мощными возможностями.

**Особенности**:
- Высококачественная графика
- Blueprints (визуальное программирование)
- C++ API
- Физический движок
- Поддержка VR/AR

**Пример Actor класса**:
```cpp
// MyActor.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"

UCLASS()
class MYGAME_API AMyActor : public AActor {
    GENERATED_BODY()
    
public:    
    AMyActor();

protected:
    virtual void BeginPlay() override;

public:    
    virtual void Tick(float DeltaTime) override;

private:
    UPROPERTY(VisibleAnywhere)
    class UStaticMeshComponent* MeshComponent;
    
    UPROPERTY(EditAnywhere)
    float RotationSpeed;
};

// MyActor.cpp
#include "MyActor.h"
#include "Components/StaticMeshComponent.h"

AMyActor::AMyActor() {
    PrimaryActorTick.bCanEverTick = true;
    
    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComponent;
    
    RotationSpeed = 45.0f;
}

void AMyActor::BeginPlay() {
    Super::BeginPlay();
}

void AMyActor::Tick(float DeltaTime) {
    Super::Tick(DeltaTime);
    
    FRotator NewRotation = GetActorRotation();
    NewRotation.Yaw += RotationSpeed * DeltaTime;
    SetActorRotation(NewRotation);
}
```

**Преимущества Unreal Engine**:
- Профессиональный уровень качества
- Большая экосистема
- Отличная документация
- Активное сообщество

**Недостатки**:
- Высокие требования к железу
- Сложность для новичков
- Размер проектов

### 2. SFML (Simple and Fast Multimedia Library)

**Описание**: Легковесная библиотека для создания 2D игр и мультимедийных приложений.

**Особенности**:
- Простота использования
- Кроссплатформенность
- Поддержка аудио, графики, ввода
- Современный C++

**Установка**:
```bash
# Ubuntu
sudo apt install libsfml-dev

# Windows (через vcpkg)
vcpkg install sfml
```

**Пример игры**:
```cpp
#include <SFML/Graphics.hpp>
#include <iostream>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Works!");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);
    
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        
        window.clear();
        window.draw(shape);
        window.display();
    }
    
    return 0;
}
```

**CMakeLists.txt для SFML**:
```cmake
cmake_minimum_required(VERSION 3.10)
project(SFMLApp)

set(CMAKE_CXX_STANDARD 17)

find_package(SFML 2.5 COMPONENTS graphics audio REQUIRED)

add_executable(game main.cpp)
target_link_libraries(game sfml-graphics sfml-audio)
```

---

## Компьютерное зрение и медиа

### 1. OpenCV

**Описание**: Самая популярная библиотека для компьютерного зрения.

**Особенности**:
- Обработка изображений
- Распознавание объектов
- Машинное обучение
- AR/VR приложения

**Установка**:
```bash
# Ubuntu
sudo apt install libopencv-dev

# Windows (через vcpkg)
vcpkg install opencv4
```

**Пример обработки изображения**:
```cpp
#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Загрузка изображения
    cv::Mat image = cv::imread("image.jpg");
    if (image.empty()) {
        std::cout << "Не удалось загрузить изображение!" << std::endl;
        return -1;
    }
    
    // Преобразование в оттенки серого
    cv::Mat gray_image;
    cv::cvtColor(image, gray_image, cv::COLOR_BGR2GRAY);
    
    // Применение гауссовского размытия
    cv::Mat blurred_image;
    cv::GaussianBlur(gray_image, blurred_image, cv::Size(15, 15), 0);
    
    // Обнаружение краев (Canny)
    cv::Mat edges;
    cv::Canny(blurred_image, edges, 50, 150);
    
    // Отображение результатов
    cv::imshow("Оригинал", image);
    cv::imshow("Оттенки серого", gray_image);
    cv::imshow("Размытое", blurred_image);
    cv::imshow("Края", edges);
    
    cv::waitKey(0);
    return 0;
}
```

**CMakeLists.txt для OpenCV**:
```cmake
cmake_minimum_required(VERSION 3.10)
project(OpenCVApp)

find_package(OpenCV REQUIRED)

add_executable(opencv_app main.cpp)
target_link_libraries(opencv_app ${OpenCV_LIBS})
```

### 2. FFmpeg

**Описание**: Мощная библиотека для работы с аудио/видео.

**Особенности**:
- Декодирование/кодирование
- Потоковая передача
- Редактирование медиа
- Поддержка множества форматов

**Пример воспроизведения видео**:
```cpp
extern "C" {
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libswscale/swscale.h>
}

#include <iostream>

int main() {
    const char* filename = "video.mp4";
    
    AVFormatContext* format_context = nullptr;
    if (avformat_open_input(&format_context, filename, nullptr, nullptr) != 0) {
        std::cerr << "Не удалось открыть файл" << std::endl;
        return -1;
    }
    
    if (avformat_find_stream_info(format_context, nullptr) < 0) {
        std::cerr << "Не удалось найти информацию о потоке" << std::endl;
        return -1;
    }
    
    av_dump_format(format_context, 0, filename, 0);
    
    avformat_close_input(&format_context);
    return 0;
}
```

---

## Утилитарные библиотеки

### 1. Boost

**Описание**: Коллекция высококачественных библиотек C++.

**Основные компоненты**:
- **Boost.Asio**: Асинхронный ввод/вывод
- **Boost.Filesystem**: Работа с файловой системой
- **Boost.Thread**: Многопоточность
- **Boost.Smart_ptr**: Умные указатели
- **Boost.Regex**: Регулярные выражения

**Установка**:
```bash
# Ubuntu
sudo apt install libboost-all-dev

# Windows (через vcpkg)
vcpkg install boost
```

**Пример использования Boost.Asio**:
```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_context io_context;
        
        tcp::resolver resolver(io_context);
        tcp::resolver::results_type endpoints =
            resolver.resolve("www.example.com", "http");
        
        tcp::socket socket(io_context);
        boost::asio::connect(socket, endpoints);
        
        boost::asio::write(socket, boost::asio::buffer("GET / HTTP/1.1\r\nHost: www.example.com\r\n\r\n"));
        
        boost::asio::streambuf response;
        boost::asio::read_until(socket, response, "\r\n");
        
        std::istream response_stream(&response);
        std::string http_version;
        response_stream >> http_version;
        unsigned int status_code;
        response_stream >> status_code;
        std::string status_message;
        std::getline(response_stream, status_message);
        
        if (!response_stream || http_version.substr(0, 5) != "HTTP/") {
            std::cout << "Неверный ответ\n";
        } else {
            std::cout << "Статус: " << status_code << "\n";
        }
    }
    catch (std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
    
    return 0;
}
```

### 2. POCO C++ Libraries

**Описание**: Модерная коллекция C++ библиотек для сетевых и интернет-приложений.

**Компоненты**:
- Foundation (базовые классы)
- Net (сетевые протоколы)
- Util (утилиты)
- XML (работа с XML)
- JSON (работа с JSON)

**Установка**:
```bash
# Ubuntu
sudo apt install libpoco-dev

# Сборка из исходников
git clone https://github.com/pocoproject/poco.git
cd poco
./configure
make -j4
sudo make install
```

**Пример HTTP-клиента**:
```cpp
#include "Poco/Net/HTTPClientSession.h"
#include "Poco/Net/HTTPRequest.h"
#include "Poco/Net/HTTPResponse.h"
#include "Poco/StreamCopier.h"
#include <iostream>

using namespace Poco::Net;
using namespace Poco;

int main() {
    try {
        URI uri("http://www.example.com/");
        HTTPClientSession session(uri.getHost(), uri.getPort());
        
        HTTPRequest request(HTTPRequest::HTTP_GET, uri.getPath(), HTTPMessage::HTTP_1_1);
        session.sendRequest(request);
        
        HTTPResponse response;
        std::istream& rs = session.receiveResponse(response);
        
        std::cout << response.getStatus() << " " << response.getReason() << std::endl;
        
        StreamCopier::copyStream(rs, std::cout);
    }
    catch (Exception& ex) {
        std::cerr << ex.displayText() << std::endl;
        return 1;
    }
    return 0;
}
```

### 3. JUCE

**Описание**: Фреймворк для разработки аудио-приложений и плагинов.

**Особенности**:
- Кроссплатформенность
- Аудио I/O
- MIDI поддержка
- GUI фреймворк
- Поддержка VST/AU/AAX плагинов

**Пример аудио-приложения**:
```cpp
#include "../JuceLibraryCode/JuceHeader.h"

class MainContentComponent : public AudioAppComponent {
public:
    MainContentComponent() {
        setSize(800, 600);
        setAudioChannels(2, 2);
    }
    
    ~MainContentComponent() override {
        shutdownAudio();
    }
    
    void prepareToPlay(int samplesPerBlockExpected, double sampleRate) override {
        // Подготовка к воспроизведению
    }
    
    void getNextAudioBlock(const AudioSourceChannelInfo& bufferToFill) override {
        // Генерация аудио
        for (int channel = 0; channel < bufferToFill.buffer->getNumChannels(); ++channel) {
            float* const buffer = bufferToFill.buffer->getWritePointer(channel, bufferToFill.startSample);
            
            for (int sample = 0; sample < bufferToFill.numSamples; ++sample) {
                buffer[sample] = std::sin(currentAngle);
                currentAngle += angleDelta;
            }
        }
    }
    
    void releaseResources() override {
        // Освобождение ресурсов
    }
    
    void paint(Graphics& g) override {
        g.fillAll(getLookAndFeel().findColour(ResizableWindow::backgroundColourId));
        g.setColour(Colours::white);
        g.setFont(15.0f);
        g.drawFittedText("Пример JUCE приложения", getLocalBounds(), Justification::centred, 1);
    }
    
    void resized() override {
        // Изменение размера компонентов
    }

private:
    double currentAngle = 0.0;
    double angleDelta = 0.0;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainContentComponent)
};

// Это создает новый Application и запускает его
class MyApp : public JUCEApplication {
public:
    MyApp() {}
    
    const String getApplicationName() override { return "JUCE App"; }
    const String getApplicationVersion() override { return "1.0.0"; }
    bool moreThanOneInstanceAllowed() override { return true; }
    
    void initialise(const String& commandLine) override {
        mainWindow.reset(new MainWindow(getApplicationName()));
    }
    
    void shutdown() override {
        mainWindow = nullptr;
    }
    
    void systemRequestedQuit() override {
        quit();
    }
    
    void anotherInstanceStarted(const String& commandLine) override {}

private:
    class MainWindow : public DocumentWindow {
    public:
        MainWindow(String name) : DocumentWindow(name,
                                                Desktop::getInstance().getDefaultLookAndFeel()
                                                                      .findColour(ResizableWindow::backgroundColourId),
                                                DocumentWindow::allButtons) {
            setUsingNativeTitleBar(true);
            setContentOwned(new MainContentComponent(), true);
            
            setResizable(true, true);
            centreWithSize(getWidth(), getHeight());
            setVisible(true);
        }
        
        void closeButtonPressed() override {
            JUCEApplication::getInstance()->systemRequestedQuit();
        }
        
    private:
        JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainWindow)
    };
    
    std::unique_ptr<MainWindow> mainWindow;
};

START_JUCE_APPLICATION(MyApp)
```

---

## Выбор подходящего фреймворка

### Таблица сравнения фреймворков

| Фреймворк | Тип | Сложность | Производительность | Сообщество | Лицензия |
|-----------|-----|-----------|-------------------|------------|----------|
| Qt | GUI | Средняя | Высокая | Большое | LGPL/GPL |
| wxWidgets | GUI | Средняя | Высокая | Среднее | wxWindows |
| FLTK | GUI | Низкая | Очень высокая | Маленькое | LGPL |
| Wt | Web | Средняя | Средняя | Среднее | GPL |
| Unreal Engine | Game | Высокая | Очень высокая | Большое | MIT/Epic |
| SFML | Game/Media | Низкая | Высокая | Среднее | zlib |
| OpenCV | CV/Media | Средняя | Очень высокая | Большое | Apache 2.0 |
| Boost | Utility | Высокая | Очень высокая | Большое | Boost |

### Рекомендации по выбору:

1. **Для десктопных приложений**:
   - Qt (сложные, профессиональные)
   - wxWidgets (простые, нативный вид)
   - FLTK (очень простые, минимальные)

2. **Для веб-приложений**:
   - Wt (C++ виджеты)
   - CppCMS (MVC подход)

3. **Для игр**:
   - Unreal Engine (AAA игры)
   - SFML (2D игры, прототипирование)

4. **Для компьютерного зрения**:
   - OpenCV (стандарт де-факто)

5. **Для аудио-приложений**:
   - JUCE (профессиональный уровень)

6. **Для утилит и библиотек**:
   - Boost (универсальный)
   - POCO (сетевые приложения)

---

## Практические примеры

### 1. Простой чат-сервер (Boost.Asio)

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <vector>
#include <memory>

using boost::asio::ip::tcp;

class ChatSession : public std::enable_shared_from_this<ChatSession> {
public:
    ChatSession(tcp::socket socket) : socket_(std::move(socket)) {}
    
    void start() {
        do_read();
    }
    
private:
    void do_read() {
        auto self(shared_from_this());
        socket_.async_read_some(boost::asio::buffer(data_, max_length),
            [this, self](boost::system::error_code ec, std::size_t length) {
                if (!ec) {
                    std::cout << "Получено: " << std::string(data_, length) << std::endl;
                    do_write(length);
                }
            });
    }
    
    void do_write(std::size_t length) {
        auto self(shared_from_this());
        boost::asio::async_write(socket_, boost::asio::buffer(data_, length),
            [this, self](boost::system::error_code ec, std::size_t /*length*/) {
                if (!ec) {
                    do_read();
                }
            });
    }
    
    tcp::socket socket_;
    enum { max_length = 1024 };
    char data_[max_length];
};

class ChatServer {
public:
    ChatServer(boost::asio::io_context& io_context, short port)
        : acceptor_(io_context, tcp::endpoint(tcp::v4(), port)) {
        do_accept();
    }
    
private:
    void do_accept() {
        acceptor_.async_accept(
            [this](boost::system::error_code ec, tcp::socket socket) {
                if (!ec) {
                    std::make_shared<ChatSession>(std::move(socket))->start();
                }
                do_accept();
            });
    }
    
    tcp::acceptor acceptor_;
};

int main() {
    try {
        boost::asio::io_context io_context;
        ChatServer server(io_context, 8080);
        std::cout << "Сервер запущен на порту 8080" << std::endl;
        io_context.run();
    }
    catch (std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
    }
    
    return 0;
}
```

### 2. Обработчик изображений (OpenCV + Qt)

```cpp
// ImageProcessor.h
#pragma once

#include <QObject>
#include <opencv2/opencv.hpp>

class ImageProcessor : public QObject {
    Q_OBJECT
    
public:
    explicit ImageProcessor(QObject *parent = nullptr);
    
    bool loadImage(const QString& filename);
    void processImage();
    void saveImage(const QString& filename);
    
signals:
    void imageProcessed(const QImage& image);
    
private:
    cv::Mat currentImage;
};

// ImageProcessor.cpp
#include "ImageProcessor.h"
#include <QImage>
#include <QDebug>

ImageProcessor::ImageProcessor(QObject *parent) : QObject(parent) {}

bool ImageProcessor::loadImage(const QString& filename) {
    currentImage = cv::imread(filename.toStdString());
    return !currentImage.empty();
}

void ImageProcessor::processImage() {
    if (currentImage.empty()) return;
    
    cv::Mat processed;
    cv::cvtColor(currentImage, processed, cv::COLOR_BGR2GRAY);
    cv::GaussianBlur(processed, processed, cv::Size(15, 15), 0);
    cv::Canny(processed, processed, 50, 150);
    
    // Конвертация в QImage
    cv::Mat rgb;
    cv::cvtColor(processed, rgb, cv::COLOR_GRAY2RGB);
    
    QImage qImage(rgb.data, rgb.cols, rgb.rows, 
                  static_cast<int>(rgb.step), QImage::Format_RGB888);
    
    emit imageProcessed(qImage.rgbSwapped());
}

void ImageProcessor::saveImage(const QString& filename) {
    if (!currentImage.empty()) {
        cv::imwrite(filename.toStdString(), currentImage);
    }
}
```

### 3. REST API сервер (POCO)

```cpp
#include "Poco/Net/HTTPServer.h"
#include "Poco/Net/HTTPRequestHandler.h"
#include "Poco/Net/HTTPRequestHandlerFactory.h"
#include "Poco/Net/HTTPServerParams.h"
#include "Poco/Net/HTTPServerRequest.h"
#include "Poco/Net/HTTPServerResponse.h"
#include "Poco/Net/ServerSocket.h"
#include "Poco/Util/ServerApplication.h"
#include "Poco/JSON/Object.h"

using namespace Poco::Net;
using namespace Poco::Util;
using namespace Poco::JSON;

class RequestHandler : public HTTPRequestHandler {
public:
    void handleRequest(HTTPServerRequest& request, HTTPServerResponse& response) override {
        response.setChunkedTransferEncoding(true);
        response.setContentType("application/json");
        
        Object json;
        json.set("message", "Привет от POCO сервера!");
        json.set("timestamp", Poco::Timestamp().epochMicroseconds());
        
        std::ostream& ostr = response.send();
        json.stringify(ostr);
    }
};

class RequestHandlerFactory : public HTTPRequestHandlerFactory {
public:
    HTTPRequestHandler* createRequestHandler(const HTTPServerRequest& request) override {
        return new RequestHandler;
    }
};

class RESTServer : public ServerApplication {
protected:
    int main(const std::vector<std::string>& args) override {
        HTTPServerParams* params = new HTTPServerParams;
        params->setMaxThreads(16);
        
        ServerSocket socket(8080);
        HTTPServer server(new RequestHandlerFactory, socket, params);
        
        server.start();
        waitForTerminationRequest();
        server.stop();
        
        return Application::EXIT_OK;
    }
};

int main(int argc, char** argv) {
    RESTServer app;
    return app.run(argc, argv);
}
```

---

## Заключение

`C++` предлагает богатый выбор фреймворков для различных задач разработки. Выбор правильного фреймворка зависит от требований проекта, уровня сложности и целевой платформы.

### Ключевые рекомендации:
1. **Изучите документацию** выбранного фреймворка
2. **Начинайте с простых примеров**
3. **Используйте менеджеры пакетов** (vcpkg, Conan)
4. **Следите за лицензированием**
5. **Участвуйте в сообществах** разработчиков

### Полезные ресурсы:
- [Awesome C++](https://github.com/fffaraz/awesome-cpp) - Кураторский список библиотек
- [CppReference](https://en.cppreference.com/) - Справочник по `C++`
- [vcpkg](https://github.com/microsoft/vcpkg) - Менеджер пакетов для `C++`

Это руководство охватывает основные фреймворки и библиотеки `C++`

Для углубленного изучения каждого инструмента рекомендуется обращаться к официальной документации и примерам кода.

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/обучение-технологиям-и-языкам-программирования)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.