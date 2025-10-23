# Video Game!!! (Maybe)

## How the Game Works
We'll describe the game here

## Structure
```
backend/
|- app/                -- bundles db and game-logic together to define the routes accessed by the frontend
|  |- __init__.py
|  |- app.py
|- db/                 -- contains all db DDL and DML
|  |- __init__.py
|  |- db.py
|- game-logic/         -- contains all game logic
|  |- __init__.py
|  |- game.py
|- main.py             -- backend application entry point
frontend/
|- public/             -- contains all publicly accessible assets (png, svg, jpeg, mp3, ...)
|  |- vite.svg         -- WILL BE REMOVED
|- src/
|  |- App.module.css   -- main styling for App.tsx component
|  |- App.tsx          -- top level JSX (HTML-like) component
|  |- main.tsx         -- frontend application entry point
|- eslint.config.js    -- --------------------------------
|- index.html          -- ################################
|- package-lock.json   -- ################################
|- tsconfig.app.json   -- these are pregenerated files that define a react project. We will ALMOST never mess with these.
|- tsconfig.json       -- ################################
|- tsconfig.node.json  -- ################################
|- vite.config.ts      -- --------------------------------
.env                   -- List of environment variables, you will need to create your own. The point is to keep keys out of VC.
.gitignore             -- top level .gitignore, there are some of these in sub-directories.
package-lock.json
README.md          -- you are here
run.sh             -- bash script that start the frontend and backend simultaneously. Just run this 99% of the time.
```

Regardless of what the game or application ends up being, this should be a really powerful tech-stack for us to follow.


## DB Design

We need to include some information about the ER model, Schemas, and other implementation features of our databse. We'll put those details here.

### Authors:
 - **Kyle Dobson**
 - **Ryley Turner**