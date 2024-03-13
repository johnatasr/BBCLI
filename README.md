# BB CLI

BB CLI is a command-line interface tool for interacting with Bitbucket. It provides a set of commands for performing operations such as creating projects, creating repositories, adding users to repositories, and more.

## Requirements

- Python 3.10 or above
- Make installed
- Poetry (Python dependency management tool)

## Setting Up the Environment

1. Make sure you have Python 3.10 or above installed. You can check your Python version by running `python --version` in your terminal.

2. Install Poetry by following the instructions on the official Poetry website.

3. Clone the repository to your local machine.

4. Navigate to the project directory and install the project dependencies with Poetry:

```bash
poetry install
```

5. Set alias for the python execution in linux with:  `alias bb-cli="python main.py"`

## Commands

Here are the available commands in BB CLI:

### create-project: Creates a new project.

```bash
bb-cli create-project -n project_name -w workspace
```

### create-repository: Creates a new repository.

```bash
bb-cli create-repository -p project -r repo_name -w workspace
```

### add-user: Adds a user to a repository.

```bash
bb-cli add-user -r repository -e user_email -w workspace
```

### remove-user: Removes a user from a repository.

```bash
bb-cli remove-user -r repository -u user_name -w workspace -a admin_username -p password
```

### allow-users-merge: Allow all users merge directly in a given branch

```bash
bb-cli allow-users-merge -r firstjohn -w johnatas-upwork -b main
```

Please replace the arguments with your actual values. For example, replace project_name with the name of your project.


## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


## License
This project is licensed under the terms of the MIT license.