Файл с программой на языке ассемблера обычно имеет расширение `.asm`

Вы можете назвать файл, например, `factorial.asm`

Это расширение указывает на то, что файл содержит исходный код на языке ассемблера.

**Пример имени файла:**
    ```asm
    factorial.asm
    ```

### **Как скомпилировать и запустить:**

1. Сохраните код в файл с именем `factorial.asm`

2. **Скомпилируйте файл с помощью ассемблера, например, `NASM`:**
    ```asm
    nasm -f elf32 factorial.asm -o factorial.o
    ```

3. **Соберите объектный файл с помощью компоновщика, например, ld:**
    ```asm
    ld -m elf_i386 factorial.o -o factorial
    ```

4. **Запустите скомпилированный файл:**
    ```asm
    ./factorial
    ```

Эти шаги помогут вам создать исполняемый файл из исходного кода на языке ассемблера и запустить его на вашей системе.
