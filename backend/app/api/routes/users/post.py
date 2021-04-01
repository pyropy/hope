from fastapi import APIRouter
from fastapi import Body, BackgroundTasks

from app.models.email import QuestionEmail
from app.models.email import EmailResponse

from app.api.dependencies.email import send_message


router = APIRouter()

@router.post("/contact/email")
async def send_user_question_via_email(
    background_tasks: BackgroundTasks,
    email: QuestionEmail = Body(..., embed=True),
    ) -> None:

    background_tasks.add_task(send_message, subject=email.user_email, message_text=email.email_body)

    return None
