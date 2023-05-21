from pytube import YouTube
import io


class LimitSizeError(Exception):
    def __init__(self, message: str = "Размер файла превышает 50мб.") -> None:
		    super().__init__(message)


class YouTubeMusic:
  
    def __init__(self, url: str = "https://youtu.be/GCdwKhTtNNw"):
    	  # Экземпляр объекта YouTube
    	  self.yt: object = YouTube(url)

    	  self.views: int = self.yt.views  # Просмотры
    	  self.pub: int = self.yt.publish_date.year  # Год публикации
    	  self.thumb: str = self.yt.thumbnail_url  # Заглавная картинка
    	  self.title: str = self.yt.title  # Название песни

    	  self.audio = self.yt.streams.get_audio_only()  # Берёт itag 140

    def check(self) -> bool | str:
  	    try:
  		      self.yt.check_availability()
            if self.audio.filesize_mb > 50:
        	      raise LimitSizeError
      	return True

    except Exception as error:
        return error

    def get_music(self):
        with io.BytesIO() as output:
            self.audio.stream_to_buffer(output)

            return output.getvalue()
