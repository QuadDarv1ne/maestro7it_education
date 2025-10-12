#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <string>
#include <vector>

using namespace std;

class Calculator {
public:
    static double evaluate(const std::vector<std::string>& tokens);
private:
    static std::vector<std::string> infixToPRN(const std::vector<std::string>& tokens);
    static double evaluateRPN(const std::vector<std::string>& rpn);
    static bool isNumber(const std::string& token);
    static bool isOperator(const std::string& token);
    static bool isFunction(const std::string& token);
    static bool isConstant(const std::string& token);
    static double getConstantValue(const std::string& token);
    static int getPrecedence(const std::string& op);
    static int getArity(const std::string& token); // 1 (для функций/унарных), 2 (для бинарных)
};

#endif