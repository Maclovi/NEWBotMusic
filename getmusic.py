from pytube import YouTube
import io


class LimitSizeError(Exception):

    def __init__(self, message: str = "Размер файла превышает 50мб.") -> None:
        super().__init__(message)


class YouTubeMusic:

    def __init__(self, url: str):
        try:
            self.yt: object = YouTube(url)  # Экземпляр объекта YouTube 
            self.audio = self.yt.streams.get_audio_only()
            if self.audio.filesize_mb > 50:
                raise LimitSizeError
            self.response_valid = True
        except Exception as error:
            self.response_valid = error    
        else:
            self.views: int = self.yt.views  # Просмотры
            self.pub: int = self.yt.publish_date.year   # Год публикации
            self.thumb: str = self.yt.thumbnail_url  # Заглавная картинка
            self.title: str = self.yt.title  # Название песни

            del self.yt

    
    def get_music(self):
        with io.BytesIO() as output:
            self.audio.stream_to_buffer(output)

            return output.getvalue()
