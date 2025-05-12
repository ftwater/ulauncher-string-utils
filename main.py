import re
import hashlib

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

class StringUtils:
    def removeSpecialCharacters(text) -> str:
        return re.sub(r'[^\w\sÀ-ÿ]', '', text)
    
    def convertToUpperCase(text) -> str:
        return text.upper()
    
    def convertToLowerCase(text) -> str:
        return text.lower()
    
    def convertToCamelCase(text) -> str:
        words = text.split()
        return ''.join(word.capitalize() for word in words)
    
    def convertToSnakeCase(text) -> str:
        words = text.split()
        return '_'.join(word.lower() for word in words)
    
    def convertToKebabCase(text) -> str:
        words = text.split()
        return '-'.join(word.lower() for word in words)
    
    def convertToSentenceCase(text) -> str:
        if not text:
            return ""
        return text[0].upper() + text[1:].lower()
    
    def convertToTitleCase(text) -> str:
        return text.title()
    
    def convertToMD5(text) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    

UTILS = {
    'remove': ('Remove Special Characters', StringUtils.removeSpecialCharacters),
    'upper': ('Convert to Upper Case', StringUtils.convertToUpperCase),
    'lower': ('Convert to Lower Case', StringUtils.convertToLowerCase),
    'camel': ('Convert to Camel Case', StringUtils.convertToCamelCase),
    'snake': ('Convert to Snake Case', StringUtils.convertToSnakeCase),
    'kebab': ('Convert to Kebab Case', StringUtils.convertToKebabCase),
    'sentence': ('Convert to Sentence Case', StringUtils.convertToSentenceCase),
    'title': ('Convert to Title Case', StringUtils.convertToTitleCase),
    'md5': ('Convert to MD5 Hash', StringUtils.convertToMD5),
}

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        query = event.get_argument() or ""
        
        parts = query.split(" ", 1)
        command = parts[0].lower()
        
        if not query:
            for key, (friendlyName, _) in UTILS.items():
                items.append(self._createCommandItem(event, key, friendlyName))
            return RenderResultListAction(items)
        
        if command in UTILS:
            if len(parts) == 1:
                friendlyName, _ = UTILS[command]
                items.append(self._createCommandItem(event, command, friendlyName))
                return RenderResultListAction(items)
            
            text = parts[1]
            friendlyName, func = UTILS[command]
            processed = func(text)
            items.append(self._createResultItem(processed, friendlyName))
            return RenderResultListAction(items)
        
        for key, (friendlyName, func) in UTILS.items():
            processed = func(query)
            items.append(self._createResultItem(processed, friendlyName))
        return RenderResultListAction(items)
    
    def _createCommandItem(self, event, command, friendly_name):
        return ExtensionResultItem(
            icon='images/icon.png',
            name=friendly_name,
            description=f"Type text to {friendly_name.lower()}",
            highlightable=False,
            on_enter=SetUserQueryAction(f"{event.get_keyword()} {command} ")
        )
        
    def _createResultItem(self, processed, friendly_name):
        return ExtensionResultItem(
            icon='images/icon.png',
            name=f"{friendly_name}",
            description=f"Press Enter to copy: {processed}",
            highlightable=False,
            on_enter=CopyToClipboardAction(processed)
        )
        
class StringUtilsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

if __name__ == '__main__':
    StringUtilsExtension().run()