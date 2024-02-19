import instaloader


class InstagramClawler:

    def __init__(self, username: str) -> None:
        self.username = username

    def download_user_videos(self):
        # 創建 Instaloader 實例
        L = instaloader.Instaloader()

        try:
            # 獲取用戶資料
            profile = instaloader.Profile.from_username(L.context, self.username)

            # 創建用戶目錄
            user_directory = f'./{self.username}'
            L.download_profile(profile.username, profile_pic_only=False)

            # 下載所有影片
            for post in profile.get_posts():
                if post.is_video:
                    L.download_post(post, target=user_directory)

            print(f'所有影片已下載至 {user_directory}')
        except instaloader.exceptions.ProfileNotExistsException:
            print(f'用戶 {self.username} 不存在')
