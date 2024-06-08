from django.urls import reverse, resolve
from lendsqr.views import (
    new_loan,
    get_staff_status,
    users,
    update_status,
    advance_filter,
)


def test_get_users_is_resolved():
    url = reverse("users")
    assert resolve(url).func == users


def test_update_status_is_resolved():
    id_value = "12345"
    action_value = "Active"
    url = reverse(viewname="status", args=[id_value, action_value])
    assert resolve(url).func == update_status


def test_advance_filter_is_resolved():
    url = reverse("advance_filter")
    assert resolve(url).func == advance_filter


def test_staff_staus_is_resolved():
    url = reverse("staff_staus")
    assert resolve(url).func == get_staff_status


def test_staff_staus_is_resolved():
    url = reverse("loan")
    assert resolve(url).func == new_loan
