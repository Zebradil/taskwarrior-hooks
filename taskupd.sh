function _taskupd() {
    DEFAULT_DIR=~/.task

    cd ${1:-$DEFAULT_DIR}

    if ! git rev-parse --git-dir 1>/dev/null 2>&1; then
        echo "$(pwd) is not in a git repository"
        return 1
    fi

    git remote update

    UPSTREAM=${1:-'@{u}'}
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse "$UPSTREAM")
    BASE=$(git merge-base @ "$UPSTREAM")

    if [ $LOCAL = $REMOTE ]; then
        echo "Up-to-date"
    elif [ $LOCAL = $BASE ]; then
        echo "Need to pull"
        git pull
    elif [ $REMOTE = $BASE ]; then
        echo "Need to push"
        git push
    else
        echo "Diverged"
    fi

    return 0
}

function taskupd() {
    (_taskupd $@)
}
