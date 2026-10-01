## GIT

# The loop
git status                  # what changed
git add ASS01/              # stage (or: git add . for everything)
git commit -m "message"
git push

# Extras
git pull                    # get teammate's changes (do before you push)
git diff                    # see unstaged changes
git diff --staged           # see what the next commit contains
git show                    # see what the last commit changed
git log --oneline           # commit history
git restore file.py         # discard uncommitted changes to a file
git restore --staged file.py   # unstage a file
git switch -c yourname/fft  # new branch
git switch main             # back to main
git merge yourname/fft      # merge a branch into main (run while on main)

# Rebase
git switch yourname/fft
git fetch
git rebase origin/main
git add file.py             # after fixing a conflict
git rebase --continue
git rebase --abort          # bail out

