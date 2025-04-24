import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

# import app modules
from app.models.supports import SupportRequest, RequestsToGetRoleAuthor, RequestsToGetRolePublisher
from app.schemas.constants import UserRoleDB
from schemas.constants.ticket_attributes import SupportRequestTypes, RequestStatus


# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.users import UserCrudORM


class TestBookComments:
    """Тестирует ORM-модель тикетов в техническую поддержку. """

    @pytest.mark.asyncio
    async def test_support_requests(self, get_db_local_case: AsyncSession):

        # Добавление пользователей
        user_1 = await UserCrudORM.create_user(
            get_db_local_case, username="username", role=UserRoleDB.USER.value)
        user_2 = await UserCrudORM.create_user(
            get_db_local_case, username="username-2", role=UserRoleDB.USER.value)
        user_admin = await UserCrudORM.create_user(
            get_db_local_case, username="username-admin", role=UserRoleDB.ADMINISTRATOR.value)

        get_db_local_case.add_all([user_1, user_2, user_admin])
        await get_db_local_case.commit()

        # Добавление единичного тикета
        ticket_1 = SupportRequest(
            support_request_type=SupportRequestTypes.REQUEST_ABOUT_ERROR.value,
            status=RequestStatus.PENDING.value,
            subject="",
            message=None,
            user_id=user_1.user_id,
            moderator_comment="",
            reviewed_user_id=None
        )
        get_db_local_case.add(ticket_1)
        await get_db_local_case.commit()

        # Тестирование, что у тикета нет проверяющего администратора
        assert ticket_1.reviewed_user_id is None, "Moderator is not checked ticket"

        # Добавление к тикету ответа от модератора
        ticket_1.reviewed_user_id = user_admin.user_id
        ticket_1.moderator_comment = "Ticket has checked!"
        ticket_1.status = RequestStatus.APPROVED.value
        await get_db_local_case.commit()
        await get_db_local_case.refresh(ticket_1)

        # Тестирование, что тикет успешно рассмотрен
        assert ticket_1.reviewed_user_id == user_admin.user_id
        assert ticket_1.moderator_comment == "Ticket has checked!"
        assert ticket_1.status == RequestStatus.APPROVED.value
        assert ticket_1.reviewed_by.username == user_admin.username

        # Добавление списка тикетов от разных пользователей
        ticket_2 = SupportRequest(
            support_request_type=SupportRequestTypes.REQUEST_TO_GET_AUTHOR_ROLE.value,
            status=RequestStatus.PENDING.value,
            subject="",
            message=None,
            user_id=user_1.user_id,
            moderator_comment="",
            reviewed_user_id=None
        )
        ticket_3 = SupportRequest(
            support_request_type=SupportRequestTypes.REQUEST_TO_GET_PUBLISHER_ROLE.value,
            status=RequestStatus.REJECTED.value,
            subject="",
            message=None,
            user_id=user_2.user_id,
            moderator_comment="",
            reviewed_user_id=user_admin.user_id
        )
        get_db_local_case.add_all([ticket_2, ticket_3])
        await get_db_local_case.commit()

        await get_db_local_case.refresh(user_1)
        await get_db_local_case.refresh(user_2)
        await get_db_local_case.refresh(user_admin)

        # Проверка, что списки тикетов успешно отображаются
        assert ticket_1 in user_admin.reviewed_tickets
        assert ticket_2 not in user_admin.reviewed_tickets
        assert ticket_3 in user_admin.reviewed_tickets

        assert ticket_1 in user_1.submitted_tickets
        assert ticket_2 in user_1.submitted_tickets
        assert ticket_3 not in user_1.submitted_tickets

        assert ticket_1.status == RequestStatus.APPROVED.value
        assert ticket_2.status == RequestStatus.PENDING.value
        assert ticket_3.status == RequestStatus.REJECTED.value

        # Тестирование дополнительной информации к тикету для авторов

        authors_metadata_ticked = RequestsToGetRoleAuthor(
            ticked_id = ticket_2.ticked_id,
            first_name="Артур",
            last_name="Кларк",
            contact_email="test@email.ru",
            website=None,
            birthday=date(1917, 12, 16),
            nationality="Великобритания",
            description=""
        )
        get_db_local_case.add(authors_metadata_ticked)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(ticket_2)

        assert ticket_2.author_request is authors_metadata_ticked
        assert ticket_2.publisher_request is None
        assert ticket_2.author_request.ticked_id == authors_metadata_ticked.ticked_id
        assert ticket_2.author_request.first_name == "Артур"
        assert ticket_2.author_request.last_name == "Кларк"
        assert ticket_2.author_request.contact_email == "test@email.ru"
        assert ticket_2.author_request.nationality == "Великобритания"
        assert ticket_2.author_request.birthday.strftime("%Y-%m-%d") == "1917-12-16"

        publisher_metadata_ticked = RequestsToGetRolePublisher(
            ticked_id=ticket_3.ticked_id,
            publisher_name="publisher test",
            website="www.publisher.test.ru",
            contact_email="test_pub@email.ru",
            contact_phone="+79990001221",
            founded_year=date(1953, 1, 1),
            description="test description"
        )
        get_db_local_case.add(publisher_metadata_ticked)
        await get_db_local_case.commit()
        await get_db_local_case.refresh(ticket_3)

        assert ticket_3.publisher_request is publisher_metadata_ticked
        assert ticket_3.author_request is None
        assert ticket_3.ticked_id == publisher_metadata_ticked.ticked_id
        assert ticket_3.publisher_request.publisher_name == "publisher test"
        assert ticket_3.publisher_request.website == "www.publisher.test.ru"
        assert ticket_3.publisher_request.contact_email == "test_pub@email.ru"
        assert ticket_3.publisher_request.contact_phone == "+79990001221"
        assert ticket_3.publisher_request.founded_year.strftime("%Y") == "1953"
        assert ticket_3.publisher_request.description == "test description"
