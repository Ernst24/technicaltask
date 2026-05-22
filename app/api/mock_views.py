from fastapi import APIRouter, Depends
from app.schemas.permissions import ResourceEnum, ActionEnum
from app.api.dependencies import PermissionChecker

router = APIRouter(prefix="", tags=["Бизнес Логика"])


@router.get("/documents", summary="Просмотр документов (Доступно: ВСЕМ ролям)")
async def get_documents(
    current_user=Depends(PermissionChecker(ResourceEnum.DOCUMENT, ActionEnum.READ)),
):
    return {"info": "Список документов", "data": [{"id": 1, "title": "Инструкция.pdf"}]}


@router.post("/documents", summary="Создание нового документа - [MANAGER][ADMIN]")
async def create_document(
    current_user=Depends(PermissionChecker(ResourceEnum.DOCUMENT, ActionEnum.CREATE)),
):
    return {"status": "success", "message": "Документ успешно загружен на сервер"}


@router.put(
    "/documents/{doc_id}", summary="Редактирование документа - [MANAGER][ADMIN]"
)
async def update_document(
    doc_id: int,
    current_user=Depends(PermissionChecker(ResourceEnum.DOCUMENT, ActionEnum.UPDATE)),
):
    return {"status": "success", "message": f"Документ {doc_id} изменен"}


@router.delete(
    "/documents/{doc_id}", summary="Безвозвратное удаление документа [ADMIN]"
)
async def delete_document(
    doc_id: int,
    current_user=Depends(PermissionChecker(ResourceEnum.DOCUMENT, ActionEnum.DELETE)),
):
    return {"status": "danger", "message": f"Документ {doc_id} стерт из базы данных"}


@router.get("/users", summary="Список всех пользователей [SUPPORT][MANAGER][ADMIN] ")
async def get_all_users_profiles(
    current_user=Depends(PermissionChecker(ResourceEnum.USER, ActionEnum.READ)),
):
    return {
        "info": "Список пользователей системы для внутренней работы",
        "data": [
            {"id": 101, "email": "ivan@mail.ru", "status": "active"},
            {"id": 102, "email": "petr@mail.ru", "status": "banned"},
        ],
    }


@router.post("/tickets", summary="Создание обращения в поддержку [CLIENT][ADMIN]")
async def create_support_ticket(
    current_user=Depends(PermissionChecker(ResourceEnum.TICKET, ActionEnum.CREATE)),
):
    return {"status": "success", "message": "Ваше обращение №4382 принято в обработку"}


@router.get("/tickets", summary="Просмотр списка тикетов [CLIENT][SUPPORT][ADMIN]")
async def get_support_tickets(
    current_user=Depends(PermissionChecker(ResourceEnum.TICKET, ActionEnum.READ)),
):
    return {"info": "Список открытых обращений", "count": 3}


@router.patch(
    "/tickets/{ticket_id}/resolve",
    summary="Ответ на тикет и его закрытие [SUPPORT][ADMIN]",
)
async def resolve_support_ticket(
    ticket_id: int,
    current_user=Depends(PermissionChecker(ResourceEnum.TICKET, ActionEnum.UPDATE)),
):
    return {
        "status": "success",
        "message": f"Тикет {ticket_id} переведен в статус 'Решено'",
    }


@router.get(
    "/analytics/revenue", summary="Просмотр финансовой выручки [MANAGER][ADMIN]"
)
async def get_revenue_analytics(
    current_user=Depends(PermissionChecker(ResourceEnum.ANALYTICS, ActionEnum.READ)),
):
    return {"metric": "Выручка компании", "value": "1,250,000 руб."}


@router.get("/analytics/server-logs", summary="Очистка логов сервера [ADMIN]")
async def get_server_performance_logs(
    current_user=Depends(PermissionChecker(ResourceEnum.ANALYTICS, ActionEnum.DELETE)),
):
    return {"status": "success", "message": "Системные логи успешно зачищены."}
