from events.models import Attendee

def register_attendee(event, name, email):
    if event.attendees.count() >= event.max_capacity:
        return False, "Events Capacity is Full."

    if Attendee.objects.filter(event=event, email=email).exists():
        return False, "This email is already registered for the event."

    Attendee.objects.create(event=event, name=name, email=email)
    return True, "Registration successful."
