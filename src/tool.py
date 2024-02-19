import os


def human_readable_size(size: int, decimal_places: int = 2) -> str:
	"""人類可讀 檔案大小
	
	https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
	Args:
	    size (int): 檔案大小 (bytes)
	    decimal_places (int, optional): 顯示小數位. Defaults to 2.
	
	Returns:
	    str: 檔案大小 單位
	"""
	for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
		if size < 1024.0 or unit == 'PB':
			break
		size /= 1024.0
	return f"{size:.{decimal_places}f} {unit}"

def get_all_files(dir_path: str, extensions=None):
	"""取得所有檔案
	
	Args:
	    dir_path (_type_): 檔案資料夾
	    extensions (_type_, optional): 指定副檔名,若無指定則全部列出. Defaults to None.
	
	Returns:
	    _type_: _description_
	"""
	target_file_path = []
	path = os.path.abspath(dir_path)

	for file in os.listdir(path):
		_, file_extension = os.path.splitext(file)
		if extensions:
			allow_extension = [f'.{e}' for e in extensions]
			if file_extension in allow_extension:
				target_file_path.append(f'{dir_path}/{file}')
		else:
			target_file_path.append(f'{dir_path}/{file}')

		# 遞迴
		if os.path.isdir(f'{dir_path}/{file}'):
			files = get_all_files(f'{dir_path}/{file}', extensions)
			for file in files:
				target_file_path.append(file)
	target_file_path.sort()
	return target_file_path
