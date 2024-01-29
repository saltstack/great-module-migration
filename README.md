This repository contains the lists of modules (as well as states, runners, engines, etc) which will get removed from Salt.

A file can fall into one of three categories.

1. Files that are core to Salt and will remain in the Salt codebase
2. Files that will be moved out of the Salt codebase but continue to be maintained by the Salt Core Team
3. Files that will be moved out into a dump repository and will no longer be maintained by the Salt Core Team
4. Files which serve no purpose on Salt's runtime, for example, test related files, which can and should be created when
   running the test suite, if need be.

We'll use `git filter-repo` to migrate modules to a separate repositoy while
retaining their git history. Once the migration has taken place, we'll do a
`git rm` against the main salt repository.


Install filter-repo (Debian)
```
sudo apt-get install -y git-filter-repo
```

Now make a fresh clone and run filter repo. Starting in the root of this repository.

```
FILESDIR=$(pwd)
cd /tmp
git clone git@github.com:saltstack/salt.git community-extensions
cd community-extensions
git filter-repo --dry --paths-from-file=$FILESDIR/community-ext-modules.txt
```

If eveything looks good... Send it!

```
git filter-repo --paths-from-file=$FILESDIR/community-ext-modules.txt
```

Now we can remove the migrated files from the salt repo.

```
cd ~/src/salt
git rm -- $(cat $FILESDIR/core-ext-modules.txt)
git commit -m 'Removing core extension modules'
```
