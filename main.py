def get_audio_from_video(video_path, output_file):
    from moviepy.editor import VideoFileClip
    # 加载MP4文件
    video = VideoFileClip(video_path)
    # 提取音频流
    audio = video.audio
    # 提取视频流
    audio.write_audiofile(output_file)  # 输出为MP3格式，你可以根据需要更改格式


def clip_audio(audio_path, start_time, end_time, out_file='output'):
    # 注意起始和终止时间都是秒
    from moviepy.editor import AudioFileClip
    # 加载音频文件
    audio = AudioFileClip(audio_path)
    cut_audio = audio.subclip(start_time, end_time)
    # 保存切割后的音频文件
    cut_audio.write_audiofile(f"{out_file}.mp3")


if __name__ == '__main__':
    clip_audio("output_audio.mp3", 0.5, 0.75)
