import yaml
import subprocess
import urllib.request

with urllib.request.urlopen('https://raw.githubusercontent.com/ros2/ros2/master/ros2.repos') as f:
    orig = yaml.safe_load(f.read().decode('utf-8'))

FORKS="./ros2.repos"
forks = yaml.safe_load(open(FORKS))

def find_forks(forks):
    repos = forks["repositories"]
    real_forks = []
    for name, data in repos.items():
        if "Barkhausen" in data["url"]:
            real_forks.append((name, data))
    return real_forks

def merge_fork(directory, url, upstream_branch):
    print (f"Merging repo in {directory} with {url}/{upstream_branch}")
    cmd = f"cd src/{directory} && git remote add upstream {url} && git pull --rebase upstream {upstream_branch}"
    print (f"   cmd is '{cmd}'")
    subprocess.check_call(cmd, shell=True)


def main():
    real_forks = find_forks(forks)
    for f in real_forks:
        orig_repo = orig["repositories"].get(f[0], {})
        orig_url = orig_repo.get("url", None)

        if orig_url is None or orig_repo is None:
            print (f"Ignoring unknown original repo {f[0]}")
        else:
            merge_fork(f[0], orig_url, "master")
            print ("========")



if __name__ == '__main__':
    main()
