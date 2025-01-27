#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "core/application.h" // ������ ������������� ����� Telegram Desktop

namespace py = pybind11;

PYBIND11_MODULE(telegram_bindings, m) {
    m.def("send_message", [](const std::string& phone, const std::string& message) {
        // ����� �������� ����� Telegram Desktop ��� �������� ���������
        // ��������:
        // Core::App().sendMessage(phone, message);
        });

    m.def("start_client", []() {
        // ������ ������� Telegram Desktop
        // ��������:
        // Core::App().start();
        });
}