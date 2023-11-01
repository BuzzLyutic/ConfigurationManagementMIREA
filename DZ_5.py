import os
import sys

def parse_commit(commit_hash):
# Read the commit object file
with open(os.path.join('.git', 'objects', commit_hash[:2], commit_hash[2:]), 'rb') as f:
data = f.read()

# Decompress the data
import zlib
data = zlib.decompress(data)

# Split the header and body
header, body = data.split(b'\x00', 1)

# Parse the header
header = dict(line.split(b' ', 1) for line in header.split(b'\n') if line)

# Parse the parent pointers
parents = header.get(b'parent', b'').split()

return {
'hash': commit_hash,
'author': header.get(b'author').decode(),
'committer': header.get(b'committer').decode(),
'message': body.decode(),
'parents': parents,
}

def visualize_repo(repo_path):
# Read the HEAD file to get the current branch
with open(os.path.join(repo_path, '.git', 'HEAD'), 'r') as f:
current_branch = f.read().strip().split('/')[-1]

# Read the refs file to get the commit hash of the current branch
with open(os.path.join(repo_path, '.git', 'refs', 'heads', current_branch), 'r') as f:
current_commit = f.read().strip()

# Parse the current commit and its ancestors
commits = [current_commit]
while commits:
commit_hash = commits.pop()
commit = parse_commit(commit_hash)
print(f"{commit_hash}: {commit['message']} ({commit['author']})")
commits.extend(commit['parents'])

if __name__ == '__main__':
visualize_repo(sys.argv[1])