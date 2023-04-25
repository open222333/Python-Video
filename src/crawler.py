import os
from .logger import logger

def videoConvertToTs(video_path: str, output_video_dir: str, output_video_name: str, video_encoding: str, p: str) -> str:
    """影片轉檔成ts格式

    ffmpeg Documentation:
    https://ffmpeg.org/ffmpeg.html

    av1:
    https://trac.ffmpeg.org/wiki/Encode/AV1

    質量由 -crf 決定
    比特率限制由 -b:v 決定，其中比特率必須非零。
    -r

    Args:
        video_path (str): 目標影片路徑
        output_video_dir (str): 輸出資料夾路徑
        output_video_name (str): 檔名，不需要副檔名以及畫質
        video_encoding (str): h264, h265, av1
        p (str): 標清給240 高清給480

    Returns:
        str: 檔名
    """
    logger.info('=== videoConvertToTs start ===')
    encoding = ''

    if not os.path.exists(output_video_dir):
        os.mkdir(output_video_dir)

    if video_encoding == 'h264':
        encoding = 'libx264 -crf 23'
    elif video_encoding == 'h265':
        encoding = 'libx265 -crf 28 -tune fastdecode'
    elif video_encoding == 'av1':
        encoding = 'libaom-av1 -crf 30 --enable-libaom'
    else:
        return ''

    video_name = f'{output_video_name}-{p}.ts'

    if video_encoding in ['h264', 'h265']:
        '''
        -c[:stream_specifier] codec (input/output,per-stream)
            http://ffmpeg.org/ffmpeg-all.html#Stream-specifiers-1
        -b
            以比特/秒為單位設置比特率。設置此項會自動激活恆定比特率 (CBR) 模式。如果未指定此選項，則設置為 128kbps。
            Set bit rate in bits/s. Setting this automatically activates constant bit rate (CBR) mode. If this option is unspecified it is set to 128kbps.
        -r[:stream_specifier] fps (input/output,per-stream)
            Set frame rate (Hz value, fraction or abbreviation).
        -ar[:stream_specifier] freq (input/output,per-stream)
            Set the audio sampling frequency. For output streams it is set by default to the frequency of the corresponding input stream. For input streams this option only makes sense for audio grabbing devices and raw demuxers and is mapped to the corresponding demuxer options.
        -video_track_timescale
            Set the timescale used for video tracks. Range is 0 to INT_MAX. If set to 0, the timescale is automatically set based on the native stream time base. Default is 0.
        -vf filtergraph (output)
            Create the filtergraph specified by filtergraph and use it to filter the stream.

            This is an alias for -filter:v, see the -filter option.

        stream_specifier
        http://ffmpeg.org/ffmpeg-all.html#Stream-specifiers-1

        -filter option
        http://ffmpeg.org/ffmpeg-all.html#filter_005foption

        '''
        if p == '240':
            command = f'ffmpeg -i {video_path} -c:v {encoding} -c:a aac -b:a 192k -r 30 -ar 44100 -video_track_timescale 90000 -vf scale=-2:240 {output_video_dir}/{video_name} -y'
        elif p == '480':
            command = f'ffmpeg -i {video_path} -c:v {encoding} -c:a aac -b:a 192k -r 30 -ar 44100 -video_track_timescale 90000 -vf scale=-2:720 {output_video_dir}/{video_name} -y'
        else:
            return ''
    else:
        if p == '240':
            command = f'ffmpeg -i {video_path} -c:v {encoding} -c:a aac -b:a 192k -r 30 -ar 44100 -video_track_timescale 90000 -vf scale=-2:240 {output_video_dir}/{video_name} -y'
        elif p == '480':
            command = f'ffmpeg -i {video_path} -c:v {encoding} -c:a aac -b:a 192k -r 30 -ar 44100 -video_track_timescale 90000 -vf scale=-2:720 {output_video_dir}/{video_name} -y'
        else:
            return ''

    logger.debug(f'指令 {command}')
    os.system(command)

    logger.info('=== videoConvertToTs end ===')
    return video_name


def generateEnctyptionKey(key_dir, p):
    '''產生加密的key

    key_dir: key所在的資料夾路徑
    p: '240' or '480'

    key file 用 openssl 產生一個 16位元的 binary key
    key 產完之後 要上傳到 s3 (回傳key file, 請呼叫端自己上傳)
    '''

    logger.info('=== generateEnctyptionKey start ===')

    key_name = f'key_{p}.key'
    command = f'openssl rand 16 > {key_dir}/{key_name}'
    logger.debug(f'指令 {command}')
    os.system(command)
    logger.info('=== generateEnctyptionKey end ===')
    return key_name


def generateEnctyptionKeyInfo(http_url_of_key: str, key_path_in_loacl: str, keyinfo_dir: str, p: str) -> str:
    """產生加密m3u8時需要的keyinfo
    key info format
    key URI        = http_url_of_key
    key file path  = key_path_in_loacl
    IV (optional)

    Args:
        http_url_of_key (str): 必須是 http 形式的
        key_path_in_loacl (str): _description_
        keyinfo_dir (str): _description_
        p (str): '240' or '480'

    Returns:
        str: _description_
    """
    logger.info('=== generateEnctyptionKeyInfo start ===')
    keyinfo = f'key_{p}.keyinfo'
    iv = os.popen('openssl rand -hex 16').read()
    data = f'{http_url_of_key}\n{key_path_in_loacl}\n{iv}'
    with open(f'{keyinfo_dir}/{keyinfo}', 'w') as k:
        k.write(data)
    logger.info('=== generateEnctyptionKeyInfo end ===')
    return keyinfo


def videoConvertToEncryptedM3U8(video_path: str, keyinfo_path: str, output_video_dir: str, output_video_name: str):
    """影片轉成加密的m3u8
    Args:
        video_path (str): _description_
        keyinfo_path (str): _description_
        output_video_dir (str): _description_
        output_video_name (str): _description_
    """
    logger.info('=== videoConvertToM3U8 start ===')
    if not os.path.exists(output_video_dir):
        os.mkdir(output_video_dir)

    command = f'ffmpeg -i {video_path} -c copy -hls_segment_type mpegts -hls_time 10 -start_number 1 -hls_key_info_file {keyinfo_path} -hls_segment_filename {output_video_dir}/{output_video_name}_%05d.ts -hls_list_size 0 -hls_playlist_type vod -hls_flags delete_segments+split_by_time {output_video_dir}/{output_video_name}.m3u8 -y'
    os.system(command)
    logger.info('=== videoConvertToM3U8 end ===')
