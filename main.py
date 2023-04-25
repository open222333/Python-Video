from src.timer import Timer
from src.logger import Log
from src.crawler import videoConvertToTs, videoConvertToEncryptedM3U8, generateEnctyptionKey, generateEnctyptionKeyInfo
from src import NGS_AVDATA_HOST, LOG_LEVEL

from argparse import ArgumentParser
import os

video_log = Log('main_result')
video_log.set_level(LOG_LEVEL)
video_log.set_file_handler()
video_log.set_msg_handler()

parser = ArgumentParser()
parser.add_argument('-p', '--path', help='影片位置')
parser.add_argument('-o', '--output', help='輸出位置')

# 從命令列讀取參數
args = parser.parse_args()

origin_size = os.path.getsize(args.path)

timer = Timer()

try:
    # 轉換成av1
    timer.set_name('轉換成av1')
    timer.start()
    av1_video_name = videoConvertToTs(
        video_path=args.path,
        output_video_dir=args.output,
        output_video_name='test-av1',
        video_encoding='av1',
        p='480'
    )
    timer.stop()
    av1_size = os.path.getsize(f"{args.output}/{av1_video_name}")
    msg = f'原檔案大小: {origin_size}\n轉換後檔案大小: {av1_size}\n{timer.get_result()}'
    video_log.info(msg)

    # # 轉換成m3u8
    # timer.set_name('av1轉換成m3u8')
    # timer.start()
    # generateEnctyptionKey(args.output, 'av1_480')
    # generateEnctyptionKeyInfo(
    #     http_url_of_key=f'{NGS_AVDATA_HOST}/test/key_av1_480.key',
    #     key_path_in_loacl=f'{args.output}/key_av1_480.key',
    #     keyinfo_dir=args.output,
    #     p='av1_480'
    # )
    # videoConvertToEncryptedM3U8(
    #     video_path=f'{args.output}/{av1_video_name}',
    #     keyinfo_path=f'{args.output}/key_av1_480.key',
    #     output_video_dir=args.output,
    #     output_video_name='test-av1-m3u8'
    # )
    # timer.stop()
    # video_log.info(timer.get_result())


    # # 轉換成ts-h264
    # timer.set_name('轉換成ts-h264')
    # timer.start()
    # h264_video_name = videoConvertToTs(
    #     video_path=args.path,
    #     output_video_dir=args.output,
    #     output_video_name='test-h264',
    #     video_encoding='h264',
    #     p='480'
    # )
    # timer.stop()
    # h264_size = os.path.getsize(f"{args.output}/{av1_video_name}")
    # msg = f'原檔案大小: {origin_size}\n轉換後檔案大小: {h264_size}\n{timer.get_result()}'
    # video_log.info(msg)

    # # 轉換成m3u8
    # timer.set_name('h264轉換成m3u8')
    # timer.start()
    # generateEnctyptionKey(args.output, 'h264_480')
    # generateEnctyptionKeyInfo(
    #     http_url_of_key=f'{NGS_AVDATA_HOST}/test/key_h264_480.key',
    #     key_path_in_loacl=f'{args.output}/key_h264_480.key',
    #     keyinfo_dir=args.output,
    #     p='h264_480'
    # )
    # videoConvertToEncryptedM3U8(
    #     video_path=f'{args.output}/{h264_video_name}',
    #     keyinfo_path=f'{args.output}/key_h264_480.key',
    #     output_video_dir=args.output,
    #     output_video_name='test-h264-m3u8'
    # )
    # timer.stop()
    # video_log.info(timer.get_result())
except Exception as err:
    video_log.error(err, exc_info=True)
