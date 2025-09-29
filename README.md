# rok

Proje: Rise of Kingdoms benzeri kamera temelli otomasyon için anakare (core region) model ve araçları.

- src/regions: koordinat dönüşümleri, region fabrikası, navigator
- src/engine: Supervisor (ekran durum denetimi)
- tests: birim testler

Çalıştırma:
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
