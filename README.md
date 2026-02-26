# Ansible MCP Collection

The Ansible MCP collection provides modules and plugins to interact with Model Context Protocol (MCP) servers, enabling automated discovery and execution of AI tools via Ansible playbooks. This collection supports both stdio (subprocess) and HTTP transport mechanisms for MCP communication. This collection is maintained by the Ansible community.

**Technology Preview**: This collection is currently in technology preview (v1.0.0-dev0). Features and interfaces may change.

## Contents

- [Description](#description)
- [Communication](#communication)
- [Requirements](#requirements)
  - [Ansible Version Compatibility](#ansible-version-compatibility)
  - [Python Version Compatibility](#python-version-compatibility)
  - [MCP Server Compatibility](#mcp-server-compatibility)
- [Included Content](#included-content)
- [Installation](#installation)
- [Use Cases](#use-cases)
- [Testing](#testing)
  - [Testing with `ansible-test`](#testing-with-ansible-test)
  - [Testing with `tox`](#testing-with-tox)
- [Contributing to This Collection](#contributing-to-this-collection)
- [Publishing New Versions](#publishing-new-versions)
- [Support](#support)
- [Release Notes](#release-notes)
- [Related Information](#related-information)
- [Code of Conduct](#code-of-conduct)
- [License Information](#license-information)

## Description

The primary purpose of this collection is to enable Ansible to interact with MCP (Model Context Protocol) servers, allowing playbooks to discover available AI tools and execute them programmatically. By leveraging this collection, organizations can integrate AI capabilities into their automation workflows, enabling use cases such as:

- **Tool Discovery**: Query MCP servers to discover available tools and their capabilities
- **Tool Execution**: Execute MCP tools with validated parameters and structured output
- **Server Management**: Retrieve server information and health status
- **Multi-Server Orchestration**: Coordinate operations across multiple MCP servers via inventory

The collection implements a persistent connection pattern for efficient communication with MCP servers, supporting both local (stdio) and remote (HTTP) transport mechanisms.

## Communication

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  * [Posts tagged with 'mcp'](https://forum.ansible.com/tag/mcp): subscribe to participate in collection-related conversations.
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Requirements

### Ansible Version Compatibility

<!--start requires_ansible-->
This collection has been tested against the following Ansible versions: **>=2.16.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

**Note**: ansible-core 2.16 reached EOL in May 2025. Future versions will support ansible-core 2.17+.

### Python Version Compatibility

This collection requires Python 3.10 or greater.

### MCP Server Compatibility

This collection supports MCP servers implementing the [Model Context Protocol specification](https://modelcontextprotocol.io/):

- **Protocol Version**: Compatible with MCP servers using JSON-RPC 2.0
- **Transport Methods**:
  - **Stdio**: Communication via stdin/stdout with subprocess-based MCP servers
  - **Streamable HTTP**: HTTP POST-based communication with remote MCP servers
- **Server Configuration**: Servers must be defined in an MCP manifest file (default: `/opt/mcp/mcpservers.json`)

## Included Content

Click on the name of a plugin or module to view that content's documentation:

<!--start collection content-->
### Connection plugins
Name | Description
--- | ---
[ansible.mcp.mcp](https://github.com/ansible-collections/ansible.mcp/blob/main/plugins/connection/mcp.py) | Persistent connection plugin for MCP servers supporting stdio and HTTP transports

### Modules
Name | Description
--- | ---
[ansible.mcp.run_tool](https://github.com/ansible-collections/ansible.mcp/blob/main/plugins/modules/run_tool.py) | Call a specific tool on an MCP server with parameter validation
[ansible.mcp.server_info](https://github.com/ansible-collections/ansible.mcp/blob/main/plugins/modules/server_info.py) | Retrieve MCP server information and capabilities
[ansible.mcp.tools_info](https://github.com/ansible-collections/ansible.mcp/blob/main/plugins/modules/tools_info.py) | Retrieve a list of supported tools from an MCP server

<!--end collection content-->

## Installation

The ansible.mcp collection can be installed with the Ansible Galaxy command-line tool:

```shell
ansible-galaxy collection install ansible.mcp
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: ansible.mcp
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.
To upgrade the collection to the latest available version, run the following command:

```shell
ansible-galaxy collection install ansible.mcp --upgrade
```

A specific version of the collection can be installed by using the `version` keyword in the `requirements.yml` file:

```yaml
---
collections:
  - name: ansible.mcp
    version: 1.0.0
```

or using the `ansible-galaxy` command as follows:

```shell
ansible-galaxy collection install ansible.mcp:==1.0.0
```

### Collection Dependencies

This collection requires `ansible.utils` for persistent connection support:

```shell
ansible-galaxy collection install ansible.utils
```

## Use Cases

You can call modules by their Fully Qualified Collection Name (FQCN), such as `ansible.mcp.run_tool`, or by their short name if you list the `ansible.mcp` collection in the playbook's `collections` keyword.

### Example: Discovering and Executing MCP Tools

```yaml
---
- name: Interact with MCP servers
  hosts: mcp_servers
  connection: ansible.mcp.mcp
  gather_facts: false

  tasks:
    - name: Get server information
      ansible.mcp.server_info:
      register: server_info

    - name: Display server capabilities
      debug:
        msg: "Server {{ server_info.server_info.name }} version {{ server_info.server_info.version }}"

    - name: List available tools
      ansible.mcp.tools_info:
      register: tools

    - name: Display available tools
      debug:
        msg: "Found {{ tools.tools | length }} tools"

    - name: Execute a specific tool
      ansible.mcp.run_tool:
        name: example_tool
        args:
          param1: value1
          param2: value2
      register: tool_result

    - name: Display tool output
      debug:
        var: tool_result.content
```

### Example: Inventory Configuration

Define MCP servers in your inventory:

```yaml
# inventory/mcp_servers.yml
---
all:
  children:
    mcp_servers:
      hosts:
        local_mcp:
          ansible_mcp_server_name: filesystem
          ansible_mcp_manifest_path: /opt/mcp/mcpservers.json

        remote_mcp:
          ansible_mcp_server_name: api_server
          ansible_mcp_manifest_path: /opt/mcp/mcpservers.json
          ansible_mcp_bearer_token: "{{ lookup('env', 'MCP_API_TOKEN') }}"
          ansible_mcp_validate_certs: true
```

### Example: MCP Manifest Configuration

Create an MCP manifest file (default: `/opt/mcp/mcpservers.json`):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["/home/user/workspace"],
      "env": {
        "ALLOWED_PATHS": "/home/user/workspace"
      }
    },
    "api_server": {
      "url": "https://mcp.example.com/api",
      "transport": "streamable-http"
    }
  }
}
```

For documentation on how to use individual modules and other content included in this collection, please see the links in the [Included Content](#included-content) section.

## Testing

This collection is tested using GitHub Actions. To learn more about testing, refer to [CI.md](https://github.com/ansible-collections/ansible.mcp/blob/main/CI.md).

## Contributing to This Collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [ansible.mcp collection repository](https://github.com/ansible-collections/ansible.mcp).

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

See [CONTRIBUTING.md](https://github.com/ansible-collections/ansible.mcp/blob/main/CONTRIBUTING.md) for more details.

### More information about contributing

- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
- [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly

## Support

> **Note:** This collection is currently in Technology Preview (v1.0.0-dev0). APIs and features may change before the stable 1.0.0 release.

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

If you encounter issues or have questions, you can submit a support request through the following channels:
- GitHub Issues: Report bugs, request features, or ask questions by opening an issue in the [GitHub repository](https://github.com/ansible-collections/ansible.mcp/).

## Release Notes

See the [changelog](https://github.com/ansible-collections/ansible.mcp/tree/main/CHANGELOG.rst).

## Related Information

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Official MCP specification and documentation
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## License Information

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
