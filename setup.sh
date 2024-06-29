#!/bin/bash

# Add Microsoft repository key and list
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update package list
apt-get update

# Install necessary dependencies
apt-get install -y alien libodbc1 unixodbc unixodbc-dev

# Convert and install the msodbcsql17 package
alien -i ./odbc_debs/msodbcsql17.deb || apt-get -f install -y

# Clean up
rm -rf /var/lib/apt/lists/*
