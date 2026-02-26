# Continuous Integration (CI)

## MCP Collection Testing

GitHub Actions are used to run the CI for the ansible.mcp collection. The workflows used for the CI can be found [here](https://github.com/ansible-collections/ansible.mcp/tree/main/.github/workflows). These workflows include jobs to run the unit tests, sanity tests, linters, integration tests, and changelog checks.

The collection uses reusable workflows from [ansible/ansible-content-actions](https://github.com/ansible/ansible-content-actions) for standardized testing.

### PR Testing Workflows

The following tests run on every pull request:

| Job | Description | Python Versions | ansible-core Versions |
| --- | ----------- | --------------- | --------------------- |
| Changelog | Checks for the presence of changelog fragments (skippable with `skip-changelog` label) | 3.12 | devel |
| Linters | Runs `black`, `flake8`, `isort`, `mypy`, and `yamllint` on plugins and tests via tox | 3.12 | N/A |
| Sanity | Runs ansible sanity checks | 3.10, 3.11, 3.12 | 2.16 |
| Unit tests | Executes unit test cases | 3.10, 3.11, 3.12 | 2.16 |
| Ansible-lint | Runs ansible-lint validation | Latest | devel |
| Build-import | Validates collection build and import | Latest | devel |

### Python Version Compatibility by ansible-core Version

These are determined by the reusable workflows from [ansible/ansible-content-actions](https://github.com/ansible/ansible-content-actions) and the collection's minimum requirements.

For the official Ansible core support matrix, see the [Ansible documentation](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).

The collection requires:
- **ansible-core**: >=2.16
- **Python**: 3.10+

| ansible-core Version | Sanity Tests | Unit Tests | Integration Tests |
| -------------------- | ------------ | ---------- | ----------------- |
| 2.16 | 3.10, 3.11, 3.12 | 3.10, 3.11, 3.12 | Not in CI (manual) |

**Note**:
- ansible-core 2.16 reached EOL in May 2025.
- The collection is currently in Technology Preview status (v1.0.0-dev0).
- Integration tests exist but are not currently automated in CI workflows.

### Integration Test Details

Integration tests are available but currently run manually. They include:

- **prepare_inventory**: Sets up test inventory for MCP servers
- **run_tool**: Tests the `ansible.mcp.run_tool` module for executing MCP tools
- **server_info**: Tests the `ansible.mcp.server_info` module for retrieving server capabilities
- **tools_info**: Tests the `ansible.mcp.tools_info` module for listing available tools

Integration tests require:
- MCP servers to be configured and available
- The `uvx` command (from the `uv` package) for AWS IAM integration tests
- Valid MCP server manifest at `/opt/mcp/mcpservers.json` or custom path

To run integration tests manually:

```bash
# Run all integration tests
python -m tox --ansible -e integration

# Run a specific integration test target
ansible-test integration run_tool
```

### Additional Dependencies

The collection depends on the following:
- **Runtime**: `ansible.utils` (for `PersistentConnectionBase`)
- **Development**: See `test-requirements.txt` for full list including pytest, pytest-ansible, pytest-xdist
- **MCP Servers**: Configured in manifest JSON file for integration testing

### Linter Configuration

The linters job uses tox to run multiple linters with specific configurations:

- **black**: Line length 160, code formatting
- **flake8**: Line length 160, ignores E203, E402, F841, DOC
- **isort**: Import sorting with default settings
- **mypy**: Type checking for `plugins/plugin_utils/` directory
- **yamllint**: YAML file validation

All linter configurations are defined in `tox.ini` and can be run locally with:

```bash
tox -e linters
```

### Transport Support

The collection supports two MCP transport types:
- **Stdio**: Subprocess-based communication for local MCP servers
- **Streamable HTTP**: HTTP POST-based communication for remote MCP servers

Integration tests validate both transport mechanisms where applicable.

### Future Enhancements

Planned CI improvements:
- Automated integration test execution in GitHub Actions
- Matrix testing across multiple ansible-core versions (2.17+)
- Extended Python version support (3.13+) as ansible-core support evolves
- Mock MCP server for faster, more reliable integration testing
