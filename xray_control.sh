#!/bin/bash

# Путь к системе управления службами
SERVICE="xray"

# Функция для запуска Xray
start_xray() {
    echo "Запуск Xray..."
    sudo systemctl start $SERVICE
    if [[ $? -eq 0 ]]; then
        echo "Xray успешно запущен."
    else
        echo "Ошибка при запуске Xray."
    fi
}

stop_xray() {
    echo "Остановка Xray..."
    sudo systemctl stop $SERVICE
    if [[ $? -eq 0 ]]; then
        echo "Xray успешно остановлен."
    else
        echo "Ошибка при остановке Xray."
    fi
}

status_xray() {
    sudo systemctl status $SERVICE
}


restart_xray() {
    echo "Перезапуск Xray..."
    sudo systemctl restart $SERVICE
    if [[ $? -eq 0 ]]; then
        echo "Xray успешно перезапущен."
    else
        echo "Ошибка при перезапуске Xray."
    fi
}

case "$1" in
    start)
        start_xray
        ;;
    stop)
        stop_xray
        ;;
    status)
        status_xray
        ;;
    restart)
        restart_xray
        ;;
    *)
        echo "Использование: $0 {start|stop|status|restart}"
        exit 1
esac

exit 0
