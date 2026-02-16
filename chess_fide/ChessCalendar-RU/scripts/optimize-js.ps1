# PowerShell script to optimize JavaScript bundles for ChessCalendar-RU

Write-Host "Optimizing JavaScript bundles for ChessCalendar-RU..." -ForegroundColor Green

# Create bundles directory if it doesn't exist
$bundleDir = "static\js\bundles"
if (!(Test-Path $bundleDir)) {
    New-Item -ItemType Directory -Path $bundleDir -Force
    Write-Host "Created directory: $bundleDir" -ForegroundColor Yellow
}

# Function to minify a JS file using Terser (if available) or simple regex
function Minify-JS {
    param([string]$InputFile, [string]$OutputFile)
    
    if (Test-Path $InputFile) {
        Write-Host "Processing: $InputFile -> $OutputFile" -ForegroundColor Cyan
        
        # Read the file content
        $content = Get-Content $InputFile -Raw
        
        # Simple minification using regex (basic version)
        # Remove comments (both single-line and multi-line)
        $minified = $content -replace '(?<!\\)//.*?$|/\*(?:[^*]|\*(?!/))*\*/', ''
        
        # Remove extra whitespace
        $minified = $minified -replace '\s+', ' '
        $minified = $minified -replace '\s*([{}=;:,+\-*/<>()[\]])\s*', '$1'
        $minified = $minified.Trim()
        
        # Write minified content to output file
        $minified | Out-File -FilePath $OutputFile -Encoding UTF8
        
        # Calculate savings
        $originalSize = (Get-Item $InputFile).Length
        $minifiedSize = (Get-Item $OutputFile).Length
        $savings = [math]::Round((($originalSize - $minifiedSize) / $originalSize) * 100, 2)
        
        Write-Host "  Original: $($originalSize) bytes" -ForegroundColor White
        Write-Host "  Minified: $($minifiedSize) bytes" -ForegroundColor White
        Write-Host "  Savings:  $savings%" -ForegroundColor Green
    } else {
        Write-Host "File not found: $InputFile" -ForegroundColor Red
    }
}

# Create optimized bundles by concatenating related files
Write-Host "`nCreating optimized bundles..." -ForegroundColor Green

# Core bundle - essential functionality
$coreFiles = @(
    "static/js/utils.js",
    "static/js/app.js"
)
$coreBundle = "static/js/bundles/core.min.js"
$coreContent = ""
foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        $coreContent += (Get-Content $file -Raw) + "`n"
    }
}
$coreContent | Out-File -FilePath $coreBundle -Encoding UTF8
Minify-JS $coreBundle $coreBundle

# Tournament features bundle
$tournamentFiles = @(
    "static/js/tournament-features.js",
    "static/js/favorites-manager.js",
    "static/js/tournament-comparison.js",
    "static/js/rating-system.js"
)
$tournamentBundle = "static/js/bundles/tournament-features.min.js"
$tournamentContent = ""
foreach ($file in $tournamentFiles) {
    if (Test-Path $file) {
        $tournamentContent += (Get-Content $file -Raw) + "`n"
    }
}
if ($tournamentContent.Trim()) {
    $tournamentContent | Out-File -FilePath $tournamentBundle -Encoding UTF8
    Minify-JS $tournamentBundle $tournamentBundle
}

# UI features bundle
$uiFiles = @(
    "static/js/ui-features.js",
    "static/js/theme-switcher.js",
    "static/js/toast-notifications.js",
    "static/js/adaptive-animations.js",
    "static/js/gesture-handler.js"
)
$uiBundle = "static/js/bundles/ui-features.min.js"
$uiContent = ""
foreach ($file in $uiFiles) {
    if (Test-Path $file) {
        $uiContent += (Get-Content $file -Raw) + "`n"
    }
}
if ($uiContent.Trim()) {
    $uiContent | Out-File -FilePath $uiBundle -Encoding UTF8
    Minify-JS $uiBundle $uiBundle
}

# Analytics and advanced features bundle
$analyticsFiles = @(
    "static/js/analytics.js",
    "static/js/performance-monitor.js",
    "static/js/smart-notifications.js",
    "static/js/advanced-reminders.js"
)
$analyticsBundle = "static/js/bundles/analytics.min.js"
$analyticsContent = ""
foreach ($file in $analyticsFiles) {
    if (Test-Path $file) {
        $analyticsContent += (Get-Content $file -Raw) + "`n"
    }
}
if ($analyticsContent.Trim()) {
    $analyticsContent | Out-File -FilePath $analyticsBundle -Encoding UTF8
    Minify-JS $analyticsBundle $analyticsBundle
}

Write-Host "`nBundle optimization completed!" -ForegroundColor Green
Write-Host "Bundles created in: $bundleDir" -ForegroundColor Yellow

# Show summary
Write-Host "`nBundle Summary:" -ForegroundColor Cyan
Get-ChildItem $bundleDir | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  $($_.Name): ${size} KB" -ForegroundColor White
}

Write-Host "`nTo use the optimized bundles, update your templates to reference the bundled files." -ForegroundColor Green