from pydantic import BaseModel

from .sync_created_model import SyncCreatedModel
from .sync_deleted_model import SyncDeletedModel
from .sync_updated_model import SyncUpdatedModel


class SyncModel(BaseModel):
    created: SyncCreatedModel
    updated: SyncUpdatedModel
    deleted: SyncDeletedModel
