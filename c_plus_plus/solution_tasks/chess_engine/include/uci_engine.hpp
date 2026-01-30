#ifndef UCI_ENGINE_HPP
#define UCI_ENGINE_HPP

#include <string>
#include <vector>
#include <map>
#include <thread>
#include <atomic>
#include <iostream>

/**
 * @brief UCI (Universal Chess Interface) протокол
 * 
 * Реализует стандартный протокол для взаимодействия с шахматными GUI
 */
class UCIEngine {
private:
    // Состояние двигателя
    std::atomic<bool> running_;
    std::atomic<bool> searching_;
    std::thread search_thread_;
    
    // Параметры поиска
    int search_depth_;
    int search_time_ms_;
    bool infinite_search_;
    
    // Опции двигателя
    std::map<std::string, std::string> options_;
    
    // Callback функции
    std::function<void(const std::string&)> send_command_callback_;
    
    // Внутренние методы
    void processUCICommand(const std::string& command);
    void handleUCINewGame();
    void handlePosition(const std::vector<std::string>& tokens);
    void handleGo(const std::vector<std::string>& tokens);
    void handleStop();
    void handleQuit();
    void sendInfo(const std::string& info);
    void sendBestMove(const std::string& move);
    
    // Вспомогательные функции
    std::vector<std::string> tokenize(const std::string& input);
    std::string trim(const std::string& str);
    
public:
    UCIEngine();
    ~UCIEngine();
    
    // Основной интерфейс
    void start();
    void stop();
    void sendCommand(const std::string& command);
    
    // Настройка callback'ов
    void setSendCallback(std::function<void(const std::string&)> callback);
    
    // Получение информации
    bool isRunning() const { return running_; }
    bool isSearching() const { return searching_; }
    
    // Опции двигателя
    void setOption(const std::string& name, const std::string& value);
    std::string getOption(const std::string& name) const;
    void printOptions() const;
};

// Константы UCI протокола
namespace UCIConstants {
    const std::string VERSION = "1.0";
    const std::string AUTHOR = "Chess Engine Team";
    
    // Стандартные команды
    const std::string CMD_UCI = "uci";
    const std::string CMD_ISREADY = "isready";
    const std::string CMD_UCINEWGAME = "ucinewgame";
    const std::string CMD_POSITION = "position";
    const std::string CMD_GO = "go";
    const std::string CMD_STOP = "stop";
    const std::string CMD_QUIT = "quit";
    const std::string CMD_SET_OPTION = "setoption";
    
    // Ответы двигателя
    const std::string RESP_ID_NAME = "id name Maestro Chess Engine";
    const std::string RESP_ID_AUTHOR = "id author " + AUTHOR;
    const std::string RESP_UCI_OK = "uciok";
    const std::string RESP_READY_OK = "readyok";
    const std::string RESP_BESTMOVE = "bestmove ";
    const std::string RESP_INFO = "info ";
    
    // Опции двигателя
    const std::string OPTION_HASH = "Hash";
    const std::string OPTION_THREADS = "Threads";
    const std::string OPTION_MULTI_PV = "MultiPV";
    const std::string OPTION_OWN_BOOK = "OwnBook";
    
    // Типы опций
    const std::string TYPE_CHECK = "check";
    const std::string TYPE_SPIN = "spin";
    const std::string TYPE_COMBO = "combo";
    const std::string TYPE_BUTTON = "button";
    const std::string TYPE_STRING = "string";
}

#endif // UCI_ENGINE_HPP