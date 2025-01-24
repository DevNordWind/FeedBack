ticket = <b>➕ Create ticket</b>

    <i>✏️ Enter a description of your problem:</i>

    .create-ticket = <b>ℹ️ Here's the text of your problem:</b>

        <pre>{ $question }</pre>
        <i>🤔 Is that correct?</i>
    .success-sent = <b>✅ Ticket #{ $ticket_id } has been sent</b>

        <i>⌛️ Wait for the administration's response...</i>
    .admin-msg = <b>🎫 A ticket has been created #{ $ticket_id}</b>

        <b>👤 User:</b> <code>{ $first_name }</code> | <code>{ $user_id}</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>⌛️ Creation time:</b> <code>{ $created_at }</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>❓ Description</b>: <pre> { $question }</pre>

