# Twitter Analyzer

> Prototype project for 365Talents

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![CircleCI](https://img.shields.io/circleci/build/github/yoyonel/365talents_twitter_analyzer/develop.svg?token=885581712496df0fba04b76a04b1f6284cba5fb4)](https://circleci.com/gh/yoyonel/365talents_twitter_analyzer/tree/develop)
[![Actions Status](https://github.com/yoyonel/365talents_twitter_analyzer/workflows/Python%20package/badge.svg)](https://github.com/yoyonel/365talents_twitter_analyzer/actions)
<!-- [![Build Status](https://travis-ci.com/yoyonel/forcity_trasherbot.svg?branch=master)](https://travis-ci.com/yoyonel/forcity_trasherbot) -->

Tu développeras un programme Python qui permet de répondre à ces trois questions :
- qui sont les utilisateurs les plus présents sur une timeline Twitter ?
- quel est le sentiment général des tweets (positif ou négatif) d’un utilisateur ?
- à partir du texte d’un tweet, est-il possible de deviner la langue dans lequel le 
tweet a été rédigé ?
 
Tu peux te connecter à l'API Twitter, 
ou utiliser ce petit fichier que tu peux utiliser comme base de tests : [http://bit.ly/365t-data-tweets](http://bit.ly/365t-data-tweets)


## Instructions

Structure is based on [this article](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure). Source code can be found in the `src` folder, and tests in the `tests` folder.

### Installation

To install the package (development mode):

```bash
➤ pip install -e ".[develop]"
```

### Tests

#### Tox
We use `tox` for the tests. This ensure a clear separation between the development environment and the test environment.
To launch the tests, run the `tox` command:

It first starts with a bunch of checks (`flask8` and others) and then launch the tests using python 3.

#### Pytest
You can use `pytest` for the tests:
```bash
➤ pytest
```
