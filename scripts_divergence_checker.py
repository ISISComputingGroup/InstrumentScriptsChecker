import os
import sys
import git
import os
from pathlib import Path 
# noinspection PyUnresolvedReferences
# Workaround for AttributeError when concurrent.futures.thread._threads_queues.clear()
from concurrent.futures import thread
# noinspection PyUnresolvedReferences
from util.channel_access import ChannelAccessUtils

REMOTE_URL = 'https://github.com/ISISNeutronMuon/InstrumentScripts'
REMOTE_BRANCH = 'master'
REPO_DIR_PATH = './InstrumentScripts'

# inst_hostnames = ["NDXARGUS", "NDXCHRONUS", "NDXHIFI", "NDXCHIPIR", "NDXCRYOLAB_R80", "NDXLARMOR", "NDXALF", "NDXDEMO",
#                    "NDXIMAT", "NDXMUONFE", "NDXZOOM", "NDXIRIS", "NDXIRIS_SETUP", "NDXENGINX_SETUP", "NDXHRPD_SETUP", 
#                    "NDXHRPD", "NDXPOLARIS", "NDXVESUVIO", "NDXENGINX", "NDXMERLIN", "NDXRIKENFE", "NDXSELAB", "NDXEMMA-A", 
#                    "NDXSANDALS", "NDXGEM", "NDXMAPS", "NDXOSIRIS", "NDXINES", "NDXTOSCA", "NDXLOQ", "NDXLET", "NDXMARI", 
#                    "NDXCRISP", "NDXSOFTMAT", "NDXSURF", "NDXNIMROD", "NDXDETMON", "NDXEMU", "NDXINTER", "NDXPOLREF", "NDXSANS2D", 
#                    "NDXMUSR", "NDXWISH", "NDXWISH_SETUP", "NDXPEARL", "NDXPEARL_SETUP", "NDXHIFI-CRYOMAG", "NDXOFFSPEC"]

instruments = ChannelAccessUtils().get_inst_list()
diverged_instruments = {}
branch_not_existing = []


def check_instrument(branch_to_check_name, master_repo):
    print(f'Checking {branch_to_check_name}')

    # Your last commit of the current branch
    master_last_commit = master_repo.head.commit.tree
    try:
        branch_last_commit = master_repo.commit("origin/" + branch_to_check_name)
    except git.exc.BadName:
        print(f'{branch_to_check_name} does not exist on remote')
        branch_not_existing.append(branch_to_check_name)
        return

    new_files = []
    deleted_files = []
    modified_files = []

    # Comparing branch to master so what changes are there on the branch not present on master
    # do not change order of comparison as this will reverse the diff
    difference_between_branch_to_master = branch_last_commit.diff(master_last_commit)

    # Collection all new files
    for file in difference_between_branch_to_master.iter_change_type('A'):
        new_files.append(file)

    # Collection all deleted files
    for file in difference_between_branch_to_master.iter_change_type('D'):
        deleted_files.append(file)

    # Collection all modified files
    for file in difference_between_branch_to_master.iter_change_type('M'):
        modified_files.append(file)

    if len(new_files) > 0 or len(deleted_files) > 0 or len(modified_files) > 0:
        print(f'{branch_to_check_name} has diverged')
        diverged_instruments[branch_to_check_name] = {'new': new_files, 'deleted': deleted_files, 'modified': modified_files}
    else:
        print(f'{branch_to_check_name} is up to date')

def check_all_scripts(instruments):
    print('Starting instrument script divergence checker')

    # clone repo
    git.Repo.clone_from(REMOTE_URL, REPO_DIR_PATH)

    # checkout to the remote branch
    masterRepo = git.Repo(REPO_DIR_PATH)
    masterRepo.git.checkout(REMOTE_BRANCH)

    for instrument in instruments:
        check_instrument(instrument['name'], masterRepo)

# Manual running (for the time being)
check_all_scripts(instruments)

if len(diverged_instruments) > 0 or len(branch_not_existing) > 0:
    print("Diverged: " + str(diverged_instruments))
    print("Branch not existing: " + str(branch_not_existing))
    sys.exit(1)
else:
    sys.exit(0)