

from ..extractor.common import InfoExtractor


class EbaumsWorldIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?ebaumsworld\.com/(?:media|videos)/[^/]+/(?P<id>\d+)'
    _TEST = {
        'url': 'http://www.ebaumsworld.com/video/watch/83367677/',
        'info_dict': {
            'id': '83367677',
            'ext': 'mp4',
            'title': 'A Giant Python Opens The Door',
            'description': 'This is how nightmares start...',
            'uploader': 'jihadpizza',
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        config = self._download_xml(
            'http://www.ebaumsworld.com/video/player/%s' % video_id, video_id)
        video_url = config.find('file').text
        if video_url.find('youtube.com') != -1:
            return self.url_result(video_url, 'Youtube')
        return {
            'id': video_id,
            'title': config.find('title').text,
            'url': video_url,
            'description': config.find('description').text,
            'thumbnail': config.find('image').text,
            'uploader': config.find('username').text,
        }
