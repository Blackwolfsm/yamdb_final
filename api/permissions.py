from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return (request.user.role.lower() == 'admin' or
                request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            if request.method == 'GET':
                return True
            else:
                return False
        if request.method == 'GET':
            return True
        return request.user == obj.author


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (request.user == obj.author or
                    request.user.role.lower() == 'moderator' or
                    request.user.role.lower() == 'admin' or
                    request.user.is_superuser)
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (request.user or
                    request.user.role.lower() == 'moderator' or
                    request.user.role.lower() == 'admin' or
                    request.user.is_superuser)
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (request.user.role.lower() == 'admin' or
                    request.user.is_superuser)
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (request.user.role.lower() == 'admin' or
                    request.user.is_superuser)
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
