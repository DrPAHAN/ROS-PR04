# Работа с параметрами (PR04)

## 1. Изменение допустимого значения (10.0 -> 5.0 Гц)
```bash
$ ros2 param set /patrol publish_hz 5.0
Set parameter successful
[INFO] ... Таймер пересоздан с частотой 5.0 Гц
$ ros2 topic hz /turtle1/cmd_vel
average rate: 5.000
