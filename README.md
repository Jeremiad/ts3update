# ts3update

## Script for updating and downloading Team Speak 3 server

### Requirements
* Python 3.5
* cfscrape
* lxml

### OS Support
* Windows
* Linux
* MacOs

### Usage

````
git clone https://github.com/Jeremiad/ts3update.git ~/ts3update
````

Create symlink for script where your Team Speak server Directory is located

````
ln -s ~/ts3update/ts3update/ts3update.py .
````

Example file structure:
````
$ ls
teamspeak3-server_linux_amd64  ts3update.py
````

To update / download Team Speak
````
$ python ts3update.py
````