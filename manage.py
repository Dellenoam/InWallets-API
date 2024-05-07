import asyncio
import asyncclick as click
import os
import sys


@click.group()
async def main():
    """
    Manage the application with this command line tool
    """


@main.command()
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port number to run the server on (default: 8000)",
)
@click.option(
    "--host",
    type=str,
    default="localhost",
    help="Host address to run the server on (default: localhost)",
)
async def runserver(port: int, host: str):
    """
    Run the server
    """
    import uvicorn

    uvicorn.run("main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    sys.path.append(os.path.join(sys.path[0], "src"))
    asyncio.run(main())
