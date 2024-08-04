from fastcrud import FastCRUD

from .token_blocklist import TokenBlocklist
from ..schemas import TokenBlocklistCreate, TokenBlocklistUpdate

CRUDTokenBlocklist = FastCRUD[TokenBlocklist, TokenBlocklistCreate, TokenBlocklistUpdate, TokenBlocklistUpdate, None]
crud_token_blocklist = CRUDTokenBlocklist(TokenBlocklist)
