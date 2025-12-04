## Ansible playbook to interact with Github MCP server to create repository and pull request


## 💡 Description

A practical demonstration using the ansible.mcp collection to interact with the GitHub MCP server. The playbook showcases two core tasks: creating a new GitHub repository and immediately opening a Pull Request against that repository.

## 🛠️ Prerequisites

To run this playbook, you need the following:

  * **The `ansible.mcp` Collection:** This custom collection must be installed locally.
  * **GitHub Personal Access Token (PAT):** A PAT with the necessary scopes (`repo` scope for repository and PR management). These scopes are for using classic token only.


## 🚀 Usage

### 1\. Configure Variables

Update the `vars.yaml` containing the variables to be used by this automation.

You will need to define variables for:

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `github_token` | Your GitHub Personal Access Token. | `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `github_organization` | The Github organization, if not specified the repository will be created in the user space. | ansible-collections |
| `github_repository_name` | The Github repository name. | `testing` |
| `github_branch_name` | The branch name to create the pull request against. | `release_2` |
| `file_content` | The file content to be added. | `foo` |
| `file_path` | The path to the file to create. | `demo.txt` |
| `pull_request_title` | The title of the pull request to create. | `A demo pull request` |
| `pull_request_body` | The pull request body. | `A new pull request created with ansible.mcp collection.` |



### 2\. Run the Playbook

Execute the playbook from your terminal:

```bash
# Example using an extra-var for the token (Recommended)
ansible-playbook playbook.yaml -i inventory.yaml -e @vars.yaml
```
