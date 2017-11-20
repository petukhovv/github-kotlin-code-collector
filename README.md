# github-kotlin-code-collector

Collection of files with Kotlin code from Github (by keywords), and:
- either their parsing (compiler run) and resulting AST conversion to JSON (and saving AST in JSON format in specified folder);
- or just saving in .kt file (if --no-compile option is specified).

### Running example with parsing

```
python3 main.py
```
Parsing performed by the Kotlin compiler (required custom Kotlin compiler version: https://github.com/PetukhovVictor/kotlin-academic/tree/vp/ast_printing_text)

Saving directory by default: **./ast**

### Running example without parsing (just saving of source code)

```
python3 main.py --no-compile
```

Saving directory by default: **./code**
