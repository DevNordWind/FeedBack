ticket = <b>➕ Создать тикет</b>

    <i>✏️ Введи описание своей проблемы</i>

    .create-ticket = <b>ℹ️ Вот текст твоей проблемы:</b>

        <pre>{ $question }</pre>
        <i>🤔 Всё верно?</i>
    .success-sent = <b>✅ Тикет #{ $ticket_id } был отправлен</b>

        <i>⌛️ Ожидайте ответа администрации...</i>
    .admin-msg = <b>🎫 Был создан тикет #{ $ticket_id}</b>

        <b>👤 Пользователь:</b> <code>{ $first_name }</code> | <code>{ $user_id}</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>⌛️ Время создания:</b> <code>{ $created_at }</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>❓ Описание</b>: <pre> { $question }</pre>

