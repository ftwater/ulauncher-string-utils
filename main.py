import re
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

class StringUtils:
    def removeSpecialCharacters(text) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', text)
    
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
        words = text.split()
        return ' '.join(word.capitalize() for word in words)
    
    def splitText(text) -> str:
        return text.split()
    

UTILS = {
    'remove': ('Remove Special Characters', StringUtils.removeSpecialCharacters),
    'upper': ('Convert to Upper Case', StringUtils.convertToUpperCase),
    'lower': ('Convert to Lower Case', StringUtils.convertToLowerCase),
    'camel': ('Convert to Camel Case', StringUtils.convertToCamelCase),
    'snake': ('Convert to Snake Case', StringUtils.convertToSnakeCase),
    'kebab': ('Convert to Kebab Case', StringUtils.convertToKebabCase),
    'sentence': ('Convert to Sentence Case', StringUtils.convertToSentenceCase),
}

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        query = event.get_argument() or ""
        
        if not query:
            for key, (friendlyName, _) in UTILS.items():
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=friendlyName,
                    description=f"Digite o texto para {friendlyName.lower()}",
                    highlightable=False,
                    on_enter=SetUserQueryAction(f"{event.get_keyword()} {key} ")
                ))
        
            return RenderResultListAction(items)
            
        for key, (friendlyName, func) in UTILS.items():
            processed = func(query)
            items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f"{friendlyName}",
            description=f"Pressione Enter para copiar: {processed}",
            highlightable=False,
            on_enter=CopyToClipboardAction(processed)
            ))
        
        return RenderResultListAction(items)

class StringUtilsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

if __name__ == '__main__':
    StringUtilsExtension().run()