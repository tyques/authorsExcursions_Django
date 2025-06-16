# Имя файла, в который будет сохранен весь текст.
$outputFile = "combined_django_project.txt"

# Папки, которые нужно исключить из сканирования.
$excludedDirs = @("__pycache__", ".git", "venv", "env", "media", "static_root", ".vscode")

# Файлы, которые нужно исключить.
$excludedFiles = @("combined_django_project.txt", "db.sqlite3")

# Расширения файлов, которые нужно исключить.
$excludedExtensions = @(".pyc", ".log", ".bak", ".tmp", ".sqlite3-journal")

# Получаем полный путь к файлу вывода, чтобы его можно было исключить.
$fullOutputPath = Join-Path -Path $PSScriptRoot -ChildPath $outputFile

# Если итоговый файл уже существует, удаляем его для чистой записи.
if (Test-Path $fullOutputPath) {
    Remove-Item $fullOutputPath
}

# Выводим сообщение о начале работы.
Write-Host "Начинаю сборку проекта в файл: $outputFile"

# Получаем все файлы в текущей директории и поддиректориях.
Get-ChildItem -Path . -Recurse -File | ForEach-Object {
    $file = $_
    $exclude = $false

    # Проверяем, находится ли файл в одной из исключенных папок.
    $pathParts = $file.FullName.Split([System.IO.Path]::DirectorySeparatorChar)
    foreach ($dir in $excludedDirs) {
        if ($pathParts -contains $dir) {
            $exclude = $true
            break
        }
    }

    # Если уже решено исключить, переходим к следующему файлу.
    if ($exclude) { return }

    # Проверяем, не является ли файл одним из исключенных.
    if ($excludedFiles -contains $file.Name) {
        $exclude = $true
    }

    # Если уже решено исключить, переходим к следующему файлу.
    if ($exclude) { return }

    # Проверяем расширение файла.
    if ($excludedExtensions -contains $file.Extension) {
        $exclude = $true
    }

    # Если файл не был исключен, добавляем его содержимое в итоговый файл.
    if (-not $exclude) {
        Write-Host "Добавляю файл: $($file.FullName)"

        # Добавляем заголовок с путем к файлу.
        Add-Content -Path $outputFile -Value "==================== $($file.FullName) ===================="

        # Пытаемся прочитать содержимое как текст и добавляем его.
        try {
            $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop
            Add-Content -Path $outputFile -Value $content
            Add-Content -Path $outputFile -Value "`n" # Добавляем пустую строку для разделения.
        }
        catch {
            # Если файл не удалось прочитать как текст (например, это бинарный файл), выводим предупреждение.
            Write-Warning "Не удалось прочитать файл как текст: $($file.FullName)"
            Add-Content -Path $outputFile -Value " [НЕ УДАЛОСЬ ПРОЧИТАТЬ ФАЙЛ КАК ТЕКСТ] `n"
        }
    }
}

Write-Host "Готово! Весь проект сохранен в файл: $outputFile"