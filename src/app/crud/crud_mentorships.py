from fastcrud import FastCRUD

from ..models.mentorship import Mentorship
from ..schemas.mentorship import MentorshipDelete, MentorshipCreateInternal, MentorshipUpdate, MentorshipUpdateInternal

CRUDMentorship = FastCRUD[Mentorship, MentorshipCreateInternal, MentorshipUpdate, MentorshipUpdateInternal, MentorshipDelete]
crud_mentorships = CRUDMentorship(Mentorship)
