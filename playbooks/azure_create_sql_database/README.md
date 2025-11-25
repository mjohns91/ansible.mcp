# azure_create_sql_database playbook

## Overview

This playbook is used to interact with the Azure MCP server. It creates an SQL server instance and a new SQL database
in the provided resource group.
Prior running this playbook, the use should create a resource group as there is no way to create it using the Azure MCP
server.

## Variables

- **`azure_location`**       - The Azure location where to create resource, default: 'eastus'.
- **`azure_subscription`**   - The Azure subscription.
- **`azure_resource_group`** - The Azure resource group.
- **`db_server_name`**       - The name of the database Server.
- **`db_name`**              - The name of the database.

## Usage

1. Log to Azure using the following
   ```bash
   az login
   ```

2. Deploy the resource
   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```