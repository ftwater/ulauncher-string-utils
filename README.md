# String Utils

A simple Ulauncher extension that provides various string manipulation utilities.

## Features

* **remove** - Remove special characters
* **upper** - Convert text to UPPERCASE
* **lower** - Convert text to lowercase
* **camel** - Convert to CamelCase
* **snake** - Convert to snake_case
* **kebab** - Convert to kebab-case
* **sentence** - Convert to Sentence case
* **sqlinstr** - Convert to SQL IN String (e.g., 'aa','bb','cc')
* **sqlinnum** - Convert to SQL IN Numbers (e.g., 11,22,33)

## Usage

Type the keyword followed by the command and the text you want to process:

```
str [command] [text]
```

For example:
```
str upper hello world
str sqlinstr apple\nbanana\norange  →  'apple','banana','orange'
str sqlinnum 11\n22\n33             →  11,22,33
```

Press Enter to copy the result to clipboard.
