from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRequest(_message.Message):
    __slots__ = ("id", "userId", "messageType", "subject", "message", "file")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    MESSAGETYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    messageType: int
    subject: str
    message: str
    file: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., messageType: _Optional[int] = ..., subject: _Optional[str] = ..., message: _Optional[str] = ..., file: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("id", "userId", "messageType", "subject", "message", "file")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    MESSAGETYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    messageType: int
    subject: str
    message: str
    file: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., messageType: _Optional[int] = ..., subject: _Optional[str] = ..., message: _Optional[str] = ..., file: _Optional[str] = ...) -> None: ...

class MessageListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[MessageResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[MessageResponse, _Mapping]]] = ...) -> None: ...
