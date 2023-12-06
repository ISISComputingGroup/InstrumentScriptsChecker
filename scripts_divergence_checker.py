import os
import sys
import git
import os
from pathlib import Path 
# noinspection PyUnresolvedReferences
# Workaround for AttributeError when concurrent.futures.thread._threads_queues.clear()
from concurrent.futures import thread
# noinspection PyUnresolvedReferences

REMOTE_URL = 'https://github.com/ISISNeutronMuon/InstrumentScripts'
REMOTE_BRANCH = 'master'
REMOTE_DIR_PATH = './InstrumentScripts'

# inst_hostnames = ["NDXARGUS", "NDXCHRONUS", "NDXHIFI", "NDXCHIPIR", "NDXCRYOLAB_R80", "NDXLARMOR", "NDXALF", "NDXDEMO",
#                    "NDXIMAT", "NDXMUONFE", "NDXZOOM", "NDXIRIS", "NDXIRIS_SETUP", "NDXENGINX_SETUP", "NDXHRPD_SETUP", 
#                    "NDXHRPD", "NDXPOLARIS", "NDXVESUVIO", "NDXENGINX", "NDXMERLIN", "NDXRIKENFE", "NDXSELAB", "NDXEMMA-A", 
#                    "NDXSANDALS", "NDXGEM", "NDXMAPS", "NDXOSIRIS", "NDXINES", "NDXTOSCA", "NDXLOQ", "NDXLET", "NDXMARI", 
#                    "NDXCRISP", "NDXSOFTMAT", "NDXSURF", "NDXNIMROD", "NDXDETMON", "NDXEMU", "NDXINTER", "NDXPOLREF", "NDXSANS2D", 
#                    "NDXMUSR", "NDXWISH", "NDXWISH_SETUP", "NDXPEARL", "NDXPEARL_SETUP", "NDXHIFI-CRYOMAG", "NDXOFFSPEC"]

inst_hostnames = ["NDW2641"]

diverged = {}


def check_instrument(hostname, remote_repo):
    print(f'Checking {hostname}')

    # repo variable
    repo = remote_repo

    # Your last commit of the current branch
    commit_feature = repo.head.commit.tree

    # Your last commit of the dev branch
    commit_origin_dev = repo.commit("origin/" + REMOTE_BRANCH)
    new_files = []
    deleted_files = []
    modified_files = []

    # Comparing 
    diff_index = commit_origin_dev.diff(commit_feature)

    # Collection all new files
    for file in diff_index.iter_change_type('A'):
        new_files.append(file)

    # Collection all deleted files
    for file in diff_index.iter_change_type('D'):
        deleted_files.append(file)

    # Collection all modified files
    for file in diff_index.iter_change_type('M'):
        modified_files.append(file)

    # # Print all new files
    # if len(new_files) > 0:
    #     print("New files:")
    #     for file in new_files:
    #         print(file.a_path)

    # # Print all deleted files
    # if len(deleted_files) > 0:
    #     print("Deleted files:")
    #     for file in deleted_files:
    #         print(file.a_path)
    
    # # Print all modified files
    # if len(modified_files) > 0:
    #     print("Modified files:")
    #     for file in modified_files:
    #         print(file.a_path)
    if len(new_files) > 0 or len(deleted_files) > 0 or len(modified_files) > 0:
        diverged[hostname] = {'new': new_files, 'deleted': deleted_files, 'modified': modified_files}

def check_all_scripts(hostnames):
    print('Starting instrument script divergence checker')

    # clone repo
    git.Repo.clone_from(REMOTE_URL, REMOTE_DIR_PATH)

    # checkout to the remote branch
    repo = git.Repo(REMOTE_DIR_PATH)
    repo.git.checkout(REMOTE_BRANCH)

    for hostname in hostnames:
        check_instrument(hostname, repo)

    return diverged


# Manual running (for the time being)
print(check_all_scripts(inst_hostnames))

if len(diverged) > 0:
    sys.exit(1)
else:
    sys.exit(0)