# Bot2

A discord bot made with [interactions.py](https://github.com/interactions-py/interactions.py).
Visit [the official website](https://interactions-py.github.io/interactions.py/) to get started.

## Development installation

<details>
<summary>Click to expand</summary>

### Mongodb

You can either use a local mongodb instance or use mongodb atlas.

#### Local

1. Install mongodb on your machine ([Windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/),
   [Mac](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/),
   [Linux](https://docs.mongodb.com/manual/administration/install-on-linux/))
2. Create a database called `bot2`

### Python

0. Clone this repository and, if needed, check out the appropriate feature branch.

0.1. You will need your own Discord bot account with a token. See [here](https://interactions-py.github.io/interactions.py/Guides/02%20Creating%20Your%20Bot/).


1. Create a virtual environment

2. Install packages using either poetry or pip `poetry install` or `pip install -r requirements.txt`

3. Change the name of `src/example_config.py` to `src/config.py` and fill in the required fields (Mandatory fields
   below)
    - DEV_GUILD_ID
    - DEV_CHANNEL_ID
    - DEV_USER_ID
    - MONGO_MODE (see below)
      
4. Change the name of `.env.example` to `.env` and fill in the required fields (Mandatory fields below)
    - PROJECT_NAME
    - DISCORD_TOKEN
    - MONGO_LOCAL_URI or MONGO_URI and MONGO_CERT_PATH (see below)

5. [Option 1] If you want to use mongo db locally.

    - Set MONGO_LOCAL_URI in `.env`. (Add db name at the end example: `mongodb://localhost:27017/DATABASE_NAME`)
    - Set MONGO_MODE = 'localhost' in `src/config.py`.

5. [Option 2] If you want to use mongodb atlas
    - Set in `.env`:
        - MONGO_URI (Add db name at the end
          example: `mongodb+srv://<cluster-url>/DATABASE_NAME?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority`)
        - MONGO_CERT_PATH
    - Set in `src/config.py`:
        - MONGO_MODE = "atlas" (from localhost to atlas)

6. Start the bot. Be in the repository root directory.

```bash
python src/main.py
```

</details>

# Additional Information

Additionally, this comes with a pre-made [pre-commit](https://pre-commit.com) config to keep your code clean.

It is recommended that you set this up by running:

```bash
pip install pre-commit
```

```bash
pre-commit install
```

---

# Todo

- [ ] Birthday Event extension
- [x] Add Mongo DB for persistence
- [ ] Meeting Scheduler
- [ ] create event while creating the object
