# github-kotlin-code-collector

Collection of files with Kotlin code from Github (by keyword).

### Example of use

```
python3 main.py --keyword fun --token my_github_token --directory ./code
```

## Program arguments

- **--keyword (k-)**: keyword for search on Github
- **--token (t-)**: Github token (you can generate in [personal access token page](https://github.com/settings/tokens) on Github)
- **--directory (d-)**: output folder with Kotlin source code files

For code parsing you can [kotlin-source2ast program](https://github.com/PetukhovVictor/kotlin-source2ast)
