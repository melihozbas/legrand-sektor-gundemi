import json, re, hashlib, html, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent
DEST=ROOT/'data'/'news.json'
QUERIES=[('Mevzuat','elektrik tesisatı yönetmelik Resmi Gazete'),('Enerji','EPDK elektrik piyasası yönetmelik değişiklik'),('Standartlar','TSE elektrik standart duyuru'),('Meslek Odaları','EMO elektrik mühendisleri odası yönetmelik'),('Akıllı Binalar','bina enerji performansı otomasyon yönetmelik'),('Veri Merkezleri','Türkiye veri merkezi enerji altyapısı yatırım')]
RULES=[('AFDD / DX³ Stop Arc',['ark hatası','yangın','afdd'],'Elektriksel yangın güvenliği üzerine teknik eğitim hazırlanması değerlendirilebilir.'),('Parafudr / SPD',['aşırı gerilim','yıldırım','parafudr','spd'],'Parafudr seçimi ve koruma koordinasyonu konusunda teknik içerik hazırlanabilir.'),('KNX ve sensörler',['akıllı bina','bina otomasyon','enerji performansı','aydınlatma kontrol'],'Bina otomasyonu ve enerji verimliliği için uygulama örnekleri hazırlanabilir.'),('DPX³ / DMX³',['şalt','dağıtım panosu','kısa devre','kesici'],'Dağıtım ve koruma çözümlerine ilişkin teknik eğitim fırsatı incelenebilir.'),('Veri merkezi çözümleri',['veri merkezi','data center'],'Veri merkezi altyapı çözümleri için hedef kitle bilgilendirmesi değerlendirilebilir.'),('Kaçak akım koruma',['kaçak akım','rcd','elektrik çarpması'],'Kaçak akım koruması ve doğru ürün seçimi konusunda eğitim hazırlanabilir.')]
def plain(s):return re.sub(r'<[^>]+>',' ',html.unescape(s or '')).strip()
def fetch(query):
    url='https://news.google.com/rss/search?q='+urllib.parse.quote(query+' when:14d')+'&hl=tr&gl=TR&ceid=TR:tr'
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 LegrandSectorResearchPrototype/1.0'})
    with urllib.request.urlopen(req,timeout=18) as resp:return ET.fromstring(resp.read())
def main():
    old=[]
    if DEST.exists():
        try:old=json.loads(DEST.read_text(encoding='utf-8')).get('items',[])
        except (ValueError,TypeError):pass
    seen={x['id']:x for x in old}
    errors=[];added=0
    for category,query in QUERIES:
        try:
            root=fetch(query)
            for item in root.findall('./channel/item')[:18]:
                title=plain(item.findtext('title'));link=(item.findtext('link') or '').strip();date=item.findtext('pubDate') or ''
                if not title or not link:continue
                uid=hashlib.sha256((title.lower()+link).encode()).hexdigest()[:16]
                if uid in seen:continue
                desc=plain(item.findtext('description'))
                src=item.find('source');source=src.text if src is not None and src.text else 'Google Haberler RSS'
                from email.utils import parsedate_to_datetime
                try:stamp=parsedate_to_datetime(date).astimezone(timezone.utc).isoformat()
                except Exception:stamp=datetime.now(timezone.utc).isoformat()
                combined=(title+' '+desc).lower();matched=[{'name':n,'action':a} for n,keys,a in RULES if any(k in combined for k in keys)]
                seen[uid]={'id':uid,'title':title,'category':category,'source':source,'url':link,'published':stamp,'summary':desc[:700] or 'Özet RSS kaynağında bulunamadı. Ayrıntılar için orijinal yayını açın.','products':matched,'status':'Sektörel haber / otomatik kayıt','verified':False}
                added+=1
        except Exception as e:errors.append(f'{category}: {type(e).__name__}: {e}')
    items=sorted(seen.values(),key=lambda x:x.get('published',''),reverse=True)[:350]
    DEST.parent.mkdir(exist_ok=True)
    DEST.write_text(json.dumps({'last_checked':datetime.now(timezone.utc).isoformat(),'new_items':added,'errors':errors,'items':items},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(items)} kayıt, {added} yeni; {len(errors)} kaynak hatası')
    for e in errors:print(e)
if __name__=='__main__':main()
