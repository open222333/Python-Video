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
