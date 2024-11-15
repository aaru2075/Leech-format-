class LinkGenerator:
    def __init__(self, base_url, start_number, end_number, anime_manga_name, content_type, custom_prefix=None, custom_extension=None, season_number=None, filename_number=None):
        self.base_url = base_url
        self.start_number = start_number
        self.end_number = end_number
        self.anime_manga_name = anime_manga_name
        self.content_type = content_type
        self.custom_prefix = custom_prefix
        self.custom_extension = custom_extension
        self.season_number = season_number
        self.filename_number = filename_number

    def generate_links(self):
        download_links = []
        file_extension = {
            'manga': '@Manga_Campus.pdf',
            'anime': '1080p [Dual] @Anime_Campus.mkv',
            'hindi': '720p [Dual] @Anime_Campus.mkv'
        }
        prefix = {
            'manga': '[MC]',
            'anime': '[AC]',
            'hindi': '[MC]'
        }

        for number in range(self.start_number, self.end_number + 1):
            download_link = f"{self.base_url}/{number}"
            filename = self.create_filename(download_link, file_extension, prefix, number)
            download_links.append(filename)
            self.filename_number += 1  # Increment filename number after each iteration
        
        return download_links

    def create_filename(self, download_link, file_extension, prefix, number):
        if self.content_type == 'custom':
            return f"{download_link} -n {self.custom_prefix} [{self.filename_number:03d}] {self.anime_manga_name} {self.custom_extension}"
        elif self.content_type in ['anime', 'hindi']:
            return f"{download_link} -n  {self.anime_manga_name} [S{self.season_number:01d} E{self.filename_number:02d}] {file_extension[self.content_type]}"
        else:
            return f"{download_link} -n {prefix[self.content_type]} [{self.filename_number:01d}] {self.anime_manga_name} {file_extension[self.content_type]}"
