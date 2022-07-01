# About contributions to RouC

This project is **opensource** and opened for any contributions from you. Here you can read, how you can help us.

## Reporting a Vulnerabilities/Bugs or suggesting any new features

If you have found any vulnerability in any version of bot, please, create an issue in [Issues tab](https://github.com/EgorBron/RouC/issues). This place also for you, if you want to suggest something new to RouC.

## Contributing to bot translations

RouC supports multiple languages. You can help translate bot to your language on our [SimpleTranslate](https://simpletranslate.herokuapp.com/rouc) page. English and Russian are ready, no need to translate into them (but you can suggest corrections).

## Contributing to sources of bot

Feel free to create forks/PRs with improvements.

#### Just follow this:

*Recommended to read before continuing: [Dive into sources](https://github.com/EgorBron/RouC/blob/master/dive_into_sources.md)*

0. Check if you have theese requirements:

* Python from 3.9.0 to 3.9.6
* Local MongoDB v4 and above
* All libraries from `requirements.txt`
* Working Git (any version)
* Data to test bot (not required): Discord bot token, Tenor API token

1. Create a fork
2. Clone your fork:

```sh
git clone https://github.com/You/YourForkRepo.git
```

3. Do your incredible work

3.1. [optional] Set `rouctoken` enviroment variable with your test data (see [Enviroment](https://github.com/EgorBron/RouC/blob/master/dive_into_sources.md#enviroment-variables)), configure database (see [Setup DB](https://github.com/EgorBron/RouC/blob/master/dive_into_sources.md#setup-database)) and check if everyting works

4. Commit:

```sh
git checkout -b BranchWithChanges # needed once
git comit -m "Commit description"
git push origin BranchWithChanges
```

5. Open a pull request with comparsion between your branch with improvements and [`alpha`](https://github.com/EgorBron/RouC/tree/alpha) version branch. 

> **NOTE:** compare only with [`alpha`](https://github.com/EgorBron/RouC/tree/alpha) branch in original repo!

> **NOTE #2:** please use only recommended versions of Python, current database and libraries.