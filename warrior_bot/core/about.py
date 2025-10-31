import textwrap

import click


@click.command(
    epilog="See usage section at https://aws-wsu.github.io/warrior-bot/ for more."
)
def about() -> None:
    """Official reference for warrior-bot"""
    title = click.style("Warrior-Bot", fg="green", bold=True)
    intro = (
        f"{title} is a CLI that allows users to find information about people, "
        "locations, academics, and campus life at Wayne State University."
    )

    examples = """
    Examples:

      {cmd1}
          Wayne's very own Panda Express is located on the lowest floor
          of the Student Center near Starbucks.

      {cmd2}
          Wayne State University's current interim president is Richard A. Bierschbach.

      {cmd3}
          Wayne State University offers a variety of clubs for all interest levels.
          Some popular ones are:
            - AWS Cloud Club
            - Formula SAE
            - Academic Senate
            - ...

      {cmd4}
          Opens default browser to https://maps.wayne.edu/
    """.format(
        cmd1=click.style("warrior-bot where panda-express", fg="cyan"),
        cmd2=click.style("warrior-bot whois president", fg="cyan"),
        cmd3=click.style("warrior-bot what clubs", fg="cyan"),
        cmd4=click.style("warrior-bot go campus-map", fg="cyan"),
    )

    click.echo(textwrap.dedent(intro))
    click.echo()
    click.echo(textwrap.dedent(examples).strip())
