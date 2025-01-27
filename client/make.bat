@echo off
REM Переход в корневую директорию проекта
cd ..\
if errorlevel 1 (
    echo Ошибка: Не удалось перейти в корневую директорию проекта.
    pause
    exit /b 1
)

REM Активация виртуального окружения
call venv\Scripts\activate
if errorlevel 1 (
    echo Ошибка: Не удалось активировать виртуальное окружение.
    pause
    exit /b 1
)

REM Проверка версии Python
python --version
if errorlevel 1 (
    echo Ошибка: Python не найден или не работает.
    pause
    exit /b 1
)

REM Переход в директорию client
cd client
if errorlevel 1 (
    echo Ошибка: Директория client не найдена.
    pause
    exit /b 1
)

REM Очистка старой сборки
if exist build (
    rd /s /q build
)
mkdir build
if errorlevel 1 (
    echo Ошибка: Не удалось создать директорию build.
    pause
    exit /b 1
)

REM Переход в директорию build
cd build
if errorlevel 1 (
    echo Ошибка: Не удалось перейти в директорию build.
    pause
    exit /b 1
)

REM Запуск CMake
cmake ..
if errorlevel 1 (
    echo Ошибка: CMake завершился с ошибкой.
    pause
    exit /b 1
)

REM Сборка проекта
cmake --build . --config Release
if errorlevel 1 (
    echo Ошибка: Сборка завершилась с ошибкой.
    pause
    exit /b 1
)

REM Пауза перед завершением
echo Сборка завершена успешно.
pause