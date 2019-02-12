# Taskwarrior-hooks-collection

My personal hook collection for the Taskwarrior task manager hero.

## Hooks list

|Title|Triggers|Result|
|-----|--------|------|
|__buy_wait__|add, modify|If project is `Buy` or it's subproject, then places task in waiting list (set `wait:someday`)
|__remove_next__|start, done|Removes task from waiting list (set `wait:someday`) and removes `next` tag
|__commit__|exit|Commits all changes in the `.task` directory if it's a git repository|

## Misc

`taskupd.sh` contains function for updating `.task` repository.