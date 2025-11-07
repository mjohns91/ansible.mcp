# -*- coding: utf-8 -*-

# Copyright (c) 2025 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.connection import Connection
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    """Action plugin for calling tools on an MCP server."""

    def run(self, task_vars=None):
        """Execute the action plugin to call an MCP tool."""
        if task_vars is None:
            task_vars = {}

        result = super(ActionModule, self).run(task_vars=task_vars)

        # Validate connection
        if error := self._validate_connection():
            result["failed"] = True
            result["msg"] = error
            return result

        # Get and validate parameters
        tool_name, tool_args, error = self._get_parameters()
        if error:
            result["failed"] = True
            result["msg"] = error
            return result

        # Execute tool and populate result
        try:
            response = self._execute_tool(tool_name, tool_args)
            self._populate_result(result, response, tool_name)
        except Exception as e:
            result["failed"] = True
            result["msg"] = str(e)

        return result

    def _validate_connection(self):
        """Validate that the connection type is MCP."""
        if self._play_context.connection.split(".")[-1] != "mcp":
            return (
                f"Connection type {self._play_context.connection} is not valid for run_tool, "
                "please use fully qualified name of MCP connection type"
            )
        return None

    def _get_parameters(self):
        """Extract and validate tool parameters."""
        tool_name = self._task.args.get("name")
        tool_args = self._task.args.get("args", {})

        if not tool_name:
            return None, None, "Missing required parameter: 'name'"

        if not isinstance(tool_args, dict):
            return (
                None,
                None,
                f"Parameter 'args' must be a dictionary, got {type(tool_args).__name__}",
            )

        return tool_name, tool_args, None

    def _execute_tool(self, tool_name, tool_args):
        """Execute the tool call via MCP connection."""
        conn = Connection(self._connection.socket_path)
        return conn.call_tool(tool_name, **tool_args)

    def _populate_result(self, result, response, tool_name):
        """Populate result dictionary from MCP response."""
        content = response.get("content", [])
        is_error = response.get("isError", False)

        result["changed"] = False
        result["content"] = content

        if is_error or "isError" in response:
            result["is_error"] = is_error

        if "structured_content" in response:
            result["structured_content"] = response["structured_content"]

        if is_error:
            result["failed"] = True
            result["msg"] = self._extract_error_message(content, tool_name)

    def _extract_error_message(self, content, tool_name):
        """Extract error message from response content."""
        error_messages = [item.get("text", "") for item in content if item.get("type") == "text"]
        return (
            " ".join(error_messages) if error_messages else f"Tool '{tool_name}' execution failed"
        )
