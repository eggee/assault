To get started, we're going to write the code that actually presents the CLI. There are a few ways that we could do this. We could use argparse from the standard library, but we're going to use the popular third-party package click.

Documentation for This Video
argparse
click
Installing click
We'll be using click to create our CLI, so it needs to be a real dependency of our tool. We're going to add this to the Pipfile using Pipenv:

$ pipenv install click
...
Additionally, let's add this to our setup.py in the REQUIRED list so that it will be installed when someone installs our package:

setup.py (partial)

REQUIRED = [
    'click'
]
Building the CLI
Now that we have click installed, we're ready to use it by creating a cli module:

assault/cli.py

import click

@click.command()
def cli():
    pass

if __name__ == "__main__":
    cli()
We've placed the "__main__" portion in there so that we can easily test this. Now we can test our CLI from within our virtualenv by executing this file:

$ pipenv shell
(assault) $ python assault/cli.py --help
Usage: cli.py [OPTIONS]

Options:
  --help  Show this message and exit.
The click.command gives us automatic help page generation and makes it easy for us to develop and define subcommands. Our next step is to add our 3 options using the click.option decorator and the URL argument using click.argument:

assault/cli.py

import click

@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    print(f"Requests: {requests}")
    print(f"Concurrency: {concurrency}")
    print(f"JSON File: {json_file}")
    print(f"URL: {url}")

if __name__ == "__main__":
    cli()
When we take a look at the help text, we see a lot more information:

(assault) $ python assault/cli.py --help
Usage: cli.py [OPTIONS] URL

Options:
  -r, --requests INTEGER     Number of requests
  -c, --concurrency INTEGER  Number of concurrent requests
  -j, --json-file TEXT       Path to output JSON file
  --help                     Show this message and exit.
Let's see what happens when we run the command without the URL argument:

(assault) $ python assault/cli.py
Usage: cli.py [OPTIONS] URL
Try "cli.py --help" for help.

Error: Missing argument "URL".
Finally, let's run it with a URL:

(assault) $ python assault/cli.py https://example.com
Requests: 500
Concurrency: 1
JSON File: None
URL: https://example.com
That's all we need to do to get the information from the user that we can then pass to the business logic of our tool.

Adding the CLI in setup.py
The boilerplate text for the setup.py that we're using already has an entry_points section in it (although commented out). We need to uncomment that section and adjust the boilerplate text:

setup.py (partial)

    entry_points={
        'console_scripts': ['assault=assault.cli:cli'],
    },
We can now test this by running pip install -e .:

(assault) $ pip install -e .
(assault) $ assault
Usage: assault [OPTIONS] URL
Try "assault --help" for help.

Error: Missing argument "URL".
Besides the output that we need to display after we make our requests, our CLI is mostly complete. Let's commit and move on to something else.

(assault) $ git add --all .
(assault) $ git commit -m 'Add click and create CLI'