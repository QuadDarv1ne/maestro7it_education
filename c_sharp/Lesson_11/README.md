# Работа с базами данных в C#

Работа с базами данных в `C#` включает использование `SQL` для выполнения запросов и управление подключениями к базам данных через `ADO.NET`.

Рассмотрим основные аспекты работы с базами данных, включая основы `SQL`, подключение через `ADO.NET` и выполнение операций `CRUD`.

### Основы работы с SQL

`SQL (Structured Query Language)` — это язык для управления и манипулирования данными в реляционных базах данных.

**Основные команды SQL включают:**

- `SELECT`: для извлечения данных из таблиц.
- `INSERT`: для добавления новых записей в таблицу.
- `UPDATE`: для изменения существующих записей.
- `DELETE`: для удаления записей из таблицы.

**Примеры SQL-запросов:**

**Выборка данных**

```sql
SELECT * FROM Employees;
```

**Добавление данных**

```sql
INSERT INTO Employees (Name, Position, Salary)
VALUES ('John Doe', 'Software Engineer', 60000);
```

**Обновление данных**

```sql
UPDATE Employees
SET Salary = 65000
WHERE Name = 'John Doe';
```

**Удаление данных**

```sql
DELETE FROM Employees
WHERE Name = 'John Doe';
```

### Подключение к базам данных через ADO.NET

**ADO.NET** — это набор классов в .NET Framework, который позволяет взаимодействовать с базами данных.

**Вот основные шаги подключения и выполнения операций с базой данных через ADO.NET:**

#### Подключение к базе данных

Создайте подключение к базе данных с помощью `SqlConnection` (для SQL Server) или других соответствующих классов.

```sql
using System;
using System.Data.SqlClient;

public class Program
{
    public static void Main()
    {
        string connectionString = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;";

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();
            Console.WriteLine("Соединение установлено.");
        }
    }
}
```

### Выполнение SQL-запросов:

**Выполнение команд (например, `INSERT`, `UPDATE`, `DELETE`):**

```sql
using System;
using System.Data.SqlClient;

public class Program
{
    public static void Main()
    {
        string connectionString = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;";

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();

            string sql = "INSERT INTO Employees (Name, Position, Salary) VALUES ('Jane Doe', 'Manager', 80000)";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                int rowsAffected = command.ExecuteNonQuery();
                Console.WriteLine($"Добавлено {rowsAffected} строк.");
            }
        }
    }
}
```

**Выполнение запросов для получения данных:**

```sql
using System;
using System.Data.SqlClient;

public class Program
{
    public static void Main()
    {
        string connectionString = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;";

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();

            string sql = "SELECT * FROM Employees";
            using (SqlCommand command = new SqlCommand(sql, connection))
            {
                using (SqlDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        Console.WriteLine($"{reader["Name"]}, {reader["Position"]}, {reader["Salary"]}");
                    }
                }
            }
        }
    }
}
```

### Операции с базами данных (CRUD)

**CRUD** — это акроним для основных операций с данными:
- Create (создание),
- Read (чтение),
- Update (обновление),
- Delete (удаление).

#### Create (Создание)

Используйте `INSERT` для добавления новых записей.

```csharp
string sql = "INSERT INTO Employees (Name, Position, Salary) VALUES ('Alice Smith', 'Developer', 70000)";
```

#### Read (Чтение)

Используйте `SELECT` для извлечения данных. Вы можете использовать `SqlDataReader для` построчного чтения данных.

```csharp
string sql = "SELECT * FROM Employees";
Update (Обновление):
```

#### Используйте `UPDATE` для изменения существующих записей.

```csharp
string sql = "UPDATE Employees SET Salary = 75000 WHERE Name = 'Alice Smith'";
Delete (Удаление):
```

####  Используйте `DELETE` для удаления записей.

```csharp
string sql = "DELETE FROM Employees WHERE Name = 'Alice Smith'";
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 11.09.2024

**Версия:** 1.0