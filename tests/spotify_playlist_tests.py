import allure
import requests
from client.playlist import Playlist
from assertpy import assert_that

from tests.helpers.spotify_helpers import get_playlist_id, get_error_details
from tests.utils.status_codes import StatusCode

playlist = Playlist()


def test_user_can_create_new_playlist():
    playlist.set_name('Playlist 1').set_description('Creating playlist through test script').set_is_public(False)
    response = playlist.create_playlist()
    allure.attach(name="Response body", body=response.text, attachment_type=allure.attachment_type.TEXT)
    allure.attach(name="Response headers", body=str(response.headers), attachment_type=allure.attachment_type.TEXT)
    assert_that(response.status_code).is_equal_to(requests.codes.created)
    assert_that(response.as_dict['name']).is_equal_to(playlist.get_name())
    assert_that(response.as_dict['description']).is_equal_to(playlist.get_description())
    assert_that(response.as_dict['public']).is_equal_to(playlist.get_is_public())


def test_user_can_see_created_playlist():
    playlist.set_name('Playlist 2').set_description('Creating playlist 2 through test script').set_is_public(False)
    new_playlist = playlist.create_playlist()
    playlist_id = get_playlist_id(new_playlist.as_dict)
    response = playlist.get_playlist(playlist_id)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.as_dict['name']).is_equal_to(playlist.get_name())
    assert_that(response.as_dict['description']).is_equal_to(playlist.get_description())
    assert_that(response.as_dict['id']).is_equal_to(playlist_id)
    assert_that(response.as_dict['public']).is_equal_to(playlist.get_is_public())


def test_user_can_update_playlist():
    playlist.set_name('Playlist 3').set_description('Creating playlist 3 through test script').set_is_public(False)
    new_playlist = playlist.create_playlist()
    playlist_id = get_playlist_id(new_playlist.as_dict)
    response = playlist.update_playlist(playlist_id)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.as_dict).is_empty()


def test_user_cannot_create_playlist_without_valid_name():
    playlist.set_name(None).set_description('Creating playlist 2 through test script').set_is_public(False)
    response = playlist.create_playlist()
    assert_that(response.status_code).is_equal_to(requests.codes.bad_request)
    status_code, message = get_error_details(response.as_dict)
    assert_that(status_code).is_equal_to(requests.codes.bad_request)
    assert_that(message).is_equal_to(StatusCode.BAD_REQUEST.value.message)


def test_user_cannot_create_playlist_without_valid_access_token():
    playlist.set_name('Playlist 4').set_description('Creating playlist 4 through test script').set_is_public(False)
    response = playlist.create_playlist(access_token='invalid')
    assert_that(response.status_code).is_equal_to(requests.codes.unauthorized)
    status_code, message = get_error_details(response.as_dict)
    assert_that(status_code).is_equal_to(requests.codes.unauthorized)
    assert_that(message).is_equal_to(StatusCode.UNAUTHORIZED.value.message)
