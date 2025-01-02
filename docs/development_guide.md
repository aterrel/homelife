# Development Guide

## Development environment

Mac is a pretty typical environment for developing and this project is largely developed using a mac.

### Installing postgres on mac

The homebrew install of mac works pretty well for development but there can often be problems along the way. Using Homebrew here is a quick guide of how the install went.

```bash
$ brew update
$ brew doctor
$ brew install postgresql@16
$ brew services start postgresql@16
$ echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
$ psql
```

If you get an error connecting to the tmp file it might be worth your time to uninstall everything and make sure there is no other postgres on your system. For example to remove postgres@14 would be something like:

```bash
$ brew remove --force postgresql
$ brew remove --force postgresql@14
$ rm -rf /usr/local/var/postgres/
$ rm -rf /usr/local/var/postgresql@14/
# for Apple Silicon might need
# rm -rf /opt/homebrew/var/postgres
# rm -rf /opt/homebrew/var/postgresql@14
```
