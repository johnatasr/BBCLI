# BB CLI

BB CLI is a command-line interface tool for interacting with Bitbucket. It provides a set of commands for performing operations such as creating projects, creating repositories, adding users to repositories, and more.

## Requirements

- Python 3.10 or above
- Make installed
- Poetry (Python dependency management tool)

## Setting Up the Environment

1. If you are using Debian/Ubuntu based OS, run the installer `. install.sh` and jump to step 7.

2. Make sure you have Python 3.12 installed. You can check your Python version by running `python --version` in your terminal.

3. Install Poetry by following the instructions on the official Poetry website.

4. Navigate to the project directory and install the project dependencies with Poetry:
```bash
poetry install
```

5. Set alias for the python execution in linux with:  `alias bbcli="python main.py"`

6. Configure the file config.yaml with your `CLIENT_ID` and `CLIENT_SECRET` from Bitbucket OAuth Consumer

## Commands

Here are the available commands in BB CLI using with the created alias:

### create-project: Creates a new project.

```bash
bbcli create-project -n project_name -w workspace
```

### create-repository: Creates a new repository.

```bash
bbcli create-repository -p project -r repo_name -w workspace
```

### add-user: Adds a user to a repository.

```bash
bbcli add-user -r repository -e user_email -w workspace
```

### remove-user: Removes a user from a repository. (Necessary user and app password crendentials)

```bash
bbcli remove-user -r repository -u user_name -w workspace -a admin_username -p password
```

### allow-users-merge: Allow all users merge directly in a given branch

```bash
bbcli allow-users-merge -r firstjohn -w johnatas-upwork -b main
```

Please replace the arguments with your actual values. For example, replace project_name with the name of your project.

#### Other commans 

``bash
make tests
`` - For running all unit tests

``bash
make lint
`` - For lint all project

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.


## License
This project is licensed under the terms of the MIT license.
