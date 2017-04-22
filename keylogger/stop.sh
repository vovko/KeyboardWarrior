#!/usr/bin/env bash
sudo kill -9 $(sudo less /var/run/logkeys.pid)
sudo rm /var/run/logkeys.pid