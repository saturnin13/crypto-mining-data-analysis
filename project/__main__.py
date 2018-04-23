import sys

from lib.options import Options
from lib.project import Project


def run_project(args):
    options = Options()
    options.parse(args[1:])

    project = Project(options)

    # project.date()
    # example arg: project.print_example_arg()
    input()

if __name__ == '__main__':
    run_project(sys.argv)