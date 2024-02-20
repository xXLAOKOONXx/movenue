# Movenue

The MOVie VENUE for your home entertainment.

This is a full screen app to give you an easy access to your video libraries. There are different tabs for different porpuses, just go try them out.

The main selling point for MOVENUE over your ordinary media center options: Watch your videos in the 5.1 quality they deserve.

## Usage

### Visibility

**I develop this for my personal usage. So if you use the app please like the repository to show me there are more users than just me :D**

### Install

You can place the exe from the latest release wherever you like and start by executing the file.

On the first start you may not find anything within the app. You need to configure folders for the respective sections. For that select the settings in top right corner of the app. After adding a folder you need to restart the app.

The app uses metadata files for movies, series and shortfilm tab. For movies and series `nfo` files are required. For shortfilms `info.json` files are required.

### Create required Metadata

shortfilm metadata is expected as created by youtube-dl when using `--write-info-json` [link](https://github.com/ytdl-org/youtube-dl?tab=readme-ov-file#filesystem-options)

movies and series are expected as created by [media companion](https://sourceforge.net/projects/mediacompanion/)

Required:

- `.nfo` file for movie, series, episode

Optional:

- `<moviename>-poster.jpg` (movie), `poster.jpg` (series), `season<NO>-poster.jpg` (season), `<episode-file-name>.nfo` (episode)

For the **music** section I recommend using [MP3Tag](https://www.mp3tag.de/) to fill 'title' and 'artists'. It is really great for going through multiple files at the same time. But this tool does not offer an easy way to add tags or give the option to add multiple artists. For those cases check out this app itself or the notebooks under `useful_notebooks`.

### Suggestion Algorithm

The app works for movie, shortfilm and series with a scoring system to suggest media. The `algorithm` takes into account:

- recency of last watching
- personal scoring
- public scoring (if available)
- monthly, weekly and daily rng scoring

This might give you the feeling the app wants to force you to consume a specific media, similar to your favorite online platform. If you want to feel free to believe the app is smart enough to figure out how much you like a media content you have never seen and that it recommends it to you quite agressive for that vary reason.

### Files

The app uses AppData/local/movenue as a location for all files that might be needed, e.g. settings, caches.

You can find the logs there as well.

### OS Support

The app only supports windows. Other operating systems are not in my scope.

### Disclaimer

Please do not use this application for illegal activities. Pay attention to your local laws and stay safe ;)

### Further Details

You might find more details on functionalities in the [docs folder](./docs/README.md).

## Development

### Costum mp4 Tags

In case some costum tags are used for mp4 files, they will use `LAO` as group identifier. This enables me to reuse the tags in other projects.

### build exe

```bash
poetry run pyinstaller app.spec
```
