# Application Setup

```shell
conda env create -n <ENVIRONMENT NAME> -f conda.yaml
conda activate <ENVIRONMENT NAME>
python index.py
```

The output of the last command should look similar to the output below:
```output
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

After running these commands, you will need to open the web app on the local host chosen by Dash.
