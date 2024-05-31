# Page Settings

For each "page" or "tab" in this app you need to create some settings for it.

## In-App Configuration

Within the app you can find all configurations in the top right corner.

On the settings page you can see all pages and there configuration.

## In-File Configuration

Some configuration options might not be supported by the In-App Configuration yet.
For those options you can go into `USER/AppData/Local/movenue/category_settings.json` and add your prefered options.
I highly recommend to start with an In-App Configuration and edit in json afterwards.

Those options are most likely located in the dict behind `key_word_args`.

## Keywords

### Category Page

- `add_recent_category` (bool): Set this value to true to have a row with the ten most recently consumed items on top of the page.
  You might want to add this configuration on a page for your series (to continue watching your favorite show).

- `add_random_category` (bool): Set this value to true to have a row with 50 random items on the top of the page.
  This row gets a new random selection on the start of a new day or when you refresh the page.
