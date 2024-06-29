#!/bin/bash

# Add Microsoft repository key and list
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update packages list
sudo apt-get update

# Install the ODBC driver
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
