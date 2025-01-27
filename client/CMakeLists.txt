cmake_minimum_required(VERSION 3.14)
project(telegram_bindings)

# Использование FetchContent для загрузки pybind11
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.13.6  # Укажите нужную версию
)
FetchContent_MakeAvailable(pybind11)

# Создание модуля Python
pybind11_add_module(telegram_bindings telegram_bindings.cpp)

# Связывание с библиотекой TelegramCore
target_link_libraries(telegram_bindings PRIVATE TelegramCore)