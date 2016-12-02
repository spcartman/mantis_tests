import random
import string
from model.project import Project


def rand_string(prefix, maxlen):
    chars = string.ascii_letters + string.digits + string.punctuation + " " * 10
    return prefix + "".join([random.choice(chars) for i in range(random.randrange(maxlen))])


def generate_project_data(n):
    return [Project(name=rand_string("name", 10),
                    status=random.choice(("development", "release", "stable", "obsolete")),
                    inherit=random.choice((True, False)),
                    view=random.choice(("public", "private")),
                    description=rand_string("descr", 30))
            for i in range(int(n))]


test_data = generate_project_data(2)
