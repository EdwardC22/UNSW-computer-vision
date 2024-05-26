# Frontend Setup
## Requirements to Build
Project requires Node >= 14.0.0 and npm >= 5.6.

Commands likely need to be prefixed with sudo.

First ensure package manager is upto date.

```bash
sudo apt-get update && sudo apt-get upgrade
```

Then, install the node package manager npm (might need to install node first not sure will figure out)

```bash
sudo apt install npm

```

Then, use npm to install the javascript runtime nodejs,
and force node to use the most recent version available.

```bash
npm install n -g
sudo n latest
```

## Running the Web Server
```
npm install
```

This installs all the dependencies for the react app

To the start the development server run:

```
npm start
```

By default this opens the server on localhost:3000.

### Building 

To create production files that can be run in a web browser run:
```
npm run build
```
This writes the files to the build folder which can be served.
