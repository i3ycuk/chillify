cmake_minimum_required(VERSION 3.16)
project(BotClient)

set(CMAKE_CXX_STANDARD 17)

# Пути к Qt
find_package(Qt5 REQUIRED COMPONENTS Core Widgets Gui)

# Указываем файлы интерфейса
file(GLOB_RECURSE UI_SOURCES "tdesktop-dev/Telegram/SourceFiles/ui/*.cpp")
# file(GLOB_RECURSE STYLE_SOURCES "SourceFiles/styles/*.cpp")

add_executable(BotClient ${UI_SOURCES} ${STYLE_SOURCES})

# Подключение Qt
target_link_libraries(BotClient Qt5::Core Qt5::Widgets Qt5::Gui)
