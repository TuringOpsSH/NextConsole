# 用户中心
from app.views.user_center.user_process import *
from app.views.user_center.role_process import *
from app.views.user_center.permission_process import *
from app.views.user_center.user_role_process import *
from app.views.user_center.role_permission_process import *
from app.views.user_center.system_notice import *
# 通讯录
from app.views.contacts.friends import *
from app.views.contacts.company import *
from app.views.contacts.department import *
from app.views.contacts.colleague import *
from app.views.contacts.visitor import *

# 助手中心
from app.views.assistant_center.assistant_manager import *
# from app.views.assistant_center.shop_assistant_manager import *
from app.views.assistant_center.assistant_instructions import *

# 配置中心
from app.views.configure_center.admin import *
from app.views.configure_center.user_config import *
from app.views.configure_center.model_manager import *
from app.views.configure_center.system_notice import *

# 工作台
from app.views.next_console.next_console import *
from app.views.next_console.attachment import *
from app.views.next_console.recommend_question import *
from app.views.next_console.workflow import *
from app.views.next_console.reference import *


# 资源中心
from app.views.resource_center.resource_objects import *
from app.views.resource_center.resource_recycle_objects import *
from app.views.resource_center.resource_shortcut import *
from app.views.resource_center.resource_tag import *
from app.views.resource_center.resource_view import *
from app.views.resource_center.resource_share import *

from app.views.task_center.workflow import *

# 知识中心
from app.views.knowledge_center.rag_api import *
from app.views.knowledge_center.resource_api import *

# 应用中心
from app.views.app_center.app_manage_view import *
from app.views.app_center.app_run import *
from app.utils.edith_web.edith_view import *

