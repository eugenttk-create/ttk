# PSAgrupp Peugeot Parser

## Подготовка
1. Поместите входной HTML-файл в `data/ID_Peugeot.html`.
2. Создайте виртуальное окружение и установите зависимости:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Запуск
```powershell
python .\src\parse_peugeot.py --input .\data\ID_Peugeot.html --output .\out\categories.xlsx --verbose
```
