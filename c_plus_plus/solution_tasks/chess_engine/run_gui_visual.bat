@echo off
echo Сборка графической версии шахматного движка...
echo ================================================

cd build
if exist "chess_engine_gui.exe" (
    echo Запуск существующего GUI...
    chess_engine_gui.exe
    goto end
)

echo GUI версия не найдена. Создаю простую визуализацию...

powershell -Command "
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Шахматная доска'
$form.Size = New-Object System.Drawing.Size(500, 500)
$form.StartPosition = 'CenterScreen'
$form.BackColor = [System.Drawing.Color]::White

$panel = New-Object System.Windows.Forms.Panel
$panel.Dock = 'Fill'
$panel.BackColor = [System.Drawing.Color]::White
$form.Controls.Add($panel)

$board = @(
    @('r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'),
    @('p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'),
    @('.', '.', '.', '.', '.', '.', '.', '.'),
    @('.', '.', '.', '.', '.', '.', '.', '.'),
    @('.', '.', '.', '.', '.', '.', '.', '.'),
    @('.', '.', '.', '.', '.', '.', '.', '.'),
    @('P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'),
    @('R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R')
)

for ($row = 0; $row -lt 8; $row++) {
    for ($col = 0; $col -lt 8; $col++) {
        $button = New-Object System.Windows.Forms.Button
        $button.Size = New-Object System.Drawing.Size(50, 50)
        $button.Location = New-Object System.Drawing.Point(($col * 50 + 50), ($row * 50 + 50))
        
        if (($row + $col) % 2 -eq 0) {
            $button.BackColor = [System.Drawing.Color]::Tan
        } else {
            $button.BackColor = [System.Drawing.Color]::SaddleBrown
        }
        
        $piece = $board[$row][$col]
        if ($piece -ne '.') {
            $button.Text = $piece
            $button.Font = New-Object System.Drawing.Font('Arial', 16, [System.Drawing.FontStyle]::Bold)
            if ([char]::IsUpper($piece)) {
                $button.ForeColor = [System.Drawing.Color]::White
            } else {
                $button.ForeColor = [System.Drawing.Color]::Black
            }
        }
        
        $panel.Controls.Add($button)
    }
}

$label = New-Object System.Windows.Forms.Label
$label.Text = 'ШАХМАТНАЯ ДОСКА'
$label.Font = New-Object System.Drawing.Font('Arial', 14, [System.Drawing.FontStyle]::Bold)
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(150, 10)
$panel.Controls.Add($label)

$form.ShowDialog()
" > nul

:end
echo Графический интерфейс завершен.
pause