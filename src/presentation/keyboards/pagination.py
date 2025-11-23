from __future__ import annotations

from aiogram import Router, F, types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel


class PaginationItems(BaseModel):
    text: str
    callback_data: CallbackData


class PaginationNavCallbackData(CallbackData, prefix="pagination_nav"):
    action: str


class Pagination(object):
    """
    Пагинация, выводящая в каждой строке по одной Inline-кнопке для элемента из items,
    и внизу — кнопки «Назад» / «Вперед».

    Примечание: после создания объекта Pagination его нужно добавить в FSM-контекст (ОБЯЗАТЕЛЬНО!) в поле под названием "pagination".
    Пример кода:
        ```
        pagination: Pagination = Pagination(items=pagination_items)
        await state.update_data(pagination=pagination)
        ```
    """

    CALLBACK_DATA_START_NEXT = "next_page_"
    CALLBACK_DATA_START_PREV = "prev_page_"

    def __init__(
        self,
        items: list[PaginationItems],
        max_items_per_page: int = 5,
        callback_data_navigation_ending: str = "",
    ):
        """
        :param items: список словарей {"items": объект, "callback_data": CallbackData или str}
        :param max_items_per_page: сколько кнопок-элементов показывать на странице
        :param callback_data_navigation_ending: суффикс, добавляемый к callback_data кнопок «prev/next»
        """
        self.items: list[PaginationItems] = items
        self.callback_data_navigation_ending = callback_data_navigation_ending
        self.__max_items = max_items_per_page
        self.__page = 0
        self.__recalc_bounds()
        self.keyboard = self.__generate_keyboard()

    def __recalc_bounds(self) -> None:
        self.__start = self.__page * self.__max_items
        self.__end = self.__start + self.__max_items

    def __generate_keyboard(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        # Кнопки для элементов на текущей странице
        for elem in self.items[self.__start : self.__end]:
            builder.row(
                InlineKeyboardButton(
                    text=elem.text, callback_data=elem.callback_data.pack()
                )
            )

        # Нижний ряд: Назад / Вперед
        nav_buttons: list[InlineKeyboardButton] = []
        if self.__page > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=PaginationNavCallbackData(
                        action=f"{self.CALLBACK_DATA_START_PREV}{self.callback_data_navigation_ending}"
                    ).pack(),
                )
            )
        if self.__end < len(self.items):
            nav_buttons.append(
                InlineKeyboardButton(
                    text="Вперед",
                    callback_data=PaginationNavCallbackData(
                        action=f"{self.CALLBACK_DATA_START_NEXT}{self.callback_data_navigation_ending}"
                    ).pack(),
                )
            )

        if nav_buttons:
            builder.row(*nav_buttons)

        return builder.as_markup()

    def next_page(self) -> Pagination:
        if self.__end < len(self.items):
            self.__page += 1
            self.__recalc_bounds()
            self.keyboard = self.__generate_keyboard()
        return self

    def prev_page(self) -> Pagination:
        if self.__page > 0:
            self.__page -= 1
            self.__recalc_bounds()
            self.keyboard = self.__generate_keyboard()
        return self

    def get_markup(self) -> InlineKeyboardMarkup:
        return self.keyboard


pagination_router = Router()


@pagination_router.callback_query(
    PaginationNavCallbackData.filter(
        F.action.startswith(Pagination.CALLBACK_DATA_START_NEXT)
    )
)
async def next_page_handler(
    callback: types.CallbackQuery,
    callback_data: PaginationNavCallbackData,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    pagination: Pagination = data["pagination"]
    pagination.next_page()
    await callback.message.edit_reply_markup(reply_markup=pagination.get_markup())
    await callback.answer()


@pagination_router.callback_query(
    PaginationNavCallbackData.filter(
        F.action.startswith(Pagination.CALLBACK_DATA_START_PREV)
    )
)
async def prev_page_handler(
    callback: types.CallbackQuery,
    callback_data: PaginationNavCallbackData,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    pagination: Pagination = data["pagination"]
    pagination.prev_page()
    await callback.message.edit_reply_markup(reply_markup=pagination.get_markup())
    await callback.answer()
