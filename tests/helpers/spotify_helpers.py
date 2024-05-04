def get_playlist_id(playlist_info):
    return playlist_info.get('id')


def get_error_details(error):
    error_details = error['error']
    return error_details['status'], error_details['message']
