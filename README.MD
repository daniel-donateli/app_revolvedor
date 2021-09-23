# Running
1. Clone repo
2. Install dependencies
```sh 
poetry install
```
3. Rename .env-example to .env and set config vars
4. Activate virtual env
```sh 
poetry shell
```
5. Set Environment Variables
    - Windows:
    ```sh 
    set FLASK_APP=app_revolvedor
    set FLASK_ENV=development
    ```
    - Linux:
    ```sh 
    export FLASK_APP=app_revolvedor
    export FLASK_ENV=development
    ```
6. Run
```sh 
flask run
```