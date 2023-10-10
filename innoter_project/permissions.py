import requests
from rest_framework.permissions import BasePermission

from innoter_project import settings


class IsAdminOrModeratorOfOwnerGroup(BasePermission):
    def has_object_permission(self, request, view, obj):
        token = request.META.get("HTTP_AUTHORIZATION", "").split("Bearer ")[-1]
        url = settings.USER_MANAG_URL + str(obj.uuid)
        headers = {"Authorization": "Bearer {}".format(token)}
        r = requests.get(url, headers=headers, verify=False)
        return True if r.status_code == 200 else False


class IsOwnerOfPage(BasePermission):
    def has_object_permission(self, request, view, obj):

        return True if request.user == str(obj.uuid) else False
