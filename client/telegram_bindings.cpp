#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "core/application.h" // Пример заголовочного файла Telegram Desktop

namespace py = pybind11;

PYBIND11_MODULE(telegram_bindings, m) {
    m.def("send_message", [](const std::string& phone, const std::string& message) {
        // Здесь вызываем метод Telegram Desktop для отправки сообщения
        // Например:
        // Core::App().sendMessage(phone, message);
        });

    m.def("start_client", []() {
        // Запуск клиента Telegram Desktop
        // Например:
        // Core::App().start();
        });
}