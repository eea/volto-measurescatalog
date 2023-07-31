# volto-measurescatalog

[![Releases](https://img.shields.io/github/v/release/eea/volto-measurescatalog)](https://github.com/eea/volto-measurescatalog/releases)

[![Pipeline](https://ci.eionet.europa.eu/buildStatus/icon?job=volto-addons%2Fvolto-measurescatalog%2Fmaster&subject=master)](https://ci.eionet.europa.eu/view/Github/job/volto-addons/job/volto-measurescatalog/job/master/display/redirect)
[![Lines of Code](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-master&metric=ncloc)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-master)
[![Coverage](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-master&metric=coverage)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-master)
[![Bugs](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-master&metric=bugs)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-master)
[![Duplicated Lines (%)](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-master&metric=duplicated_lines_density)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-master)

[![Pipeline](https://ci.eionet.europa.eu/buildStatus/icon?job=volto-addons%2Fvolto-measurescatalog%2Fdevelop&subject=develop)](https://ci.eionet.europa.eu/view/Github/job/volto-addons/job/volto-measurescatalog/job/develop/display/redirect)
[![Lines of Code](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-develop&metric=ncloc)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-develop)
[![Coverage](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-develop&metric=coverage)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-develop)
[![Bugs](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-develop&metric=bugs)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-develop)
[![Duplicated Lines (%)](https://sonarqube.eea.europa.eu/api/project_badges/measure?project=volto-measurescatalog-develop&metric=duplicated_lines_density)](https://sonarqube.eea.europa.eu/dashboard?id=volto-measurescatalog-develop)

Catalogue of Measures search [Volto](https://github.com/plone/volto) add-on for WISE Marine

## Features

Demo GIF

## Getting started

### Try volto-measurescatalog with Docker

1. Get the latest Docker images

   ```
   docker pull plone
   docker pull plone/volto
   ```

1. Start Plone backend

   ```
   docker run -d --name plone -p 8080:8080 -e SITE=Plone -e PROFILES="profile-plone.restapi:blocks" plone
   ```

1. Start Volto frontend

   ```
   docker run -it --rm -p 3000:3000 --link plone -e ADDONS="@eeacms/volto-measurescatalog" plone/volto
   ```

1. Go to http://localhost:3000

### Add volto-measurescatalog to your Volto project

1. Make sure you have a [Plone backend](https://plone.org/download) up-and-running at http://localhost:8080/Plone

   ```Bash
   docker compose up backend
   ```

1. Start Volto frontend

- If you already have a volto project, just update `package.json`:

  ```JSON
  "addons": [
      "@eeacms/volto-measurescatalog"
  ],

  "dependencies": {
      "@eeacms/volto-measurescatalog": "^1.0.0"
  }
  ```

- If not, create one:

  ```
  npm install -g yo @plone/generator-volto
  yo @plone/volto my-volto-project --addon @eeacms/volto-measurescatalog
  cd my-volto-project
  ```

1. Install new add-ons and restart Volto:

   ```
   yarn
   yarn start
   ```

1. Go to http://localhost:3000

1. Happy editing!

## Release

See [RELEASE.md](https://github.com/eea/volto-addon-template/blob/master/RELEASE.md).

## How to contribute

See [DEVELOP.md](https://github.com/eea/volto-measurescatalog/blob/master/DEVELOP.md).

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

See [LICENSE.md](https://github.com/eea/volto-measurescatalog/blob/master/LICENSE.md) for details.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
