# Mabb programming language 4
Язык программирования Mabb четвертой версии. В прошлых версиях не было лексера, в этой версии я его добавил. Этот язык программирования сделан на python.
Mabb programming language version 4. Previous versions did not have a lexer, I added it to this version. This programming language is created in Python. 

# Документация
_PRINT - команда для вывода текста или же переменной в консоль. Например: _PRINT 'Hello World!' или же для вывода переменной _PRINT variable

_VAR - команда для создания переменной разных типов. _NUMBER - для числа, _TEXT - для текста, _INPUT - для ввода пользователем. Например: _VAR _NUMBER num = 10     _VAR _TEXT text = 'Hello World!'      _VAR _INPUT input = 'Enter a number: '

_EXECUTE - команда для выполнения программы с заданной строки. Например: _EXECUTE 6 - выполняет программу со строки 6.

_IF-_ENDIF - проверяет, истинно ли условие. Если условие не истинно, то программа не выполняет его блок. Например: _IF variable = 'Hello World!' _PRINT 'Variable = Hello World!' _ENDIF

_END - заканчивает программу.

_OPERATION - делает арифметическую операцию над числами/переменными, а после записывает ответ в указанную переменную. Например: _OPERATION sum = num + 1
