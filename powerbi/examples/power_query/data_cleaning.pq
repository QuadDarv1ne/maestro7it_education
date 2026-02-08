/*
Power Query примеры для очистки и преобразования данных
*/

// 1. Базовая очистка данных
let
    Source = Excel.CurrentWorkbook(){[Name="SalesData"]}[Content],
    
    // Удаление полностью пустых строк
    RemoveEmptyRows = Table.SelectRows(Source, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    
    // Удаление дубликатов
    RemoveDuplicates = Table.Distinct(RemoveEmptyRows),
    
    // Замена ошибочных значений
    ReplaceErrors = Table.ReplaceValue(RemoveDuplicates, "N/A", null, Replacer.ReplaceValue, {"Amount", "Quantity"}),
    
    // Удаление ненужных столбцов
    RemoveColumns = Table.RemoveColumns(ReplaceErrors, {"Notes", "Comments"}),
    
    // Переименование столбцов
    RenameColumns = Table.RenameColumns(RemoveColumns, {
        {"Prod Name", "ProductName"},
        {"Cust ID", "CustomerID"},
        {"Ord Date", "OrderDate"}
    })
in
    RenameColumns


// 2. Преобразование типов данных
let
    Source = #"Previous Step",
    
    // Изменение типов данных
    ChangeTypes = Table.TransformColumnTypes(Source, {
        {"OrderDate", type date},
        {"Amount", type number},
        {"Quantity", Int64.Type},
        {"CustomerID", type text},
        {"IsActive", type logical}
    }),
    
    // Создание вычисляемых столбцов
    AddColumns = Table.AddColumn(ChangeTypes, "OrderValue", each [Amount] * [Quantity], type number),
    
    // Форматирование дат
    FormatDates = Table.AddColumn(AddColumns, "OrderMonth", each Date.ToText([OrderDate], "yyyy-MM"), type text)
in
    FormatDates


// 3. Работа с текстом
let
    Source = #"Previous Step",
    
    // Очистка текстовых данных
    CleanText = Table.TransformColumns(Source, {
        {"ProductName", Text.Proper},        // Капитализация
        {"CustomerName", Text.Trim},         // Удаление пробелов
        {"Email", Text.Lower},              // Нижний регистр
        {"Category", Text.Upper}            // Верхний регистр
    }),
    
    // Извлечение подстрок
    ExtractParts = Table.AddColumn(CleanText, "Domain", each Text.AfterDelimiter([Email], "@"), type text),
    
    // Замена текста
    ReplaceText = Table.ReplaceValue(ExtractParts, "old-domain.com", "new-domain.com", Replacer.ReplaceText, {"Email"})
in
    ReplaceText


// 4. Работа с датами
let
    Source = #"Previous Step",
    
    // Извлечение компонентов даты
    AddDateComponents = Table.AddColumn(Source, "Year", each Date.Year([OrderDate]), Int64.Type),
    AddMonth = Table.AddColumn(AddDateComponents, "Month", each Date.Month([OrderDate]), Int64.Type),
    AddDay = Table.AddColumn(AddMonth, "Day", each Date.Day([OrderDate]), Int64.Type),
    AddWeekday = Table.AddColumn(AddDay, "Weekday", each Date.DayOfWeek([OrderDate]), Int64.Type),
    
    // Создание кварталов
    AddQuarter = Table.AddColumn(AddWeekday, "Quarter", each "Q" & Text.From(Number.RoundUp(Date.Month([OrderDate])/3)), type text),
    
    // Расчет рабочих дней
    AddWorkday = Table.AddColumn(AddQuarter, "IsWorkday", each if Date.DayOfWeek([OrderDate]) < 5 then "Рабочий" else "Выходной", type text)
in
    AddWorkday


// 5. Условные преобразования
let
    Source = #"Previous Step",
    
    // Условная замена значений
    ConditionalReplace = Table.AddColumn(Source, "StatusDescription", each 
        if [StatusCode] = 1 then "Активный"
        else if [StatusCode] = 2 then "Неактивный"
        else if [StatusCode] = 3 then "В ожидании"
        else "Неизвестно", type text
    ),
    
    // Условное удаление строк
    FilterRows = Table.SelectRows(ConditionalReplace, each [Amount] > 0 and [Quantity] > 0),
    
    // Условное создание столбцов
    AddConditionalColumn = Table.AddColumn(FilterRows, "Priority", each 
        if [Amount] > 10000 then "Высокий"
        else if [Amount] > 5000 then "Средний"
        else "Низкий", type text
    )
in
    AddConditionalColumn


// 6. Объединение таблиц
let
    // Загрузка таблиц
    Orders = Excel.CurrentWorkbook(){[Name="Orders"]}[Content],
    Customers = Excel.CurrentWorkbook(){[Name="Customers"]}[Content],
    Products = Excel.CurrentWorkbook(){[Name="Products"]}[Content],
    
    // Объединение Orders и Customers (LEFT JOIN)
    MergeOrdersCustomers = Table.NestedJoin(Orders, {"CustomerID"}, Customers, {"ID"}, "CustomerData", JoinKind.LeftOuter),
    ExpandCustomerData = Table.ExpandTableColumn(MergeOrdersCustomers, "CustomerData", {"Name", "City", "Country"}, {"CustomerName", "CustomerCity", "CustomerCountry"}),
    
    // Объединение с Products (LEFT JOIN)
    MergeWithProducts = Table.NestedJoin(ExpandCustomerData, {"ProductID"}, Products, {"ID"}, "ProductData", JoinKind.LeftOuter),
    ExpandProductData = Table.ExpandTableColumn(MergeWithProducts, "ProductData", {"ProductName", "Category", "Price"}, {"ProductName", "ProductCategory", "UnitPrice"})
in
    ExpandProductData


// 7. Группировка и агрегация
let
    Source = #"Previous Step",
    
    // Группировка по нескольким полям
    GroupByCategoryYear = Table.Group(Source, {"ProductCategory", "Year"}, {
        {"TotalSales", each List.Sum([Amount]), type number},
        {"OrderCount", each Table.RowCount(_), Int64.Type},
        {"AverageOrder", each List.Average([Amount]), type number},
        {"MaxOrder", each List.Max([Amount]), type number},
        {"MinOrder", each List.Min([Amount]), type number},
        {"UniqueCustomers", each List.Count(List.Distinct([CustomerID])), Int64.Type}
    }),
    
    // Сортировка результатов
    SortResults = Table.Sort(GroupByCategoryYear, {{ "TotalSales", Order.Descending }})
in
    SortResults


// 8. Пивотирование данных
let
    Source = #"Previous Step",
    
    // Преобразование в длинный формат
    UnpivotData = Table.UnpivotOtherColumns(Source, {"Product", "Year"}, "Attribute", "Value"),
    
    // Пивотирование по месяцам
    PivotByMonth = Table.Pivot(Source, List.Distinct(Source[Month]), "Month", "Amount", List.Sum),
    
    // Создание иерархии
    AddHierarchy = Table.AddColumn(PivotByMonth, "FullHierarchy", each [Category] & " > " & [Subcategory], type text)
in
    AddHierarchy


// 9. Создание пользовательской функции
let
    // Функция расчета скидки
    CalculateDiscount = (amount as number, discountRate as number) as number =>
    let
        discountAmount = amount * discountRate,
        finalAmount = amount - discountAmount
    in
        finalAmount,
    
    // Использование функции
    Source = #"Previous Step",
    ApplyDiscount = Table.AddColumn(Source, "FinalPrice", each @CalculateDiscount([OriginalPrice], [DiscountRate]), type number)
in
    ApplyDiscount


// 10. Обработка ошибок
let
    Source = #"Previous Step",
    
    // Проверка на null значения
    CheckNulls = Table.AddColumn(Source, "IsValid", each 
        [Amount] <> null and [Quantity] <> null and [CustomerID] <> null
    ),
    
    // Замена ошибок на значения по умолчанию
    HandleErrors = Table.AddColumn(Source, "SafeAmount", each 
        try [Amount] otherwise 0
    ),
    
    // Валидация данных
    ValidateData = Table.SelectRows(HandleErrors, each 
        try Number.IsNumeric([Amount]) and [Amount] >= 0 otherwise false
    )
in
    ValidateData