import sys

import git

REMOTE_URL = "https://github.com/ISISNeutronMuon/InstrumentScripts"
REMOTE_BRANCH = "master"
REPO_DIR_PATH = "./InstrumentScripts"

instruments = [
    "NDXCRISP",
    "NDXINTER",
    "NDXOFFSPEC",
    "NDXPOLREF",
    "NDXSURF",
    "NDXARGUS",
    "NDXCHRONUS",
    "NDXEMU",
    "NDXHIFI",
    "NDXMUSR",
    "NDXLARMOR",
    "NDXLOQ",
    "NDXSANS2D",
    "NDXZOOM",
]

diverged_instruments = {}
branch_not_existing = []


def check_instrument(branch_to_check_name, master_repo):
    # Your last commit of the current branch
    master_last_commit = master_repo.head.commit.tree
    try:
        branch_last_commit = master_repo.commit("origin/" + branch_to_check_name)
    except git.exc.BadName:
        print(f"ERROR: {branch_to_check_name} branch does not exist on remote")
        branch_not_existing.append(branch_to_check_name)
        return

    new_files = []
    deleted_files = []
    modified_files = []

    # Comparing branch to master so what changes are there on the branch not present on master
    # do not change order of comparison as this will reverse the diff
    difference_between_branch_to_master = master_last_commit.diff(branch_last_commit)

    # Collection of all new files
    for change in difference_between_branch_to_master.iter_change_type("A"):
        file = change.a_path if change.a_path else change.b_path
        new_files.append(file)

    # Collection of all deleted files
    for change in difference_between_branch_to_master.iter_change_type("D"):
        file = change.a_path if change.a_path else change.b_path
        deleted_files.append(file)

    # Collection of all modified files
    for change in difference_between_branch_to_master.iter_change_type("M"):
        file = change.a_path if change.a_path else change.b_path
        modified_files.append(file)

    if len(new_files) > 0 or len(deleted_files) > 0 or len(modified_files) > 0:
        print(f"ERROR: {branch_to_check_name} has diverged")
        diverged_instruments[branch_to_check_name] = {
            "new": new_files,
            "deleted": deleted_files,
            "modified": modified_files,
        }
    else:
        print(f"{branch_to_check_name} is up to date")


def check_all_scripts(instruments):
    print("Starting instrument script divergence checker")

    # clone repo
    git.Repo.clone_from(REMOTE_URL, REPO_DIR_PATH)

    # checkout to the remote branch
    masterRepo = git.Repo(REPO_DIR_PATH)
    masterRepo.git.checkout(REMOTE_BRANCH)

    for instrument in instruments:
        check_instrument(instrument, masterRepo)


# Manual running (for the time being)
check_all_scripts(instruments)

if len(diverged_instruments) > 0 or len(branch_not_existing) > 0:
    sys.exit(1)
else:
    sys.exit(0)
