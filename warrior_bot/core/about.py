import click


@click.command(epilog="See usage section at https://aws-wsu.github.io/warrior-bot/ for more.")
def about():
    """Official reference for warrior-bot"""
    click.echo("""
        Warrior-Bot is a CLI (command line interface) that allows users to find information regarding
        people, location, academics, and campus life at Wayne State University. Users access these through
        commands passed to Warrior-Bot. Please see examples below for recommended usage and use help ___
        for specific commands or topics.
               
        warrior-bot where panda-express

               Wayne's very own Panda Express is located on the lowest floor of the Student Center near Starbucks.
            
               
        warrior-bot whois president
               
               Wayne State University's current interim president is Richard A. Bierschbach.
               

        warrior-bot what clubs
               
               Wayne State University offers a variety of clubs for all interest levels. Some popular ones are
                    AWS Club
                    Formula SAE
                    Academic Senate
               
               
        warrior-bot go campus-map
               
               Opens default browser to https://maps.wayne.edu/
    """)
    
