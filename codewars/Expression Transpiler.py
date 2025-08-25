'''
https://www.codewars.com/kata/597ccf7613d879c4cb00000f/train/python
'''

import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "val"])

# токены (пробелы обрабатываем вручную)
TOKEN_REGEX = re.compile(
    r"""(?:
        (?P<ARROW>->) |
        (?P<NUMBER>[0-9]+) |
        (?P<IDENT>[A-Za-z_][A-Za-z_0-9]*) |
        (?P<LBRACE>\{) |
        (?P<RBRACE>\}) |
        (?P<LPAREN>\() |
        (?P<RPAREN>\)) |
        (?P<COMMA>,)
    )""",
    re.VERBOSE,
)

def tokenize(src: str):
    """
    Разбивает исходную строку `src` на список токенов.

    Аргументы:
        src (str): строка с исходным выражением.

    Возвращает:
        list[Token] | None: список токенов или None при ошибке токенизации.

    Особенности:
        - Пропускает пробелы и переносы строк.
        - Проверяет, что число не содержит некорректных символов (например "1a").
    """
    pos = 0
    toks = []
    L = len(src)
    match = TOKEN_REGEX.match
    while True:
        # пропускаем пробелы/переносы
        while pos < L and src[pos].isspace():
            pos += 1
        if pos >= L:
            break
        m = match(src, pos)
        if not m:
            return None
        typ = m.lastgroup
        val = m.group(typ)
        endpos = m.end()
        # если NUMBER сразу за ним идёт буква или '_' — это invalid (например "1a")
        if typ == "NUMBER" and endpos < L and (src[endpos].isalpha() or src[endpos] == '_'):
            return None
        toks.append(Token(typ, val))
        pos = endpos
    return toks

# ---------------- Parser ----------------

class ParseError(Exception):
    """Исключение для ошибок парсинга выражений."""
    pass

class Parser:
    """
    Парсер выражений, преобразующий список токенов в абстрактное синтаксическое дерево (AST).

    Поддерживает:
      - числа
      - идентификаторы
      - вызовы функций
      - лямбда-выражения в фигурных скобках
      - вложенные выражения в круглых скобках
    """

    def __init__(self, toks):
        """
        Инициализация парсера.

        Аргументы:
            toks (list[Token]): список токенов, полученных из функции tokenize().
        """
        self.toks = toks
        self.i = 0
        self.n = len(toks)

    def peek(self, t=None):
        """
        Возвращает текущий токен без сдвига курсора.

        Аргументы:
            t (str | None): ожидаемый тип токена (если None — возвращается любой).

        Возвращает:
            Token | None: текущий токен или None, если не совпадает/конец списка.
        """
        if self.i >= self.n:
            return None
        tok = self.toks[self.i]
        return tok if (t is None or tok.type == t) else None

    def eat(self, t=None):
        """
        Считывает и возвращает текущий токен, сдвигая курсор.

        Аргументы:
            t (str | None): ожидаемый тип токена.

        Исключение:
            ParseError — если токен не совпадает с ожидаемым.
        """
        tok = self.peek(t)
        if not tok:
            raise ParseError("unexpected token")
        self.i += 1
        return tok

    def parse(self):
        """
        Главный метод парсинга.

        Возвращает:
            tuple: корневой узел AST.

        Исключение:
            ParseError — если выражение пустое, содержит ошибки или лишние токены.
        """
        if self.n == 0:
            raise ParseError("empty")
        node = self.expr()
        if self.i != self.n:
            raise ParseError("extra input")
        # топ-уровневые пустые скобки считаются ошибкой (по условию kata)
        if node[0] == "empty_paren":
            raise ParseError("empty paren not allowed as top-level")
        return node

    def expr(self):
        """expr := atom { (arglist | lambda) }"""
        node = self.atom()
        while True:
            if self.peek("LPAREN"):
                args = self.arglist()
                node = ("call", node, args)
                continue
            if self.peek("LBRACE"):
                # Разрешаем trailing-lambda ТОЛЬКО после call/ident/number/empty_paren
                # (не разрешаем после чистой lambda — чтобы, например, "{}{}{}" считалось ошибкой)
                if node[0] not in ("call", "ident", "number", "empty_paren"):
                    raise ParseError("invalid brace after non-call/ident")
                lam = self.lambda_expr()
                if node[0] == "call":
                    node = ("call", node[1], node[2] + [lam])
                else:
                    node = ("call", node, [lam])
                continue
            break
        return node

    def atom(self):
        """atom := IDENT | NUMBER | lambda | ( expr ) | ()"""
        if self.peek("IDENT"):
            return ("ident", self.eat().val)
        if self.peek("NUMBER"):
            return ("number", self.eat().val)
        if self.peek("LBRACE"):
            return self.lambda_expr()
        if self.peek("LPAREN"):
            self.eat("LPAREN")
            if self.peek("RPAREN"):
                self.eat("RPAREN")
                return ("empty_paren",)
            node = self.expr()
            self.eat("RPAREN")
            return node
        raise ParseError("atom expected")

    def arglist(self):
        """arglist := '(' [ expr { ',' expr } ] ')'"""
        self.eat("LPAREN")
        args = []
        if not self.peek("RPAREN"):
            while True:
                args.append(self.expr())
                if self.peek("COMMA"):
                    self.eat("COMMA")
                    continue
                break
        self.eat("RPAREN")
        return args

    def lambda_expr(self):
        """
        lambda := '{' ( params '->' body
                       | body
                       | empty )
                  '}'

        NOTE: ARROW without params (i.e. '{->...}') is considered invalid per tests.
        """
        self.eat("LBRACE")
        # пустая лямбда {}
        if self.peek("RBRACE"):
            self.eat("RBRACE")
            return ("lambda", [], [])

        params = []
        body = []

        # если начинается с IDENT/NUMBER — нужно посмотреть, является ли это списком параметров (за ним ARROW)
        if self.peek("IDENT") or self.peek("NUMBER"):
            save = self.i
            tmp = [self.eat().val]
            while self.peek("COMMA"):
                self.eat("COMMA")
                nxt = self.eat()
                if nxt.type not in ("IDENT", "NUMBER"):
                    raise ParseError("bad token in lambda param list")
                tmp.append(nxt.val)
            if self.peek("ARROW"):
                # подтверждён список параметров -> consume arrow и парсим тело
                params = tmp
                self.eat("ARROW")
                while not self.peek("RBRACE"):
                    body.append(self.expr())
            else:
                # rollback: это не параметры, а начало тела
                self.i = save
                while not self.peek("RBRACE"):
                    body.append(self.expr())
        elif self.peek("ARROW"):
            # ARROW без параметров — по тестам должен быть ошибкой
            raise ParseError("arrow without params not allowed")
        else:
            # обычное тело лямбды
            while not self.peek("RBRACE"):
                body.append(self.expr())

        self.eat("RBRACE")
        return ("lambda", params, body)

# ---------------- Emitter ----------------

def emit(node):
    """
    Генерация итогового кода на основе AST.

    Аргументы:
        node (tuple): узел AST.

    Возвращает:
        str: строка с выражением в целевом формате.
    """
    typ = node[0]
    if typ == "ident":
        return node[1]
    if typ == "number":
        return node[1]
    if typ == "empty_paren":
        return "()"
    if typ == "call":
        func = emit(node[1])
        args = ",".join(emit(a) for a in node[2])
        return f"{func}({args})"
    if typ == "lambda":
        params, body = node[1], node[2]
        p = ",".join(params)
        b = "".join(emit(bn) + ";" for bn in body)
        return f"({p}){{{b}}}"
    raise ValueError("unknown node type")

# ---------------- Public API ----------------

def transpile(expression: str) -> str:
    """
    Транспиляция выражения из Kotlin-подобного синтаксиса в компактный Dart-подобный.

    Аргументы:
        expression (str): исходная строка с выражением.

    Возвращает:
        str: строка в целевом формате или пустая строка при ошибке (по правилам kata).
    """
    try:
        toks = tokenize(expression)
        if toks is None:
            return ""
        parser = Parser(toks)
        ast = parser.parse()
        return emit(ast)
    except Exception:
        return ""

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks