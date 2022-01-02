# Hextris pour YunoHost

[![Niveau d'intégration](https://dash.yunohost.org/integration/hextris.svg)](https://dash.yunohost.org/appci/app/hextris) ![](https://ci-apps.yunohost.org/ci/badges/hextris.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/hextris.maintain.svg)  
[![Installer Hextris avec YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=hextris)

*[Read this readme in english.](./README.md)*
*[Lire ce readme en français.](./README_fr.md)*

> *Ce package vous permet d'installer Hextris rapidement et simplement sur un serveur YunoHost.
Si vous n'avez pas YunoHost, regardez [ici](https://yunohost.org/#/install) pour savoir comment l'installer et en profiter.*

## Vue d'ensemble

Rotate the Hexagon to prevent the blocks from stacking outside the outer grey hexagon!

HEXTRIS is a fast paced puzzle game inspired by Tetris. Blocks start on the edges of the screen, and fall towards the inner blue hexagon. The objective of the game is to prevent the blocks from stacking outside the area of the grey hexagon. To do this, you must rotate the hexagon to manage different stacks of blocks on each face. Aim to connect 3 or more blocks of the same color: when 3 or more blocks of the same color touch each other, they are destroyed, and the blocks above them slide down! Destroying multiple series of blocks grants combos, whose durations are indicated by a quickly receding outline around the outer, grey hexagon. You lose once blocks on a face of the hexagon stack outside of the outer hexagon!

**Version incluse :** 2020-05-05~ynh4

**Démo :** https://hextris.io/

## Captures d'écran

![](./doc/screenshots/screenshot.jpg)

## Documentations et ressources

* Site officiel de l'app : http://hextris.github.io/
* Dépôt de code officiel de l'app : https://github.com/Hextris/Hextris
* Documentation YunoHost pour cette app : https://yunohost.org/app_hextris
* Signaler un bug : https://github.com/YunoHost-Apps/hextris_ynh/issues

## Informations pour les développeurs

Merci de faire vos pull request sur la [branche testing](https://github.com/YunoHost-Apps/hextris_ynh/tree/testing).

Pour essayer la branche testing, procédez comme suit.
```
sudo yunohost app install https://github.com/YunoHost-Apps/hextris_ynh/tree/testing --debug
ou
sudo yunohost app upgrade hextris -u https://github.com/YunoHost-Apps/hextris_ynh/tree/testing --debug
```

**Plus d'infos sur le packaging d'applications :** https://yunohost.org/packaging_apps