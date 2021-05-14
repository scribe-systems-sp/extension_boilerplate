# Boilerplate scribe extension
You can use it as a starting point in creating scribe extension.

## Set up
First of all clone repository and submodules

```shell
git clone https://github.com/scribe-systems-sp/extension_boilerplate.git extension
cd extension
git submodule update --init --recursive
```

Check out `build.py` and set up variables
| Variable         | Default             | Description                                   |
| ---------------- |:-------------------:| ---------------------------------------------:|
| DIST_FOLDER      | ./dist              | Output folder                                 |
| BUILD_CONFIG     | ./build_config.json | Build configuration file                      |
| EXTENSION_CONFIG | ./config.json       | Extension configuration file                  |
| PUBLISH          | True                | Publish changes to the external Scribe server |
| URL              | http://localhost    | URL to the scribe server                      |
| USERNAME         | admin               | Admin username                                |
| PASSWORD         | admin123123         | Admin password                                |

Build extension and publish it (if PUBLISH is True)
```shell
./build.py
```

Your extension in `dist/extension.tar.gz`