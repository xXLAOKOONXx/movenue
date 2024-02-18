from datetime import date
import os
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET

class Episode(object):
    EPISODE_WIDTH = 300
    EPISODE_HEIGHT = 200
    def __init__(self, nfo_path, tvshow_nfo_path):
        self.nfo_path = nfo_path
        self.tvshow_nfo_path = tvshow_nfo_path
        try:
            xml_tree = ET.parse(self.nfo_path)
        except Exception as e:
            print(f'Error interpreting {self.nfo_path}')
            raise e
        self.xml_tree = xml_tree
        xml_root = xml_tree.getroot()

        self.episode_no = int(xml_root.find('episode').text)
        self.season_no = int(xml_root.find('season').text)
        self.title = xml_root.find('title').text
        self.poster_url = f'''{'.'.join(self.nfo_path.split('.')[0:-1])}-thumb.jpg'''
        self.video_url = f'''{'.'.join(self.nfo_path.split('.')[0:-1])}.mp4'''.replace('/','\\')
        self.playcount = int(xml_root.find('playcount').text) if xml_root.find('playcount') is not None else 0

    @property
    def poster_image(self):
        try:
            if not hasattr(self, '_poster_image'):
                self._poster_image = ImageTk.PhotoImage(Image.open(self.poster_url).resize((self.EPISODE_WIDTH, self.EPISODE_HEIGHT)))
            return self._poster_image
        except Exception:
            return None
        

    def play_episode(self):
        xml_root = self.xml_tree.getroot()

        last_played = xml_root.find('lastplayed')
        if last_played is None:
            last_played = ET.SubElement(xml_root, 'lastplayed')
        last_played.text = str(date.today())
        
        play_count = xml_root.find('playcount')
        if play_count is None:
            play_count = ET.SubElement(xml_root, 'playcount')
        play_count.text = str(int(play_count.text or 0) + 1)
        self.playcount = play_count.text

        self.xml_tree.write(self.nfo_path)

        # update tvshow
        try:
            xml_tree = ET.parse(self.tvshow_nfo_path)
        except Exception as e:
            print(f'Error interpreting {self.tvshow_nfo_path}')
            raise e
        xml_root = xml_tree.getroot()

        last_played = xml_root.find('lastplayed')
        if last_played is None:
            last_played = ET.SubElement(xml_root, 'lastplayed')
        last_played.text = str(date.today())

        xml_tree.write(self.tvshow_nfo_path)

        os.startfile(self.video_url)