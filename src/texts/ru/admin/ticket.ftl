admin-ticket = 🎫 <b>Панель управления тикетами</b>

    { $is_tickets_exists ->
    [True] <i>ℹ️ Жми на кнопки, чтобы ответить на тикеты!</i>
    *[other] <i>🤖 Тикетов не найдено!</i>
    }

ticket-browsing = <b>🎫 Тикет #{ $ticket_id}</b>

        <b>👤 Пользователь:</b> <code>{ $first_name }</code> | <code>{ $user_id}</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>⌛️ Время создания:</b> <code>{ $created_at }</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>❓ Описание</b>: <pre> { $question }</pre>

    .process-btn = ✅ Обработать
    .deny-btn = ❌ Отклонить
    .ban-btn = 🚫 Заблокировать пользователя

approve = <b>ℹ️ Вот текст твоеего ответа:</b>

        <pre>{ $answer }</pre>
        <i>🤔 Всё верно?</i>

ticket-answer = ✏️ <b>Введите ответ на тикет:</b>
    .approve = { approve }
    .notify-user = <b>🎫 Тикет #{ $ticket_id} был рассмотрен!</b>

        <i>ℹ️ Ответ администрации:</i><pre>{ $answer }</pre>
    .notify-admin = ✅ Ответ был отправлен юзеру

ticket-deny = ✏️<b> Введи причину отклонения:</b>
    .notify-user = <b>🎫 Тикет #{ $ticket_id} был отклонен!</b>

        <i>❌ Причина:</i><pre>{ $answer }</pre>
    .notify-admin = ✅ Отклонение было отправлен юзеру

ban-duration = <b>⌛️ Бан продлится до:</b> <code>{ $date_until }</code>

time-selected = { $is_time_selected ->
    [True] {ban-duration}
    *[other] <i>⌛️ Введи время бана</i>
}

time-unit = { $time_unit ->
    [hours] Часы
    [days] Дни
    [minutes] Минуты
    *[other] Неизвестно
}

ticket-ban = ✏️<b>Введи причину бана:</b>
    .select-time = <b>🚫 Причина бана:</b><pre>{ $reason }</pre>

    { time-selected }
    .days-btn = Дни
    .hours-btn = Часы
    .minutes-btn = Минуты
    .input-time = ✏️<b>Введи { time-unit }:</b>
    .ban-btn = 🚫 Заблокировать пользователя
    .notify-user = <b>🚫 Вы были заблокированы в связи с тикетом # { $ticket_id }</b>

        <b>❌ Причина блокировки:</b> <code>{ $reason }</code>
        ➖➖➖➖➖➖➖➖➖➖
        {ban-duration}
    .notify-admin = ✅ Пользователь был забанен
