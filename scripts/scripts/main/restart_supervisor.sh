#!/bin/bash
rm -r celerybeat-schedule
echo "Удаление файла celerybeat"
systemctl restart supervisor.service
echo "Supervisor service перезапущен!"
