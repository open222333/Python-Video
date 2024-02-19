from src.tool import get_all_files
import instaloader
import shutil
import os


class InstagramClawler:
    
    output_dir = 'output'
    l = instaloader.Instaloader()

    def __init__(self, username: str) -> None:
        self.username = username
        self.user_directory = os.path.join(self.output_dir, self.username)
        
    def login(self, username:str, password:str, session_filename='instaloader.session'):
        if not os.path.exists(session_filename):
            self.l.context.login(username, password)
            self.l.save_session_to_file(session_filename)
            
        try:
            self.l.load_session_from_file(self.username, session_filename)
        except instaloader.exceptions.InstaloaderException as e:
            self.l.context.login(username, password)
            self.l.save_session_to_file(session_filename)
        
    def download_user_videos(self, username:str, password:str):
        self.login(username, password)
        
        try:
            os.makedirs(self.user_directory, exist_ok=True)
            # 獲取用戶資料
            profile = instaloader.Profile.from_username(self.l.context, self.username)
            # 下載所有影片
            for post in profile.get_posts():
                if post.is_video:
                    self.l.download_post(post, target=self.username)
        except instaloader.exceptions.ProfileNotExistsException as e:
            print(e)
        
    def move_to_dir(self, remove_except_mp4=True):
        files = get_all_files(self.username)
        for file in files:
            if remove_except_mp4:
                _, extension = os.path.splitext(file)
                if extension == '.mp4':
                    shutil.move(file, self.user_directory)
            else:
                shutil.move(file, self.user_directory)
        shutil.rmtree(self.username)
