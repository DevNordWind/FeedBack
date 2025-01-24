admin-ticket = 🎫 <b>Ticket Management Panel</b>

    { $is_tickets_exists ->
    [True] <i>ℹ️ Click the buttons to respond to tickets!</i>
    *[other] <i>🤖 No tickets found!</i>
    }

ticket-browsing = <b>🎫 Ticket #{ $ticket_id }</b>

        <b>👤 User:</b> <code>{ $first_name }</code> | <code>{ $user_id }</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>⌛️ Created at:</b> <code>{ $created_at }</code>
        ➖➖➖➖➖➖➖➖➖➖
        <b>❓ Description:</b> <pre>{ $question }</pre>

    .process-btn = ✅ Process
    .deny-btn = ❌ Deny
    .ban-btn = 🚫 Ban User

approve = <b>ℹ️ Here is the text of your response:</b>

        <pre>{ $answer }</pre>
        <i>🤔 Is everything correct?</i>

ticket-answer = ✏️ <b>Enter your response to the ticket:</b>
    .approve = { approve }
    .notify-user = <b>🎫 Ticket #{ $ticket_id } has been reviewed!</b>

        <i>ℹ️ Administration's response:</i><pre>{ $answer }</pre>

ticket-deny = ✏️<b> Enter the reason for denial:</b>
    .notify-user = <b>🎫 Ticket #{ $ticket_id } has been denied!</b>

        <i>❌ Reason:</i><pre>{ $answer }</pre>

ban-duration = <b>⌛️ The ban will last until:</b> <code>{ $date_until }</code>

time-selected = { $is_time_selected ->
    [True] {ban-duration}
    *[other] <i>⌛️ Enter the ban duration</i>
}

time-unit = { $time_unit ->
    [hours] Hours
    [days] Days
    [minutes] Minutes
    *[other] Unknown
}

ticket-ban = ✏️<b>Enter the reason for the ban:</b>
    .select-time = <b>🚫 Reason for the ban:</b><pre>{ $reason }</pre>

    { time-selected }
    .days-btn = Days
    .hours-btn = Hours
    .minutes-btn = Minutes
    .input-time = ✏️<b>Enter { time-unit }:</b>
    .ban-btn = 🚫 Ban User
    .notify-user = <b>🚫 You have been banned due to ticket #{ $ticket_id }</b>

        <b>❌ Reason for the ban:</b> <code>{ $reason }</code>
        ➖➖➖➖➖➖➖➖➖➖
        {ban-duration}
