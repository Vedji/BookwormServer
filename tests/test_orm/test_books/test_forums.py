import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# import app modules
from app.models.books.forums import BookForumAnswers, BookForumQuestions
from app.schemas.constants import UserRoleDB
from schemas.constants import AllowedBookFileFormats

# import test environment
from .. import (init_sqlite_db_local_case,  get_db_local_case)
from tests.utils.orm.books import BookCrudORM
from tests.utils.orm.users import UserCrudORM


class TestForums:

    @pytest.mark.asyncio
    async def test_forums(self, get_db_local_case: AsyncSession):
        role = UserRoleDB.USER.value

        # Создаем пользователя, который будет добавлять книгу
        user_1 = await UserCrudORM.create_user(get_db_local_case, username="username-1", role=role)
        user_2 = await UserCrudORM.create_user(get_db_local_case, username="username-2", role=role)
        user_3 = await UserCrudORM.create_user(get_db_local_case, username="username-3", role=role)
        await get_db_local_case.commit()

        # Создаем и проверяем книгу
        book = await BookCrudORM.create_book(
            get_db_local_case,
            book_publication_date=datetime(1024, 6, 6),
            book_content = None,
            book_content_type=AllowedBookFileFormats.NONE,
            book_isbn="9780733426094",
            added_user=user_1.user_id
        )
        await get_db_local_case.commit()

        question_1 = BookForumQuestions(
            book_id=book.book_id,
            is_open=True,
            title="Успешно ли тестирование?",
            question_message=None,
            added_user=user_1.user_id
        )
        question_2 = BookForumQuestions(
            book_id=book.book_id,
            is_open=True,
            title="Успешно ли тестирование 2?",
            question_message=None,
            added_user=user_1.user_id
        )
        get_db_local_case.add_all([question_1, question_2])
        await get_db_local_case.commit()
        answer_11 = BookForumAnswers(
            forum_id=question_1.forum_id,
            message="Возможно...",
            added_user=user_2.user_id,

        )
        answer_12 = BookForumAnswers(
            forum_id=question_1.forum_id,
            message="Смотря как тестировать.",
            added_user=user_3.user_id,

        )
        answer_21 = BookForumAnswers(
            forum_id=question_2.forum_id,
            message="Смотря как тестировать 2.",
            added_user=user_2.user_id,

        )
        get_db_local_case.add_all([answer_11, answer_12, answer_21])
        await get_db_local_case.commit()
        await get_db_local_case.refresh(question_1)
        await get_db_local_case.refresh(user_1)
        await get_db_local_case.refresh(user_2)
        await get_db_local_case.refresh(book)

        assert question_1.title == "Успешно ли тестирование?"
        assert answer_11 in question_1.answers
        assert answer_12 in question_1.answers
        assert answer_21 in user_2.book_forum_answers
        assert question_1 in user_1.book_forum_questions
        assert question_1 in book.book_forum_questions
        assert question_2 in book.book_forum_questions
