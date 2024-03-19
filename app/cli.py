import click

from app.certificate import generate_ssl_certificate
from app.server import run_callback_server
from app.services import BitbucketService
from app.utils import load_constants_from_yaml


@click.group()
def cli():
    """Bitbucket CLI Tool"""


def init_bitbucket_service(internal_click: click) -> BitbucketService:
    constants = load_constants_from_yaml("./configs.yaml")

    internal_click.echo("Please visit the following URL to authorize the application:")
    internal_click.echo(
        "{}/authorize?client_id={}&response_type=code".format(
            constants.get("BITBUCKET_OAUTH2_URL"), constants.get("CLIENT_ID")
        )
    )

    generate_ssl_certificate(click)
    run_callback_server(click)

    code = internal_click.prompt("Enter the authorization code from the callback URL")

    bitbucket_service = BitbucketService(constants)
    if bitbucket_service.do_login(code):
        internal_click.echo("Login successful.")
        internal_click.echo("running ...")
        return bitbucket_service
    else:
        raise SystemExit("Login failed. Please try again")


@cli.command()
@click.option("-n", "--name", required=True, prompt=True, help="Name of the project")
@click.option(
    "-w", "--workspace", required=True, prompt=True, help="Workspace of the project"
)
def create_project(name: str, workspace: str):
    """Create a new project"""
    bitbucket_service: BitbucketService = init_bitbucket_service(click)
    if bitbucket_service.create_project(name, workspace):
        click.echo(f'Project "{name}" created successfully')
        return
    click.echo(f"Failed to create project")


@cli.command()
@click.option(
    "-p",
    "--project",
    required=True,
    prompt=True,
    help="Name of the repository to be created",
)
@click.option(
    "-r", "--repository", required=True, prompt=True, help="Name of the repository"
)
@click.option(
    "-w", "--workspace", required=True, prompt=True, help="Workspace of the repository"
)
def create_repository(
    project: str,
    repository: str,
    workspace: str,
):
    """Create a new repository"""
    bitbucket_service: BitbucketService = init_bitbucket_service(click)
    if bitbucket_service.create_repository(project, repository, workspace):
        click.echo(f'Repository "{repository}" created successfully')
        return
    click.echo(f"Failed to create repository")


@cli.command()
@click.option(
    "-r",
    "--repository",
    required=True,
    prompt=True,
    help="Name of the repository to add user to",
)
@click.option(
    "-e", "--user_email", required=True, prompt=True, help="User email to add"
)
@click.option(
    "-w", "--workspace", required=True, prompt=True, help="Workspace of the user to add"
)
def add_user(
    repository: str,
    user_email: str,
    workspace: str,
):
    """Add a user to a repository"""
    bitbucket_service: BitbucketService = init_bitbucket_service(click)
    if bitbucket_service.add_user_to_repository(repository, user_email, workspace):
        click.echo(
            f'Invite sent to "{user_email}" successfully, request for repository "{repository}"'
        )
        return
    click.echo(f"Failed to add user to repository")


@cli.command()
@click.option(
    "-r",
    "--repository",
    required=True,
    prompt=True,
    help="Name of the repository to remove user from",
)
@click.option(
    "-d",
    "--display_name",
    nargs=2,
    type=str,
    prompt=True,
    required=True,
    help="Full name shown in the Bitbucket platform",
)
@click.option(
    "-w",
    "--workspace",
    required=True,
    prompt=True,
    help="Workspace of the user to remove",
)
@click.option(
    "-a",
    "--admin_username",
    required=True,
    prompt=True,
    help="Admin username of the repository to remove",
)
@click.option(
    "-p",
    "--app_password",
    required=True,
    prompt=True,
    help="Admin app password of the repository to remove",
)
def remove_user(
    repository: str,
    display_name: str,
    workspace: str,
    admin_username: str,
    app_password: str,
):
    """Remove a user from a repository"""
    bitbucket_service: BitbucketService = init_bitbucket_service(click)
    first_name, second_name = display_name
    formatted_name = "{} {}".format(first_name, second_name)
    if bitbucket_service.remove_user_from_repository(
        repository, formatted_name, workspace, admin_username, app_password
    ):
        click.echo(
            f'User "{formatted_name}" removed from repository "{repository}" successfully'
        )
        return
    click.echo(f"Failed to remove user from repository")


@cli.command()
@click.option(
    "-r",
    "--repository",
    required=True,
    prompt=True,
    help="Name of the repository to grant permission",
)
@click.option(
    "-w",
    "--workspace",
    required=True,
    prompt=True,
    help="Workspace of the user to remove",
)
@click.option(
    "-b",
    "--branch",
    required=True,
    prompt=True,
    default="main",
    help="Branch name to be applied",
)
def allow_users_merge(repository: str, workspace: str, branch: str):
    """Allow all users to merge directly in a given branch"""
    bitbucket_service: BitbucketService = init_bitbucket_service(click)
    if bitbucket_service.allow_users_merge_directly(repository, workspace, branch):
        click.echo(f"Users allowed to merge successfully")
        return
    click.echo(f"Failed to create/update branch restriction")
