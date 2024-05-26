# Backend Setup

Once the backend requirements have been installed by running the backend_setup.sh
script in the root directory, to subsequently run the backend all that needs to be
done is to activate the virtual environment:

```bash
source env/bin/activate
```

Then, ensure the environment variables are set:

```bash
source ../config.sh

```

Then, run flask:

```bash
flask run
```
