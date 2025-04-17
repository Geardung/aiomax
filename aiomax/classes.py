from .utils import get_message_body
from .types import *
from typing import *
from .buttons import *


class BotCommand:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    
    def as_dict(self):
        return {
            "name": self.name, "description": self.description
        }
    

class PhotoAttachmentRequestPayload:
    def __init__(self, url: "str | None"):
        self.url = url
    

    def as_dict(self):
        return {
            "url": self.url
        }
    

class User:
    def __init__(self,
        user_id: int,
        first_name: str,
        name: str,
        is_bot: bool,
        last_activity_time: int,
        last_name: "str | None" = None,
        username: "str | None" = None,
        description: "str | None" = None,
        avatar_url: "str | None" = None,
        full_avatar_url: "str | None" = None,
        commands: "List[BotCommand] | None" = None,
        last_access_time: "int | None" = None,
        is_owner: "bool | None" = None,
        is_admin: "bool | None" = None,
        join_time: "int | None" = None,
        permissions: "List[str] | None" = None

    ):
        self.user_id: int = user_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.name: str = name
        self.username: "str | None" = username
        self.is_bot: bool = is_bot
        self.last_activity_time: int = last_activity_time
        self.description: "str | None" = description
        self.avatar_url: "str | None" = avatar_url
        self.full_avatar_url: "str | None" = full_avatar_url
        self.commands: "List[BotCommand] | None" = [
            BotCommand(**i) for i in commands
        ] if commands else None
        self.last_access_time: "int | None" = last_access_time
        self.is_owner: "bool | None" = is_owner
        self.is_admin: "bool | None" = is_admin
        self.join_time: "int | None" = join_time
        self.permissions: "List[str] | None" = permissions


    @staticmethod
    def from_json(data: dict) -> "User | None":
        if data == None: return None

        return User(**data)
    
    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

class Attachment:
    def __init__(self, type: str):
        self.type: str = type


    @staticmethod
    def from_json(data: dict) -> "Attachment | None":
        if data['type'] == 'image':
            return PhotoAttachment.from_json(data)
        elif data['type'] == 'video':
            return VideoAttachment.from_json(data)
        elif data['type'] == 'audio':
            return AudioAttachment.from_json(data)
        elif data['type'] == 'file':
            return FileAttachment.from_json(data)
        elif data['type'] == 'sticker':
            return StickerAttachment.from_json(data)
        elif data['type'] == 'contact':
            return ContactAttachment.from_json(data)
        elif data['type'] == 'share':
            return ShareAttachment.from_json(data)
        elif data['type'] == 'location':
            return LocationAttachment.from_json(data)
        elif data['type'] == 'inline_keyboard':
            return InlineKeyboardAttachment.from_json(data)
        else:
            raise Exception(f"Unknown attachment type: {data['type']}")


class MediaPayload:
    def __init__(self,
        url: str,
        token: str,
    ):
        self.url: str = url
        self.token: str = token


    @staticmethod
    def from_json(data: dict) -> "MediaPayload | None":
        return MediaPayload(data['url'], data['token'])


class StickerPayload:
    def __init__(self,
        url: str,
        code: str,
    ):
        self.url: str = url
        self.code: str = code


    @staticmethod
    def from_json(data: dict) -> "StickerPayload | None":
        return StickerPayload(data['url'], data['code'])


class ContactPayload:
    def __init__(self,
        vcf_info: "str | None" = None,
        tam_info: "User | None" = None,
    ):
        self.vcf_info: "str | None" = vcf_info
        self.tam_info: "User | None" = tam_info


    @staticmethod
    def from_json(data: dict) -> "ContactPayload | None":
        return ContactPayload(data['vcf_info'], data['tam_info'])


class PhotoPayload(MediaPayload):
    def __init__(self,
        url: str,
        token: str,
        photo_id: int
    ):
        super().__init__(url, token)
        self.photo_id: int = photo_id

    
    @staticmethod
    def from_json(data: dict) -> "PhotoPayload | None":
        return PhotoPayload(data['url'], data['token'], data['photo_id'])


class PhotoAttachment(Attachment):
    def __init__(self,
        payload: PhotoPayload
    ):
        super().__init__("image")
        self.payload: PhotoPayload = payload


    @staticmethod
    def from_json(data: dict) -> "PhotoAttachment | None":
        return PhotoAttachment(
            PhotoPayload.from_json(data['payload'])
        )


class VideoAttachment(Attachment):
    def __init__(self,
        payload: MediaPayload,
        thumbnail: "str | None" = None,
        width: "int | None" = None,
        height: "int | None" = None,
        duration: "int | None" = None
    ):
        super().__init__("video")
        self.payload: MediaPayload = payload
        self.thumbnail: "str | None" = thumbnail
        self.width: "int | None" = width
        self.height: "int | None" = height
        self.duration: "int | None" = duration

    
    @staticmethod
    def from_json(data: dict) -> "VideoAttachment | None":
        return VideoAttachment(
            MediaPayload.from_json(data['payload']),
            data.get('thumbnail', None),
            data.get('width', None),
            data.get('height', None),
            data.get('duration', None),
        )


class AudioAttachment(Attachment):
    def __init__(self,
        payload: MediaPayload,
    ):
        super().__init__("audio")
        self.payload: MediaPayload = payload


    @staticmethod
    def from_json(data: dict) -> "AudioAttachment | None":
        return AudioAttachment(
            MediaPayload.from_json(data['payload'])
        )


class FileAttachment(Attachment):
    def __init__(self,
        payload: MediaPayload,
        filename: str,
        size: int
    ):
        super().__init__("file")
        self.payload: MediaPayload = payload
        self.filename: str = filename
        self.size: int = size


    @staticmethod
    def from_json(data: dict) -> "FileAttachment | None":
        return FileAttachment(
            MediaPayload.from_json(data['payload']),
            data['filename'],
            data['size']
        )


class StickerAttachment(Attachment):
    def __init__(self,
        payload: StickerPayload,
        width: int,
        height: int
    ):
        super().__init__("sticker")
        self.payload: StickerPayload = payload
        self.width: int = width
        self.height: int = height

    
    @staticmethod
    def from_json(data: dict) -> "StickerAttachment | None":
        return StickerAttachment(
            StickerPayload.from_json(data['payload']),
            data['width'],
            data['height']
        )


class ContactAttachment(Attachment):
    def __init__(self,
        payload: ContactPayload,
    ):
        super().__init__("contact")
        self.payload: ContactPayload = payload


    @staticmethod
    def from_json(data: dict) -> "ContactAttachment | None":
        return ContactAttachment(
            ContactPayload.from_json(data['payload'])
        )


class ShareAttachment(Attachment):
    def __init__(self,
        url: str,
        payload: "MediaPayload | None",
        title: "str | None" = None,
        description: "str | None" = None,
        image_url: "str | None" = None,
    ):
        super().__init__("share")
        self.url: str = url
        self.payload: "MediaPayload | None" = payload
        self.title: "str | None" = title
        self.description: "str | None" = description
        self.image_url: "str | None" = image_url


    @staticmethod
    def from_json(data: dict) -> "ShareAttachment | None":
        return ShareAttachment(
            data['url'],
            MediaPayload.from_json(data.get('payload', None)),
            data.get('title', None),
            data.get('description', None),
            data.get('image_url', None),
        )


class LocationAttachment(Attachment):
    def __init__(self,
        latitude: float,
        longitude: float,
    ):
        super().__init__("location")
        self.latitude: float = latitude
        self.longitude: float = longitude


    @staticmethod
    def from_json(data: dict) -> "LocationAttachment | None":
        return LocationAttachment(
            data['latitude'],
            data['longitude']
        )


class InlineKeyboardAttachment(Attachment):
    def __init__(self,
        payload: List[List[Button]],
    ):
        super().__init__("inline_keyboard")
        self.payload: List[List[Button]] = payload


    @staticmethod
    def from_json(data: dict) -> "InlineKeyboardAttachment | None":
        return InlineKeyboardAttachment(
            [[Button.from_json(j) for j in i] for i in data['payload']]
        )


class MessageRecipient:
    def __init__(self,
        chat_id: "int | None",
        chat_type: str
    ):
        self.chat_id: "int | None" = chat_id
        self.chat_type: str = chat_type


    @staticmethod
    def from_json(data: dict) -> "MessageRecipient":
        if data == None: return None

        return MessageRecipient(
            chat_id = data["chat_id"],
            chat_type = data["chat_type"]
        )
    

class Markup:
    def __init__(self,
        type: Literal[
            'strong', 'emphasized', 'monospaced', 'link', 'strikethrough',
            'underline', 'user_mention', 'heading', 'highlighted'
        ],
        start: int,
        length: int,
        user_link: "str | None" = None,
        user_id: "int | None" = None,
        url: "str | None" = None
    ):
        '''
        A markup element

        :param type: Markup type
        :param start: Start position
        :param length: Length
        :param user_link: Username. `None` if markup type is not `user_link`
        :param user_id: User ID. `None` if markup type is not `user_link`
        :param url: URL. `None` if markup type is not `link`
        '''
        self.type: Literal[
            'strong', 'emphasized', 'monospaced', 'link', 'strikethrough',
            'underline', 'user_mention', 'heading', 'highlighted'
        ] = type
        self.start: int = start
        self.length: int = length

        self.user_link: "str | None" = user_link
        self.user_id: "int | None" = user_id
        self.url: "str | None" = url


    @staticmethod
    def from_json(data: dict) -> "Markup | None":
        if data == None: return None

        if data['type'] == 'user_mention':
            return Markup(
                data['type'], data['from'], data['length'],
                user_link=data.get('user_link', None), user_id=data.get('user_id', None)
            )
        elif data['type'] == 'link':
            return Markup(
                data['type'], data['from'], data['length'], url=data['url']
            )

        return Markup(data['type'], data['from'], data['length'])


class MessageBody:
    def __init__(self,
        mid: str,
        seq: int,
        text: "str | None",
        attachments: "List[Attachment] | None",
        markup: "List[Markup] | None" = None
    ):
        self.message_id: str = mid
        self.seq: int = seq
        self.text: "str | None" = text
        self.attachments: "List[Attachment] | None" = attachments
        self.markup: "List[Markup] | None" = markup


    @staticmethod
    def from_json(data: dict) -> "MessageBody":
        if data == None: return None

        return MessageBody(
            mid = data["mid"],
            seq = data["seq"],
            text = data["text"],
            attachments = [Attachment.from_json(x) for x in data.get('attachments', [])],
            markup = [Markup.from_json(x) for x in data.get('markup', [])]
        )


class LinkedMessage:
    def __init__(self,
        type: str,
        message: MessageBody,
        sender: "User | None" = None,
        chat_id: "int | None" = None,
    ):
        self.type: str = type
        self.message: MessageBody = message
        self.sender: "User | None" = sender
        self.chat_id: "int | None" = chat_id


    @staticmethod
    def from_json(data: dict) -> "LinkedMessage":
        if data == None: return None
            
        return LinkedMessage(
            type = data["type"],
            message = MessageBody.from_json(data["message"]),
            sender = User.from_json(data.get('sender', None)),
            chat_id = data.get('chat_id', None),
        )


class Message:
    def __init__(self,
        recipient: MessageRecipient,
        body: MessageBody = None,
        timestamp: float = None,
        sender: "User | None" = None,
        link: "LinkedMessage | None" = None,
        views: "int | None" = None,
        url: "str | None" = None,
        constructor: "User | None" = None,
    ):
        self.recipient: MessageRecipient = recipient
        self.body: "MessageBody | None" = body
        self.timestamp: "float | None" = timestamp
        self.sender: "User | None" = sender
        self.link: "LinkedMessage | None" = link
        self.views: "int | None" = views
        self.url: "str | None" = url
        self.constructor: "User | None" = constructor
        self.user_locale: "str | None" = None


    @staticmethod
    def from_json(data: dict) -> "Message":
        return Message(
            recipient = MessageRecipient.from_json(data.get('recipient')),
            body = MessageBody.from_json(data.get('body', None)),
            timestamp = data.get('timestamp', None),
            sender = User.from_json(data.get("sender", None)),
            link = LinkedMessage.from_json(data.get("link", None)),
            views = data.get("stat", {}).get("views", None),
            url = data.get("url", None),
            constructor = User.from_json(data.get("constructor", None)),
        )
    

class BotStartPayload:
    def __init__(self,
        chat_id: int,
        user: User,
        payload: "str | None",
        user_locale: "str | None"
    ):
        self.chat_id: int = chat_id
        self.user: User = user
        self.payload: "str | None" = payload
        self.user_locale: "str | None" = user_locale


    @staticmethod
    def from_json(data: dict) -> "BotStartPayload":
        return BotStartPayload(
            chat_id = data["chat_id"],
            user = User.from_json(data["user"]),
            payload = data.get('payload', None),
            user_locale = data.get('user_locale', None)
        )
    

class CommandContext:
    def __init__(self,
        bot,
        message: Message,
        command_name: str,
        args: str
    ):
        self.bot = bot
        self.message: Message = message
        self.command_name: str = command_name
        self.args_raw: str = args
        self.args: List[str] = args.split()


    async def send(self,
        text: str,
        format: "Literal['html', 'markdown', 'default'] | None" = 'default',
        notify: bool = True,
        disable_link_preview: bool = False,
        keyboard: "List[List[Button]] | None" = None,
        # todo attachments
    ) -> Message:
        '''
        Send a message to the chat that the user sent the command.

        :param text: Message text. Up to 4000 characters
        :param format: Message format. Bot.default_format by default
        :param notify: Whether to notify users about the message. True by default.
        :param disable_link_preview: Whether to disable link preview. False by default
        :param keyboard: An inline keyboard to attach to the message
        '''
        return (await self.bot.send_message(
            text, chat_id=self.message.recipient.chat_id,
            format=format, notify=notify, disable_link_preview=disable_link_preview,
            keyboard=keyboard
        ))


    async def reply(self,
        text: str,
        format: "Literal['html', 'markdown', 'default'] | None" = 'default',
        notify: bool = True,
        disable_link_preview: bool = False,
        keyboard: "List[List[Button]] | None" = None,
        # todo attachments
    ) -> Message:
        '''
        Reply to the message that the user sent.

        :param text: Message text. Up to 4000 characters
        :param format: Message format. Bot.default_format by default
        :param notify: Whether to notify users about the message. True by default.
        :param disable_link_preview: Whether to disable link preview. False by default
        :param keyboard: An inline keyboard to attach to the message
        '''
        return (await self.bot.reply(
            text, self.message, format, notify, disable_link_preview, keyboard
        ))


class Handler():
    def __init__(
        self,
        call: Callable,
        filter: "Callable | None" = None,
    ):
        self.call = call
        self.filter = filter


class Image:
    def __init__(self,
        url: str,
    ):
        self.url: str = url
    
    
    @staticmethod
    def from_json(data: dict) -> "User | None":
        if data == None: return None

        return User(**data)
    

class Chat:
    def __init__(self,
        chat_id: int,
        type: str,
        status: str,
        last_event_time: int,
        participants_count: int,
        is_public: bool,
        title: "str | None" = None,
        icon: "Image | None" = None,
        description: "str | None" = None,
        pinned_message: "Message | None" = None,
        owner_id: "int | None" = None,
        participants: "int | None" = None,
        link: "str | None" = None,
        messages_count: "str | None" = None,
        chat_message_id: "str | None" = None,
        dialog_with_user: "User | None" = None,
    ):
        self.chat_id: int = chat_id
        self.type: str = type
        self.status: str = status
        self.last_event_time: int = last_event_time
        self.participants_count: int = participants_count
        self.title: "str | None" = title
        self.icon: "Image | None" = icon
        self.is_public: bool = is_public
        self.dialog_with_user: "User | None" = dialog_with_user
        self.description: "str | None" = description
        self.pinned_message: "Message | None" = pinned_message
        self.owner_id: "int | None" = owner_id
        self.participants: "int | None" = participants
        self.link: "str | None" = link
        self.messages_count: "str | None" = messages_count
        self.chat_message_id: "str | None" = chat_message_id


    @staticmethod
    def from_json(data: dict) -> "Chat | None":
        if data == None: return None

        return Chat(**data)
    

class Callback:
    def __init__(self,
        bot,
        timestamp: int,
        callback_id: str,
        user: User,
        user_locale: "str | None",
        payload: "str | None" = None
    ):
        self.bot = bot
        self.timestamp: int = timestamp
        self.callback_id: str = callback_id
        self.user: User = user
        self.payload: "str | None" = payload
        self.user_locale: "str | None" = user_locale


    async def answer(self,
        notification: "str | None" = None,
        text: "str | None" = None,
        format: "Literal['html', 'markdown', 'default'] | None" = 'default',
        notify: bool = True,
        keyboard: "List[List[Button]] | None" = None,
        # todo attachments
    ):
        '''
        Answer the callback.

        :param notification: Notification to display to the user
        :param text: Message text. Up to 4000 characters
        :param format: Message format. Bot.default_format by default
        :param notify: Whether to notify users about the message. True by default.
        :param disable_link_preview: Whether to disable link preview. False by default
        :param keyboard: An inline keyboard to attach to the message
        '''
        assert notification != None or text != None,\
            'Either notification or text must be specified'
        body = {
            'notification': notification,
            'message': None
        }
        if text != None:
            format = self.bot.default_format if format == 'default' else format
            body['message'] = get_message_body(text, format, notify=notify, keyboard=keyboard)

        out = await self.bot.post(
            'https://botapi.max.ru/answers', params={'callback_id': self.callback_id},
            json=body
        )
        return await out.json()


    @staticmethod
    def from_json(data: dict, user_locale: "str | None" = None, bot = None) -> "Callback | None":
        if data == None: return None
        
        return Callback(
            bot,
            data['timestamp'],
            data['callback_id'],
            User.from_json(data['user']),
            user_locale,
            data.get('payload', None)
        )
