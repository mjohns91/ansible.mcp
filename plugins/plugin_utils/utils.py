# -*- coding: utf-8 -*-

# Copyright (c) 2025 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from typing import Any


def validate_connection_plugin(play_context: Any, module_name: str) -> dict:
    """Ensure the action module is running with the mcp connection plugin.

    Args:
        play_content: The object containing the playbook context.
        module_name: The name of the module being executed.
    Returns:
        An optional dictionary with the error message.
    """

    result: dict[str, Any] = {}
    connection_name = play_context.connection.split(".")[-1]
    if connection_name != "mcp":
        # It is supported only with mcp connection plugin
        result["failed"] = True
        result["msg"] = (
            f"connection type {play_context.connection} is not valid for {module_name} module,"
            " please use fully qualified name of mcp connection type"
        )
    return result
