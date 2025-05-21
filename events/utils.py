from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_email(event, participant):
    """Sending an email notification to a participant."""

    subject = f"You have been added to the event.: {event.title}"
    context = {
        "participant_username": participant.username,
        "event_title": event.title,
        "event_description": event.description,
        "event_date": event.date.strftime("%Y-%m-%d %H:%M:%S"),
        "event_location": event.location,
        "organizer_username": event.organizer.username,
        "organizer_email": event.organizer.email,
    }

    # Render HTML and text versions of the letter
    html_message = render_to_string("emails/event_notification.html", context)
    plain_message = strip_tags(html_message)

    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=None,
        recipient_list=[participant.email],
        html_message=html_message,
        fail_silently=True,  # Ignore sending errors
    )
