from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

# THE PERMISSIONS WE NEED.
# ONLY ADMIN PERMISSION
# ONLY TUTOR AND ADMIN PERMISSION
# ONLY TUTOR, ADMIN AND OBJECT USER PERMISSIONS.
# ONLY STUDENT GROUP MEMEBERS, ADMIN AND TUTORS PERMISSIONS  ==== BAN USER PERMITION.
# ONLY USER PERMISSION.





class isAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return (user and user.groups.filter(name="ADMIN").exists())
        


class isTutorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.groups.filter(name="TUTOR").exists() or user.groups.filter(name="ADMIN"))
        



class isTutorOrAdminEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
    
        user = request.user
        return (user.groups.filter(name="TUTOR").exists() or user.groups.filter(name="ADMIN"))
    


class isValidUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return (user.groups.filter(name="ADMIN").exists() or user.groups.filter(name="TUTOR").exists() or user.groups.filter(name="STUDENT").exists())



class owner_Tutor_Admin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return ( obj.profile.user==user or user.groups.filter(name="ADMIN").exists() or user.groups.filter(name="TUTOR").exists() )



class ownerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return ( obj.user == user)




class profilePermision(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return ( obj.user==user or user.groups.filter(name="ADMIN").exists() or user.groups.filter(name="TUTOR").exists() )


    
