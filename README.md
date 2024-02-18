# Laoflix

## Usage

### Visibility

**I develop this for my personal usage. So if you use the app please like the repository to show me there are more users than just me :D**

### About

This app is a full screen app to have a nice overview over your video libraries.

Only windows is supported and in scope.

### Install

You can place the exe from the latest release wherever you like and start by executing the file.

On the first start you may not find anything within the app. You need to configure folders for the respective sections. For that select the settings in top right corner of the app. After adding a folder you need to restart the app.

The app uses metadata files for movies, series and youtube tab. For movies and series `nfo` files are required. For youtubes `info.json` files are required.

### Create required Metadata

youtube metadata is expected as created by youtube-dl when using `--write-info-json` [link](https://github.com/ytdl-org/youtube-dl?tab=readme-ov-file#filesystem-options)

movies and series are expected as created by [media companion](https://sourceforge.net/projects/mediacompanion/)

### Files

The app uses AppData/local/laoflix as a location for all files that might be needed.

You can find the logs there as well.

## Development

### build exe

```bash
poetry run pyinstaller app.spec
```
