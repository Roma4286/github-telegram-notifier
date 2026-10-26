from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from ..models import Base


class BaseRepository[ModelT: Base]:
    model: type[ModelT]

    def __init__(self, session: Session):
        self.session = session

    def _detach(self, obj: ModelT) -> ModelT:
        self.session.expunge(obj)
        return obj

    def _first(self, stmt: Select[tuple[ModelT]]) -> ModelT | None:
        obj = self.session.scalars(stmt).first()
        return self._detach(obj) if obj is not None else None

    def _all(self, stmt: Select[tuple[ModelT]]) -> Sequence[ModelT]:
        objs = self.session.scalars(stmt).all()
        for obj in objs:
            self.session.expunge(obj)
        return objs

    def get(self, id: Any) -> ModelT | None:
        obj = self.session.get(self.model, id)
        return self._detach(obj) if obj is not None else None

    def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[ModelT]:
        return self._all(select(self.model).limit(limit).offset(offset))

    def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return self._detach(obj)

    def update(self, obj: ModelT, **fields: Any) -> ModelT:
        obj = self.session.merge(obj)
        for name, value in fields.items():
            if not hasattr(obj, name):
                raise AttributeError(f"{self.model.__name__} has no field {name!r}")
            setattr(obj, name, value)
        self.session.commit()
        self.session.refresh(obj)
        return self._detach(obj)

    def delete(self, obj: ModelT) -> None:
        self.session.delete(self.session.merge(obj))
        self.session.commit()
