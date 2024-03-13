import click

from app.certificate import generate_ssl_certificate
from app.server import run_callback_server
from app.services import BitbucketService
from app.utils import load_constants_from_yaml


@click.group()
@click.pass_context
def cli(ctx):
    """Bitbucket CLI Tool"""
    constants = load_constants_from_yaml("./configs.yaml")

    click.echo("Please visit the following URL to authorize the application:")
    click.echo(
        "{}/authorize?client_id={}&response_type=code".format(
            constants.get("BITBUCKET_OAUTH2_URL"), constants.get("CLIENT_ID")
        )
    )

    generate_ssl_certificate(click)
    run_callback_server(click)

    code = click.prompt("Enter the authorization code from the callback URL")

    ctx.obj = BitbucketService(constants)
    if ctx.obj.do_login(code):
        click.echo("Login successful.")
        click.echo("running ...")
    else:
        click.echo("Login failed. Please try again.")


@cli.command()
@click.option("-n", "--name", prompt=True, help="Name of the project")
@click.option("-w", "--workspace", prompt=True, help="Workspace of the project")
@click.pass_obj
def create_project(bitbucket_service: BitbucketService, name, workspace: str):
    """Create a new project"""
    if bitbucket_service.create_project(name, workspace):
        click.echo(f'Project "{name}" created successfully')
        return
    click.echo(f"Failed to create project")


@cli.command()
@click.option(
    "-p", "--project", prompt=True, help="Name of the repository to be created"
)
@click.option("-r", "--repository", prompt=True, help="Name of the repository")
@click.option("-w", "--workspace", prompt=True, help="Workspace of the repository")
@click.pass_obj
def create_repository(
    bitbucket_service: BitbucketService,
    project,
    repository,
    workspace: str,
):
    """Create a new repository"""
    if bitbucket_service.create_repository(project, repository, workspace):
        click.echo(f'Repository "{repository}" created successfully')
        return
    click.echo(f"Failed to create repository")


@cli.command()
@click.option(
    "-r", "--repository", prompt=True, help="Name of the repository to add user to"
)
@click.option("-e", "--user_email", prompt=True, help="User email to add")
@click.option("-w", "--workspace", prompt=True, help="Workspace of the user to add")
@click.pass_obj
def add_user(
    bitbucket_service: BitbucketService, repository, user_email, workspace: str
):
    """Add a user to a repository"""
    if bitbucket_service.add_user_to_repository(repository, user_email, workspace):
        click.echo(
            f'User "{user_email}" added to repository "{repository}" successfully'
        )
        return
    click.echo(f"Failed to add user to repository")


@cli.command()
@click.option(
    "-r", "--repository", prompt=True, help="Name of the repository to remove user from"
)
@click.option("-u", "--user_name", prompt=True, help="Username of the user to remove")
@click.option("-w", "--workspace", prompt=True, help="Workspace of the user to remove")
@click.option(
    "-a",
    "--admin_username",
    prompt=True,
    help="Admin username of the repository to remove",
)
@click.option(
    "-p",
    "--password",
    prompt=True,
    help="Admin app password of the repository to remove",
)
@click.pass_obj
def remove_user(
    bitbucket_service: BitbucketService,
    repository,
    user_name,
    workspace,
    admin_username,
    password: str,
):
    """Remove a user from a repository"""
    if bitbucket_service.remove_user_from_repository(
        repository, user_name, workspace, admin_username, password
    ):
        click.echo(
            f'User "{user_name}" removed from repository "{repository}" successfully'
        )
        return
    click.echo(f"Failed to remove user from repository: some text")


@cli.command()
@click.option(
    "-r", "--repository", prompt=True, help="Name of the repository to grant permission"
)
@click.option("-w", "--workspace", prompt=True, help="Workspace of the user to remove")
@click.option(
    "-b", "--branch", prompt=True, default="main", help="Branch name to be applied"
)
@click.pass_obj
def allow_users_merge(
    bitbucket_service: BitbucketService, repository, workspace, branch: str
):
    """Allow all users to merge directly in a given branch"""
    if bitbucket_service.allow_users_merge_directly(repository, workspace, branch):
        click.echo(f"Users allowed to merge successfully")
        return
    click.echo(f"Failed to create/update branch restriction")
