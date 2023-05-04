from src.timer import Timer
from src.logger import Log
from src.crawler import videoConvertToTs, videoConvertToEncryptedM3U8, generateEnctyptionKey, generateEnctyptionKeyInfo, removeM3U8KeyHost
from src.tool import human_readable_size
from src import NGS_AVDATA_HOST, LOG_LEVEL

from argparse import ArgumentParser
import os

video_log = Log('main_result')
video_log.set_level(LOG_LEVEL)
video_log.set_log_formatter('%(asctime)s %(levelname)s - %(message)s')
video_log.set_file_handler()
video_log.set_msg_handler()

parser = ArgumentParser()
parser.add_argument('-p', '--path', help='影片位置')
parser.add_argument('-o', '--output', help='輸出位置')
parser.add_argument('-t', '--type', help='轉換類型 av1, h264 預設all', default='all')
parser.add_argument('--onlymessage', help='只顯示訊息(測試用)', action='store_true')
parser.add_argument('--convert_video', help='影片轉檔', action='store_true')
parser.add_argument('--convert_m3u8', help='m3u8測試', action='store_true')

# 從命令列讀取參數
args = parser.parse_args()

origin_size = os.path.getsize(args.path)

timer = Timer()

try:
    if args.convert_video:
        if args.type == 'all' or args.type == 'h264':
            # 轉換成ts-h264
            timer.set_name('轉換成h264')
            timer.start()
            h264_video_name = videoConvertToTs(
                video_path=args.path,
                output_video_dir=args.output,
                output_video_name='test-h264',
                video_encoding='h264',
                p='480',
                test=args.onlymessage
            )
            timer.stop()
            if args.onlymessage:
                h264_size = 0
            else:
                h264_size = os.path.getsize(f"{args.output}/{h264_video_name}")
            msg = f'\n{timer.name} 轉換結果:\n原檔案路徑: {args.path}\n原檔案大小: {human_readable_size(origin_size)}\n轉換後檔案大小: {human_readable_size(h264_size)}\n{timer.get_result()}\n'
            video_log.info(msg)

        if args.type == 'all' or args.type == 'av1':
            # 轉換成av1
            timer.set_name('轉換成av1')
            timer.start()
            av1_video_name = videoConvertToTs(
                video_path=args.path,
                output_video_dir=args.output,
                output_video_name='test-av1',
                video_encoding='av1',
                p='480',
                test=args.onlymessage
            )
            timer.stop()
            if args.onlymessage:
                av1_size = 0
            else:
                av1_size = os.path.getsize(f"{args.output}/{av1_video_name}")
            msg = f'\n{timer.name} 轉換結果:\n原檔案路徑: {args.path}\n原檔案大小: {human_readable_size(origin_size)}\n轉換後檔案大小: {human_readable_size(av1_size)}\n{timer.get_result()}\n'
            video_log.info(msg)
    else:
        h264_video_name = 'test-h264.mp4'
        av1_video_name = 'test-av1.mp4'
        
    if args.convert_m3u8:
        if args.type == 'all' or args.type == 'h264':
            # h264轉換成m3u8
            timer.set_name('h264轉換成m3u8')
            timer.start()
            key_name = generateEnctyptionKey(
                key_dir=args.output,
                p='h264_480',
                test=args.onlymessage
            )
            generateEnctyptionKeyInfo(
                http_url_of_key=f'{NGS_AVDATA_HOST}/{key_name}',
                key_path_in_loacl=f'{args.output}/{key_name}',
                keyinfo_dir=args.output,
                p='h264_480',
                test=args.onlymessage
            )
            videoConvertToEncryptedM3U8(
                video_path=f'{args.output}/{h264_video_name}',
                keyinfo_path=f'{args.output}/{key_name}',
                output_video_dir=args.output,
                output_video_name='test-h264-m3u8',
                test=args.onlymessage
            )
            timer.stop()
            video_log.info(f'\n{timer.name} 結果:\n{timer.get_result()}\n')

        if args.type == 'all' or args.type == 'av1':
            # 轉換成m3u8
            timer.set_name('av1轉換成m3u8')
            timer.start()
            key_name = generateEnctyptionKey(
                key_dir=args.output,
                p='av1_480',
                test=args.onlymessage
            )
            generateEnctyptionKeyInfo(
                http_url_of_key=f'{NGS_AVDATA_HOST}/{key_name}',
                key_path_in_loacl=f'{args.output}/{key_name}',
                keyinfo_dir=args.output,
                p='av1_480',
                test=args.onlymessage
            )
            videoConvertToEncryptedM3U8(
                video_path=f'{args.output}/{av1_video_name}',
                keyinfo_path=f'{args.output}/{key_name}',
                output_video_dir=args.output,
                output_video_name='test-av1-m3u8',
                test=args.onlymessage
            )
            # removeM3U8KeyHost(
            #     m3u8_path_in_local=f'{args.output}/{av1_video_name}',
            #     key_dir_in_s3=f'{NGS_AVDATA_HOST}/{key_name}',
            #     key_name=f'{NGS_AVDATA_HOST}/{key_name}',
            #     test=args.onlymessage
            # )
            timer.stop()
            video_log.info(f'\n{timer.name} 結果:\n{timer.get_result()}\n')
except Exception as err:
    video_log.error(err, exc_info=True)
