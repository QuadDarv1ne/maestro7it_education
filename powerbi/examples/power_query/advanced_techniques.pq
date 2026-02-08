/*
Продвинутые Power Query примеры
*/

// 1. Динамическая загрузка файлов
let
    // Получение списка файлов из папки
    SourceFolder = "C:\Data\Sales\",
    Files = Folder.Files(SourceFolder),
    FilteredFiles = Table.SelectRows(Files, each Text.EndsWith([Name], ".xlsx")),
    
    // Динамическая загрузка и объединение
    LoadFiles = Table.AddColumn(FilteredFiles, "Data", each 
        let
            FileContent = Excel.Workbook(File.Contents(SourceFolder & [Name]), null, true),
            SalesSheet = FileContent{[Item="Sales", Kind="Sheet"]}[Data],
            PromotedHeaders = Table.PromoteHeaders(SalesSheet, [PromoteAllScalars=true])
        in
            PromotedHeaders
    ),
    
    // Объединение всех таблиц
    CombinedData = Table.Combine(LoadFiles[Data])
in
    CombinedData


// 2. API интеграция
let
    // Подключение к REST API
    apiUrl = "https://api.example.com/data",
    apiKey = "your-api-key",
    
    Headers = [
        #"Authorization" = "Bearer " & apiKey,
        #"Content-Type" = "application/json"
    ],
    
    Response = Json.Document(Web.Contents(apiUrl, [Headers=Headers])),
    Data = Response[data],
    ToTable = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expanded = Table.ExpandRecordColumn(ToTable, "Column1", {"id", "name", "value"}, {"ID", "Name", "Value"})
in
    Expanded


// 3. Работа с JSON
let
    // Загрузка JSON данных
    JsonSource = "{""products"":[{""id"":1,""name"":""Product A"",""price"":100},{""id"":2,""name"":""Product B"",""price"":200}]}",
    ParsedJson = Json.Document(JsonSource),
    ProductsList = ParsedJson[products],
    ProductsTable = Table.FromList(ProductsList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedProducts = Table.ExpandRecordColumn(ProductsTable, "Column1", {"id", "name", "price"}, {"ID", "Name", "Price"})
in
    ExpandedProducts


// 4. Создание календарной таблицы
let
    // Параметры календаря
    StartDate = #date(2020, 1, 1),
    EndDate = Date.AddYears(DateTime.LocalNow(), 1),
    
    // Создание списка дат
    DateList = List.Dates(StartDate, Duration.Days(EndDate - StartDate)+1, #duration(1,0,0,0)),
    DateTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    
    // Добавление календарных атрибутов
    AddYear = Table.AddColumn(DateTable, "Year", each Date.Year([Date]), Int64.Type),
    AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonth, "MonthName", each Date.MonthName([Date], "ru-RU"), type text),
    AddQuarter = Table.AddColumn(AddMonthName, "Quarter", each "Q" & Text.From(Number.RoundUp(Date.Month([Date])/3)), type text),
    AddDayOfWeek = Table.AddColumn(AddQuarter, "DayOfWeek", each Date.DayOfWeek([Date]), Int64.Type),
    AddDayName = Table.AddColumn(AddDayOfWeek, "DayName", each Date.DayOfWeekName([Date], "ru-RU"), type text),
    AddIsWeekend = Table.AddColumn(AddDayName, "IsWeekend", each if Date.DayOfWeek([Date]) >= 5 then "Да" else "Нет", type text),
    AddWeekNumber = Table.AddColumn(AddIsWeekend, "WeekNumber", each Date.WeekOfYear([Date]), Int64.Type)
in
    AddWeekNumber


// 5. Иерархическая структура данных
let
    Source = Excel.CurrentWorkbook(){[Name="OrgStructure"]}[Content],
    
    // Создание иерархии
    AddHierarchy = Table.AddColumn(Source, "HierarchyPath", each 
        let
            ParentID = [ParentID],
            CurrentID = [ID],
            Path = if ParentID = null then Text.From(CurrentID) else @GetParentPath(ParentID) & " > " & Text.From(CurrentID)
        in
            Path
    ),
    
    // Рекурсивная функция для построения пути
    GetParentPath = (parentID as number) as text =>
    let
        ParentRow = Table.SelectRows(Source, each [ID] = parentID),
        ParentParentID = if Table.IsEmpty(ParentRow) then null else ParentRow{0}[ParentID],
        CurrentName = if Table.IsEmpty(ParentRow) then "" else Text.From(ParentRow{0}[Name])
    in
        if ParentParentID = null then CurrentName
        else @GetParentPath(ParentParentID) & " > " & CurrentName
in
    AddHierarchy


// 6. Анализ временных рядов
let
    Source = #"Previous Step",
    
    // Сортировка по дате
    Sorted = Table.Sort(Source, {{ "Date", Order.Ascending }}),
    
    // Расчет скользящего среднего
    AddMovingAverage = Table.AddColumn(Sorted, "MovingAverage7", each 
        let
            CurrentDate = [Date],
            SevenDaysAgo = Date.AddDays(CurrentDate, -6),
            PeriodData = Table.SelectRows(Sorted, each [Date] >= SevenDaysAgo and [Date] <= CurrentDate),
            AverageValue = List.Average(PeriodData[Value])
        in
            AverageValue
    ),
    
    // Расчет накопительной суммы
    AddRunningTotal = Table.AddColumn(AddMovingAverage, "RunningTotal", each 
        List.Sum(
            Table.SelectRows(AddMovingAverage, each [Date] <= [Date])[Value]
        )
    ),
    
    // Расчет процентного изменения
    AddGrowthRate = Table.AddColumn(AddRunningTotal, "GrowthRate", each 
        let
            PreviousRow = Table.SelectRows(AddRunningTotal, each [Date] = Date.AddDays([Date], -1)),
            PreviousValue = if Table.IsEmpty(PreviousRow) then null else PreviousRow{0}[Value],
            CurrentValue = [Value]
        in
            if PreviousValue = null or PreviousValue = 0 then null
            else (CurrentValue - PreviousValue) / PreviousValue
    )
in
    AddGrowthRate


// 7. Создание параметризованных запросов
let
    // Параметры
    StartDateParam = DateTime.From(Date.AddMonths(DateTime.LocalNow(), -12)),
    EndDateParam = DateTime.From(DateTime.LocalNow()),
    MinAmountParam = 1000,
    
    Source = Excel.CurrentWorkbook(){[Name="Sales"]}[Content],
    
    // Применение параметров
    FilterByDate = Table.SelectRows(Source, each [Date] >= StartDateParam and [Date] <= EndDateParam),
    FilterByAmount = Table.SelectRows(FilterByDate, each [Amount] >= MinAmountParam),
    
    // Группировка с параметрами
    Grouped = Table.Group(FilterByAmount, {"CustomerID"}, {
        {"TotalSales", each List.Sum([Amount]), type number},
        {"OrderCount", each Table.RowCount(_), Int64.Type},
        {"AvgOrder", each List.Average([Amount]), type number}
    })
in
    Grouped


// 8. Обработка ошибок и исключений
let
    Source = Excel.CurrentWorkbook(){[Name="RawData"]}[Content],
    
    // Безопасное преобразование типов
    SafeTypeConversion = Table.TransformColumns(Source, {
        {"Amount", each try Number.From(_) otherwise 0},
        {"Date", each try DateTime.From(_) otherwise #datetime(1900,1,1,0,0,0)},
        {"Quantity", each try Int64.From(_) otherwise 0}
    }),
    
    // Валидация данных
    ValidateData = Table.AddColumn(SafeTypeConversion, "IsValid", each 
        try 
            Number.IsNumeric([Amount]) and 
            [Amount] >= 0 and 
            DateTime.IsDateTime([Date]) and
            Int64.Is([Quantity]) and
            [Quantity] >= 0
        otherwise false
    ),
    
    // Фильтрация по валидным записям
    ValidRecords = Table.SelectRows(ValidateData, each [IsValid] = true),
    
    // Логирование ошибок
    ErrorLog = Table.SelectRows(ValidateData, each [IsValid] = false)
in
    ValidRecords


// 9. Создание пользовательских типов данных
let
    Source = Excel.CurrentWorkbook(){[Name="Products"]}[Content],
    
    // Создание пользовательского типа
    AddProductType = Table.AddColumn(Source, "ProductType", each 
        let
            Category = [Category],
            Price = [Price]
        in
            if Category = "Electronics" and Price > 1000 then "Премиум"
            else if Category = "Electronics" then "Стандарт"
            else if Price > 500 then "Премиум"
            else "Базовый"
    ),
    
    // Создание статуса товара
    AddProductStatus = Table.AddColumn(AddProductType, "Status", each 
        if [Stock] = 0 then "Нет в наличии"
        else if [Stock] < 10 then "Заканчивается"
        else if [IsActive] = false then "Снят с продажи"
        else "В наличии"
    )
in
    AddProductStatus


// 10. Оптимизация производительности
let
    Source = Excel.CurrentWorkbook(){[Name="LargeDataset"]}[Content],
    
    // Ранняя фильтрация
    EarlyFilter = Table.SelectRows(Source, each [Date] >= #date(2023,1,1)),
    
    // Удаление ненужных столбцов на ранней стадии
    EarlyColumnRemoval = Table.RemoveColumns(EarlyFilter, {"Description", "Notes", "Comments"}),
    
    // Типизация на ранней стадии
    EarlyTypeConversion = Table.TransformColumnTypes(EarlyColumnRemoval, {
        {"Date", type date},
        {"Amount", type number},
        {"CustomerID", type text}
    }),
    
    // Создание индекса для оптимизации
    AddIndex = Table.AddIndexColumn(EarlyTypeConversion, "Index", 1, 1)
in
    AddIndex