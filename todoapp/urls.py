from django.urls import path
from todoapp.views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, TaskLoginView, TaskLogoutView, TaskRegister, TaskReorder

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task' ),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('update-task/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('delete-task/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('login/', TaskLoginView.as_view(), name='task-login'),
    path('logout/', TaskLogoutView.as_view(), name='task-logout'),
    path('register/', TaskRegister.as_view(), name='task-register'),
    path('reorder-task/', TaskReorder.as_view(), name='task-reorder'),
]

